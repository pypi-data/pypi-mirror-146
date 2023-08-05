import numpy as np
import os
import shutil
import keyboard
import socket
import pywifi
from Robot import *
from Gyro import *

# 保存包中写义的常量
from pywifi import const

"""                  神经网络控制参数                 """
w1 = np.loadtxt("./Data/BP_net/Net6/w1.txt", delimiter=" ", dtype="float")
w2 = np.loadtxt("./Data/BP_net/Net6/w2.txt", delimiter=" ", dtype="float")
b1 = np.loadtxt("./Data/BP_net/Net6/b1.txt", delimiter=" ", dtype="float")
b2 = np.loadtxt("./Data/BP_net/Net6/b2.txt", delimiter=" ", dtype="float")
b1 = np.array([b1.tolist()]).T

"""                      控制参数                     """
con_time = 100  # ms
N = 1  # 控制采样频率相对指令的倍数
gravity = 0


def connect_all():
    global gyro_1, gyro_3, server
    while 1:
        s_client, adder = server.accept()
        try:
            raw_data = s_client.recv(11)
            if raw_data[1] == 1:
                s_id = raw_data[2]
                exec('gyro_{0}.client = s_client'.format(s_id))
                exec('gyro_{0}.adder = adder'.format(s_id))
                exec('gyro_{0}.name = s_id'.format(s_id))
                exec('Gyro.client_index.append({0})'.format(s_id))
                print('陀螺仪ID:', s_id, '成功连接')

            if raw_data[1] == 0:
                robot.client = s_client
                robot.adder = adder
                robot.status = True
                print('机械腿成功连接')
        except Exception as e:
            print(e)


def control_main():
    global gravity, gyro_1, gyro_3, robot

    # 默认舵机位置
    bus_data_s = [500, 500, 500, 500]

    time.sleep(1)
    while 1:
        # 导入陀螺仪数据，组成神经网络输入端数据
        # data_set = [[gyro_1.ax, gyro_1.ay, gyro_1.az, gyro_4.ax,
        #              gyro_4.ay, gyro_4.az, gyro_1.roll, gyro_1.pitch,
        #              gyro_1.yaw, gyro_4.roll, gyro_4.pitch, gyro_4.yaw]]
        # data_set = np.array(data_set).T

        # TODO 待测试神经网络代码，现用经验法判断
        # if settle_down(data_set):
        #     robot.servo_move([1, 4], [500, 500], 200)
        #     time.sleep(0.2)
        #     gravity = 0

        # 若一只腿抬起则将重心偏移致并双腿恢复到并排状态
        if gyro_3.roll - gyro_3.roll_before > 0.1 and gravity == 0:
            robot.move([1, 4], [440, 440], 200)
            time.sleep(0.2)
            robot.move([2, 3, 5, 6], [500, 500, 500, 500], 500)  # 步距补偿
            time.sleep(0.5)
            gravity = 1

        # 在gravity=1状态下跟随动作并检测是否落脚
        if abs(gyro_3.roll + gyro_1.roll) > 1 and gravity == 1 and abs(gyro_3.roll) <= 135:
            bus_data_s[0] = \
                500 + gyro_3.roll / 270 * 1000
            bus_data_s[1] = \
                500 + gyro_3.roll / 270 * 1000
            bus_data_s[2] = \
                500 + gyro_3.roll / 270 * 1000
            bus_data_s[3] = \
                500 + gyro_3.roll / 270 * 1000
            robot.move([2, 3, 5, 6], bus_data_s, con_time)
            time.sleep(con_time / 1000)

            # 此处使用8倍关系经验判断落脚阈值为5度
            if gyro_3.roll + 8 * gyro_1.roll < 5:
                robot.move([1, 4], [500, 500], 200)
                time.sleep(0.2)
                gravity = 0

        # 相同的操作在另外一只脚上的镜像
        if gyro_1.roll - gyro_1.roll_before > 0.1 and gravity == 0:
            robot.move([1, 4], [560, 560], 200)
            time.sleep(0.2)
            robot.move([2, 3, 5, 6], [500, 500, 500, 500], 500)
            time.sleep(0.5)
            gravity = -1

        # 相同的操作在另外一只脚上的跟随
        if abs(gyro_3.roll + gyro_1.roll) > 1 and gravity == -1 and abs(gyro_1.roll) < 135:
            bus_data_s[0] = \
                500 - gyro_1.roll / 270 * 1000
            bus_data_s[1] = \
                500 - gyro_1.roll / 270 * 1000
            bus_data_s[2] = \
                500 - gyro_1.roll / 270 * 1000
            bus_data_s[3] = \
                500 - gyro_1.roll / 270 * 1000
            robot.move([2, 3, 5, 6], bus_data_s, con_time)
            time.sleep(con_time / 1000)

            # 相同的操作以8倍关系经验判断落脚阈值为5度
            if gyro_1.roll + 8 * gyro_3.roll < 5:
                robot.move([1, 4], [500, 500], 200)
                time.sleep(0.2)
                gravity = 0


def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    while 1:
        try:
            s.connect(('198.168.1.1', 80))
            ip = s.getsockname()[0]
            break
        finally:
            s.close()
    print("服务器IP为：", ip)
    return ip


# 创建激活函数sigmoid
def sigmoid(z):
    return 2 / (1 + np.exp(-2 * z)) - 1


def settle_down(data):
    step1 = np.dot(w1, data)
    step2 = sigmoid(step1 - b1)
    step3 = np.dot(w2, step2)
    step4 = sigmoid(step3 - b2)
    output = np.heaviside(step4 - 0.5, 1)
    return output


def setdir(filepath):
    if not os.path.exists(filepath):
        os.mkdir(filepath)
    else:
        shutil.rmtree(filepath)
        os.mkdir(filepath)


def key_scan(flag):
    try:
        if keyboard.is_pressed('space'):
            print('记录落脚一次')
            flag = 1
    except Exception as e:
        print(e)
    return flag


def connect_wifi(ssid, key):
    wifi = pywifi.PyWiFi()  # 创建一个wifi对象
    ifaces = wifi.interfaces()[0]  # 取第一个无限网卡
    # print(ifaces.name())  # 输出无线网卡名称
    ifaces.disconnect()  # 断开网卡连接
    time.sleep(3)  # 缓冲3秒

    profile = pywifi.Profile()  # 配置文件
    profile.ssid = ssid  # wifi名称
    profile.auth = const.AUTH_ALG_OPEN  # 需要密码
    profile.akm.append(const.AKM_TYPE_WPA2PSK)  # 加密类型
    profile.cipher = const.CIPHER_TYPE_CCMP  # 加密单元
    profile.key = key  # wifi密码

    ifaces.remove_all_network_profiles()  # 删除其他配置文件
    tmp_profile = ifaces.add_network_profile(profile)  # 加载配置文件

    ifaces.connect(tmp_profile)  # 连接
    time.sleep(5)  # 尝试10秒能否成功连接
    if ifaces.status() == const.IFACE_CONNECTED:
        print("连接WiFi:", ssid, "成功")
        return True
    else:
        print("连接WiFi:", ssid, "失败")
        return False


def server_init(port):
    server_s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # 不经过WAIT_TIME，直接关闭
    # server_s.setblocking(False)  # 设置非阻塞编程
    server_s.bind((get_ip(), port))  # 自动获取本机ip 并在8000端口创建服务器
    server_s.listen(5)
    print("服务器准备就绪,等待客户端上线..........\r\n")
    return server_s


"""           建立一个服务端            """
server = server_init(8000)
"""            生成控制对象               """
gyro_1 = Gyro(server)
gyro_3 = Gyro(server)
robot = Robot(server)
gravity = 0

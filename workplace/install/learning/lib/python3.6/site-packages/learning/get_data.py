# -*- coding:utf-8 -*-
import socket
import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32MultiArray

class SocketReciv:
    def __init__(self, name) -> None:
        super().__init__(name)
        self.dog_name="az"
        self.ip = '10.0.0.143' # 查看上位机ip，进行修改
        self.client_socket = socket.socket()
        self.client_socket.connect((self.ip, 40000))
        self.ball_coords=(0,0)
        self.dog_coords=(0,0)
        self.client_socket.send('start'.encode())

    def get_dog_address(self):
        data = self.client_socket.recv(1024).decode()
        # split方法用于按空格分隔字符串
        a, b, c, d = data.split(' ')
        # 将字符串转换为浮点数，如果字符串为'None'，则返回None
        a = float(a) if a != 'None' else None
        b = float(b) if b != 'None' else None
        c = float(c) if c != 'None' else None
        d = float(d) if d != 'None' else None
        self.ball_coords=(a,b)
        self.dog_coords=(c,d)
    
    def sub_callback(self, msg: Range):
        '''the callback function of subscriber'''

        self.get_logger().info(f"the distance is {dist}")
        ball_coords, dog_coords = get_dog_address(client_socket)
        dog_target_coords = get_dog_target_position(ball_coords, goal_coords)

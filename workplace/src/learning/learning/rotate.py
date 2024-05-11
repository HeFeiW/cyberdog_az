'''
让狗转，直到球处于视野中心（实现方法：让绿球x坐标位于260-400间）
跟随球出视野方向旋转，
函数rotate_aim_ball(mode=0)，
mode=0：球处于中心，停止，返回True
mode=1:持续动态跟随，直到KeyBoardInterrupt，返回True
'''
import cv2
import numpy as np
from cv_bridge import CvBridge
from rclpy.node import Node
from sensor_msgs.msg import Image
from protocol.msg import MotionServoCmd
import rclpy
import threading
import time
from .rgb_cam_suber import rgb_cam_suber
from .stop_node import StopNode


class rotate(Node):
    def __init__(self, name, rgb_cam_suber,left=1):
        super().__init__(name)
        self.rgb_node = rgb_cam_suber
        self.speed_x, self.speed_y, self.speed_z = 0.0, 0.0, 0.0
        self.dog_name = "az"
        self.pub = self.create_publisher(MotionServoCmd, f"/{self.dog_name}/motion_servo_cmd", 10)
        self.timer = self.create_timer(0.1, self.timer_callback)
        if (1 == left):
            self.x_rec=[.0,.0,.0,.0,.0]
        else :
            self.x_rec=[640.,640.,640.,640.,640.]
        self.aim = False
        self.prefer_direc = left # 1 for left, -1 for right

    def timer_callback(self):
        rclpy.spin_once(self.rgb_node)
        ball_x, ball_y = self.rgb_node.ball_position
        size = self.rgb_node.size
        if ball_x != 0:
            self.x_rec.pop(0)
            self.x_rec.append(ball_x)
        if size < 100:
            av=sum(self.x_rec)/len(self.x_rec)
            if av < 10:
                self.speed_x, self.speed_y, self.speed_z = 0.0, 0.0, 0.5*self.prefer_direc
            if  av < 320:
                self.speed_x, self.speed_y, self.speed_z = 0.0, 0.0, 0.5
            else:
                self.speed_x, self.speed_y, self.speed_z = 0.0, 0.0, -0.5
        elif ball_x > 260 and ball_x < 380:
            self.speed_z = 0.0
            self.aim = True
        elif ball_x <= 260:
            self.speed_x, self.speed_y, self.speed_z = 0.0, 0.0, 0.25
        else:
            self.speed_x, self.speed_y, self.speed_z = 0.0, 0.0, -0.25

        msg = MotionServoCmd()
        msg.motion_id = 308
        msg.cmd_type = 1
        msg.value = 2
        msg.vel_des = [self.speed_x, self.speed_y, self.speed_z]
        msg.step_height = [0.05, 0.05]
        self.pub.publish(msg)
        self.get_logger().info(f"x={ball_x},arr={self.x_rec}rotate={self.speed_z}")

def rotate_aim_ball(mode=0,left=1):
    rclpy.init(args=None)
    rgb_node = rgb_cam_suber("rgb_cam_suber")
    rotate_node = rotate("rotate_node", rgb_node,left)
    stop_node = StopNode("stop_node")
    rotate_thread = threading.Thread(target=rclpy.spin, args=(rotate_node,))
    rotate_thread.start()
    if mode == 0:
        while(rotate_node.aim == False):
            pass
    elif mode == 1:
        try:
            while True:
                pass
        except KeyboardInterrupt:
            print('KeyBoardInterrupt')
    stop_thread = threading.Thread(target=rclpy.spin, args=(stop_node,))
    stop_thread.start()
    time.sleep(0.1)
    rotate_node.destroy_node()
    rgb_node.destroy_node()
    stop_node.destroy_node()
    rclpy.shutdown()
    cv2.destroyAllWindows()
    return True

def main(args=None):
    print(rotate_aim_ball())

if __name__ == '__main__':
    main()

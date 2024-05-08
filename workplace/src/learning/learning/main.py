import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Range
from protocol.msg import MotionServoCmd
import threading
import time

import rotate
from walk_t_sec import move_t_sec
import routine



def main(args=None):
    rclpy.init(args=args)
    sensor_node = sensor_suber("my_sensor")
    move_node = basic_move("move_node", sensor_node)
    rclpy.spin_once(sensor_node)
    rclpy.spin(move_node)
    move_node.destroy_node()
    sensor_node.destroy_node()
    rclpy.shutdown()

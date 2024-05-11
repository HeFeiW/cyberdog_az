'''
> main.py
> author: whf
> date: 2024-5-11
> draft of main function for striker
'''
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Range
from protocol.msg import MotionServoCmd
import threading
import time

import rotate
from walk_t_sec import move_t_sec
import routine
from get_loc import LocReciv


def main(args=None):
    rclpy.init(args=args)
    prefer_dirc = 1 # preferred direction for rotation, 1 for right, -1 for left

    loc_receiv = LocReciv()
    loc_receiv.start_in_thread()

    

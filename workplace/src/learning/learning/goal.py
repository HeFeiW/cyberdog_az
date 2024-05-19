
'''
提供一个射门方法make_goal()
'''
from .walk_t_sec import move_t_sec
import rclpy
from rclpy.node import Node
from protocol.msg import MotionServoCmd
import threading
import time

def make_goal(dist):
    ok = 0
    # ok=move_t_sec(1.2,0,-0.5)
    # while not ok:
    #     pass
    ok=move_t_sec(dist,0,1.0)
def main(args=None):
    make_goal()

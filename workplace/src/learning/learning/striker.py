import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Range
from protocol.msg import MotionServoCmd
import socket
import sys
import time
import numpy as np
from cv_bridge import CvBridge
from .walk_t_sec import move_t_sec
from .rotate import rotate_aim_ball
from .goal import make_goal
from .data_receive import get_dog_address
from .routine import get_goal_coords
from .routine import get_routine
def main():
    rotate_aim_ball()
    dist=2.5
    gate_coords=[0.0,7.9]
    ball_coords,dog_coords = get_dog_address()
    print(ball_coords,dog_coords)
    goal_coords,right=get_goal_coords(ball_coords,dog_coords,gate_coords,dist)
    print(goal_coords[0],goal_coords[1])
    theta,goDist=get_routine(ball_coords,dog_coords,goal_coords,right)
    theta = theta * 1.1 #修正因子
    goDist = goDist * 0.95
    ok=0
    left =0
    if theta < 0:
        theta = abs(theta)
        ok=move_t_sec(theta/0.3,2,-0.3)
        left = 1
    else:
        ok=move_t_sec(theta/0.5,2,0.5)
        left = -1
    if (ok):
        move_t_sec(goDist/0.5,0,0.5)
    rotate_aim_ball(0,left)
    make_goal(dist+1.5)
if __name__ == "__main__": 
    main()
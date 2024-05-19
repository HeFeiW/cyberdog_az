
'''
0519
LX
提供一个射门方法shoot(mode,translation_dist,socket) mode=0:在足球正后方射门 mode=1:旋转对准球后射门 
mode=2:球在场地左侧不可射门区，向右平移带球至可射门区后从正后方射门 mode=3:球在场地右侧不可射门区，向左平移带球至可射门区从正后方射门
mode=4:不可射门 do nothing
translation_dist 平移距离 暂时缺省设定为1.5，也许后续可以从get_routine函数中获得一个更好的值
socket用于获得平移推球后球的坐标
'''
from .walk_t_sec import move_t_sec
import rclpy
from rclpy.node import Node
from protocol.msg import MotionServoCmd
import threading
import time
from .stop_node import StopNode
from .socket import SocketReciv
from .move_to_target import dist
from .move_to_target import moveto
from .goal import make_goal
from .rotate import rotate_aim_ball
from .walk_t_sec import move_t_sec

def shoot(mode,socket,translation_dist=1.5):
    shoot_dist=2
    if mode == 0 :#正后方直接射门
        make_goal(shoot_dist)
    elif mode == 1: #先转，斜着对着射门
        rotation=rotate_aim_ball()*1.05 #请别吐槽。。
        make_goal(shoot_dist)
        if rotation>0:
            move_t_sec(rotation/0.5,2,-0.5)
        else:
            rotation = abs(rotation)
            move_t_sec(rotation/0.5,2,0.5)
    elif mode == 2:#球在左侧不可射门区，这时假设已经移动到球的左边，并且向右带球
        move_t_sec(translation_dist/0.25,1,0.25)
        ball_coords, dog_coords, _ = socket.get_data()
        target_coords=(ball_coords[0],ball_coords[1]-1)#这里后期用get_routine直接获得目标坐标和射门方式mode比较好一点
        mode = 0
        moveto(target_coords,socket)
        shoot(0,socket)
    elif mode == 3:
        move_t_sec(translation_dist/0.25,1,-0.25)
        ball_coords, dog_coords, _ = socket.get_data()
        target_coords=(ball_coords[0],ball_coords[1]-1)#这里后期用get_routine直接获得目标坐标和射门方式mode比较好一点
        mode = 0
        moveto(target_coords,socket)
        shoot(0,socket)
    elif mode == 4:
        print("无法射门")
    


def main(args=None):
    socket1=SocketReciv()
    shoot(1,socket1)
if __name__ == "__main__": 
    main()

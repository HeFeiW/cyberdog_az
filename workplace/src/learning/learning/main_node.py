'''
>   author: whf
>   date:2024-05-22
>   main node:
        always spin this node and do not create or destroy other nodes repeatedly
'''
from .draw import Record
import rclpy
from .rgb_cam_suber import RGBCamSuber
from .move_node import Move
from .get_data import Location
from .routine import get_goal_coords
import time
import traceback
import sys
from .constants import C

def main(args=None):
    #   整个函数包在try里，这样 catch 异常并退出之前可以主动断开与上位机连接防止多次失败测试之后上位机过载。
    print(C.ERROR)
    rclpy.init(args=args)
    # rgb_cam_suber = RGBCamSuber('rgb_s')
    # rclpy.spin_once(rgb_cam_suber)
    # record = Record()
    location = Location()
    print(f'where are we?')
    move = Move(location)
    try:
        # TODO 主循环，实际使用时可以改成 while True循环
        i = 0
        while True:
            i += 1
            print(f'-----in loop {i}-----')
            while time.time()-location.my_loc_rec()[4][0] > 1:
                #   确保当前自身位置信息是更新过的（上次时间戳距今小于 1s）
                print(f'latest rec at {location.my_loc_rec()[4][0]}')
                location.get_data()
            ball_dist = location.dist(location.my_loc(),location.ball)
            if location.isBallBehind():#球在正后方
                duration = (ball_dist+0.8)/(0.8*C.MAX_SPEED_Y)
                if location.my_loc()[0]>0:#在球场右半边
                    if C.COLOR == 0:#red
                        move.go_for(2.0,[-0.5,0.0,0.0])
                        move.go_for(duration,[0.0,-0.8*C.MAX_SPEED_Y,0.0])
                    elif C.COLOR == 1:#black
                        move.go_for(2.0,[-0.5,0.0,0.0])
                        move.go_for(duration,[0.0,0.8*C.MAX_SPEED_Y,0.0])
                elif location.my_loc()[0]<0:#在球场左半边
                    if C.COLOR == 0:#red
                        move.go_for(2.0,[0.5,0.0,0.0])
                        move.go_for(duration,[0.0,-0.8*C.MAX_SPEED_Y,0.0])
                    elif C.COLOR == 1:#black
                        move.go_for(2.0,[0.5,0.0,0.0])
                        move.go_for(duration,[0.0,0.8*C.MAX_SPEED_Y,0.0])
            target,_,shoot_mode= get_goal_coords(location.ball,location.my_loc(),C.GATE,C.DIST)
            print(f'target is{target}')
            if location.NotOut(target):
                print(f'target not out')
            else:
                print(f'shoot target out of filed')
                move.goto(C.START_POINT)
                continue
            print(f'ball:{location.ball},me:{location.my_loc()}')
            # target = location.MayCrash(target)
            if not move.goto(target):
                continue
            # TODO check if ball_loc satisfies the requirements to shoot
            # if not location.CanShoot():
            #     continue
            print(f'Can Shoot!')
            move.shoot(shoot_mode)
            # move.shoot2()
            print('successfully shoot!')
            print('sleeping...')
            if location.Scored():
                move.goto(C.START_POINT)
            print("Let's do it again!")
            # record.add_loc(location)
            # record.add_my_vel(move)
            # record.draw(location)
        rclpy.shutdown()
    except Exception as e:
        print(e)
        exc_type, exc_value, exc_traceback = sys.exc_info()
        traceback.print_exception(exc_type, exc_value, exc_traceback, limit=None, file=sys.stdout)
    finally:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        traceback.print_exception(exc_type, exc_value, exc_traceback, limit=None, file=sys.stdout)
        location.close()
if __name__ == '__main__':
    main()
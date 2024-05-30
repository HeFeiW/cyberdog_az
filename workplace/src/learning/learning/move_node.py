
'''
>   move_node.py
>   author: whf & lx
>   date: 2024-05-22
>   All moving-related functions packed together.
>   funtions:
    - goto(self,target,frequency = 0.3)
    - go_for(self,duration,vel)
>   all calculation are based on upper-computer coordinate system, velocity will be converted to dog coordinate system in func go().
from:move_to_target.py
    05/18 李想
    提供一个move到目标坐标的方法move_to(goal_address,socket).传入一个目标坐标和SocketReciv类示例
    目前步态是慢速步态，最大纵向速度0.65，最大横移速度0.3， 最大角速度1.25.
    注意必须输入浮点数
'''
import math
from rclpy.node import Node
from protocol.msg import MotionServoCmd
import time
from .get_data import Location
from .rotate import rotate_aim_ball
from .constants import C
from .rgb_cam_suber import RGBCamSuber
import rclpy
import traceback
from .geometry import Line
class Move(Node):
    def __init__(self,location:Location):
        super().__init__('move_node')
        self.dog_name = C.NAME
        self.pub = self.create_publisher(MotionServoCmd, f"/{self.dog_name}/motion_servo_cmd", 1)
        self.arrived=False
        self.max_speed_x = C.MAX_SPEED_X
        self.max_speed_y = C.MAX_SPEED_Y
        self.max_speed_z = C.MAX_SPEED_Z
        self.GATE = C.GATE
        self.DIST = C.DIST
        self.location = location
        self.rgb_node = RGBCamSuber("rgb_cam_suber")
    def goto(self,target,accurate_mode = True, frequency = C.FREQUENCY):    # mode == 1， accurate mode, get data while going; mode == 0, fast mode, dont get data.
        '''
        goto(self,target:target_coords)
        go to point [target] at max speed.
        update movement cmd evert [frequency] seconds.
        for accurate_mode:
            update location every cycle of operation, and update target.
        for
        '''
        mid_target = target
        print(f'==== goto:{target} ====')
        ratio = 1.0 #speed ratio, 1.0 for full speed,decays with distance
        while not self.location.in_place(target):
            if accurate_mode:
                #   accurate mode
                if not self.location.CanShoot(target):
                    #   如果发现在目标点已经不符合射门要求（即球移动了，使得原先的target失效），此时判定为这一次goto失效。
                    print(f'==== goto:target {target} no longer effective ====')
                    return False
                mid_target = self.location.MayCrash(target)
                dist_to_target = dist(self.location.my_loc(), target)
                if dist_to_target > C.DIST_TO_TARGET_THRESHOLD:
                    ratio = 1.0
                else:
                    ratio = 0.2+0.8 * dist_to_target/C.DIST_TO_TARGET_THRESHOLD #decay speed with distance
            else:
                dist_to_target = dist(self.location.my_loc(), target)
                #   fast mode 不加校正地走到target（用于射门）
                if dist_to_target > C.DIST_TO_TARGET_THRESHOLD:
                    ratio = 1.0
                else:
                    a = 0.5 / (1 - math.exp(-C.DIST_TO_TARGET_THRESHOLD))
                    b = 0.5 + a
                    ratio = b - a * math.exp(-dist_to_target)
                mid_target = target
            v =self.max_vel(mid_target,self.location.my_loc(),ratio)
            vel = [v[0],v[1],.0]
            self.go(vel)
            time.sleep(0.1)
            if mid_target is not target:
                print(f'--- goto():mid_target {mid_target}')
        self.stop()
        print(f'==== goto:targeting {target}, arrived at {self.location.my_loc()} ====') 
        return True
    def go_for(self,duration,vel):
        '''
        go for [duration] seconds at speed [vel]
        vel:[speed+x,speed_y,speed_z]
        '''
        if duration != 0:
            print(f'going for {duration} seconds')
            current_time =time.time()
            while(time.time()-current_time<duration):
                 self.go(vel)
                 time.sleep(0.1)
            self.stop()
        if duration == 0:
            pass
        #   一直走。用while循环加订阅话题跳出
        return True

    def stop(self):
        '''
        stop the robot
        '''
        self.go([.0,.0,.0])
        return
    def go(self,vel,mode = 0):
        '''
        一个比较方便的生成并发送cmd封装，输入vel三元列表即可
        若mode缺省或为0，输入上位机坐标系下速度，在函数内映射为自身速度；
        若mode为 1 ，输入自身坐标系下速度。
        '''
        msg = MotionServoCmd()
        msg.motion_id =C.MOTION_ID
        msg.cmd_type = 1
        msg.value = 2
        if mode == 0:
            if C.COLOR == 0:    # RED
                msg.vel_des = [vel[1],-vel[0],vel[2]]
            elif C.COLOR == 1:
                msg.vel_des = [-vel[1],vel[0],vel[2]]
        else:
            msg.vel_des = vel
        print(f'vel:{msg.vel_des}')
        msg.step_height = C.STEP_HEIGHT
        self.pub.publish(msg)
    def max_vel(self,target,me,ratio = 1.0):
        '''
        max_vel(self,target:target_coords,me: my_coords)
        return the max velocity pointing from me to target.
        '''
        vector = [.0,.0]
        dir = [1,1]
        vector[0]=target[0]-me[0]
        vector[1]=target[1]-me[1]
        dir = [vector[0]/abs(vector[0]),vector[1]/abs(vector[1])]
        max_x = self.max_speed_x * ratio
        max_y = self.max_speed_y * ratio
        max_z = self.max_speed_z * ratio
        vel_x = abs(max_y * vector[0] / vector[1])   #   TODO xy好像有问题
        if vel_x <= max_x:
            vel = [dir[0] * vel_x,dir[1] * max_y]
        else:
            vel = [dir[0] * max_x , dir[1] * abs(max_x * vector[1] / vector[0])]
        return vel 
    def rotate_aim_ball(self,mode=0,left=1):
        if (1 == left):
            self.x_rec=[.0,.0,.0,.0,.0]
        else :
            self.x_rec=[640.,640.,640.,640.,640.]
        self.aim = False
        self.prefer_direc = left # 1 for left, -1 for right
        self.total_rotation = 0.0  #total rotation
        current_time = time.time()
        while self.aim is not True and time.time()-current_time < C.TRANSLATE_TIMEOUT:   # timeout
            rclpy.spin_once(self.rgb_node)
            ball_x, ball_y = self.rgb_node.ball_position
            size = self.rgb_node.size
            vel = [.0,.0,.0]
            if ball_x != 0:
                self.x_rec.pop(0)
                self.x_rec.append(ball_x)
            if size < 100:
                av=sum(self.x_rec)/len(self.x_rec)
                if av < 10:
                    vel = [0.0, 0.0, 0.5*self.prefer_direc]
                elif  av < 320:
                    vel = [0.0, 0.0, 0.5]
                else:
                    vel = [0.0, 0.0, -0.5]
            elif ball_x > 360 and ball_x < 420:
                vel = [.0,.0,.0]
                self.aim = True
                return self.total_rotation
            elif ball_x <= 360:
                vel = [0.0, 0.0, 0.25]
            else:
                vel = [0.0, 0.0, -0.25]
            self.total_rotation += vel[2] * 0.1  # 更新累积的角度，注意这里的0.1是时间间隔
            self.go(vel)
            self.get_logger().info(f"x={ball_x},arr={self.x_rec}rotate={vel[2]}")
            time.sleep(0.1)    
        return self.total_rotation
    def translate_aim_ball(self,left=1):
        '''
        author:lx
        date:2024/0527
        >   translate to aim the ball
        >   if timeout,break
        '''
        self.speed_x, self.speed_y, self.speed_z = 0.0, 0.0, 0.0#初始化，防止AttributeError: 'Move' object has no attribute 'speed_x'
        if (1 == left):
            self.x_rec=[.0,.0,.0,.0,.0]
        else :
            self.x_rec=[640.,640.,640.,640.,640.]
        self.aim_horizontal = False
        self.prefer_direc_horizontal = left # 1 for left, -1 for right
        current_time = time.time()
        while self.aim_horizontal is not True and time.time()-current_time < C.TRANSLATE_TIMEOUT:#timeout
            rclpy.spin_once(self.rgb_node)
            ball_x, ball_y = self.rgb_node.ball_position
            size = self.rgb_node.size
            if ball_x != 0:
                self.x_rec.pop(0)
                self.x_rec.append(ball_x)
            if size < 100:
                av=sum(self.x_rec)/len(self.x_rec)
                if av < 10:
                    self.speed_x, self.speed_y, self.speed_z = 0.0, C.TRANSLATE_SPEED*self.prefer_direc_horizontal, 0.0
                elif  av < 320:
                    self.speed_x, self.speed_y, self.speed_z = 0.0, C.TRANSLATE_SPEED, 0.0
                else:
                    self.speed_x, self.speed_y, self.speed_z = 0.0, -C.TRANSLATE_SPEED, 0.0
            elif ball_x > 360 and ball_x < 400: #LX 0530 第2次调参
                self.speed_y = 0.0
                self.aim_horizontal = True
            elif ball_x <= 360:
                self.speed_x, self.speed_y, self.speed_z = 0.0, C.TRANSLATE_SPEED, 0.0
            else:
                self.speed_x, self.speed_y, self.speed_z = 0.0, -C.TRANSLATE_SPEED, 0.0
            self.go([self.speed_x,self.speed_y,self.speed_z],1)
            self.get_logger().info(f"translating,x={ball_x},arr={self.x_rec}")
            time.sleep(0.1)
        return True
        
    def shoot(self,mode=0,redundancy = 1.0):
        # 0528 LX改过
        '''
        shooting
        Mode 0: Shoot from directly behind the football
        Mode 1: Rotate to face the ball and then shoot
        Mode 2: No shooting, do nothing

        go [redundancy] meters further
        '''
        left = self.location.isLeft()
        shoot_dist = self.location.dist(self.location.ball,self.location.my_loc())
        print(f"ball is on the {left}")
        if mode == 0:
            self.translate_aim_ball(left)
            print(f"ball is on the {left}")
            duration = (shoot_dist + redundancy)/(0.8 * self.max_speed_y)
            self.go_for(duration,[.0,0.8*self.max_speed_y,.0])#TODO change +/-
        elif mode == 1:
            ball_loc,me_loc = self.location.ball,self.location.my_loc()
            rotation=self.rotate_aim_ball(0,left) 
            duration = (shoot_dist + redundancy)/(0.8 * self.max_speed_y)
            self.go_for(duration,[.0,0.8*self.max_speed_y,.0]) #TODO change +/-
            if rotation>0:
                self.go_for(rotation/0.5,[.0,.0,-0.5])
            else:
                rotation = abs(rotation)
                self.go_for(rotation/0.5,[.0,.0,0.5])
        elif mode == 2:
            pass  
    def shoot2(self):
            #   get a rest point that is in the field, using geometry.Line.get_target 
            dist = 1.0
            if C.COLOR == 0:#red
                dir = 1
            if C.COLOR == 1:#black
                dir = -1
            shoot_line = Line(self.location.my_loc(),self.location.ball,2)
            rest_point = shoot_line.get_target(dist,dir)
            while not self.location.NotOut(rest_point):
                dist -= 0.1
                if dist <= 0.1:
                    rest_point = shoot_line.get_target(0.1,dir)
            #   go to the rest point
            self.goto(rest_point,False)
    def shoot3(self):
         #   get a rest point that is in the field, using y +/-
            dist = 1.
            if C.COLOR == 0:#red
                dir = 1
            if C.COLOR ==1:#black
                dir = -1
            rest_point = self.location.ball[1] + dir * dist
            while not self.location.NotOut(rest_point):
                dist -= 0.1
                rest_point = self.location.ball[1] + dir * dist
                if dist <= 0.1:
                    rest_point = self.location.ball[1] + dir * 0.1
            #   go to the rest point
            self.goto(rest_point,False)     
def dist(point1, point2):
        distance = math.sqrt((point2[0]-point1[0])**2 + (point2[1]-point1[1])**2)
        return distance
def main():
    rclpy.init()
    location = Location()  # Assuming Location is initialized without parameters
    GATE = [8.8,-0.2]
    DIST = 2.5
    move_node = Move(location)
    # Test go_for method
    # move_node.shoot(1)
    duration = 6.28  # Duration in seconds
    vel = [1.0, 0.0, 0.00]  # Velocity in x, y, z
    move_node.go_for(duration, vel)
    # vel = [0.0, 0.0, -1.00]
    # move_node.go_for(duration, vel)
    move_node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()
'''
>   draw.py
>   author:whf
>   date:2024-05-29
>   function:draw the track of the ball and the dogs
    call:
    -   initialize the class Record in the main function
    -   add_loc(location) to add the location of the ball and the dogs(sugggset call in get_data())
    -   add_target(target) to add the target location(suggest call in goto())
    -   add_my_vel(vel) to set the velocity of the dog(suggest call in go())
'''
from random import choice
import matplotlib.pyplot as plt
from .get_data import Location
from .move_node import move
from .constants import C
class Record():
    def __init__(self):
        self.figure = plt.figure()
        self.ax = self.figure.add_subplot(111)
        self.ax.set_title("track")
        self.ax.set_xlabel('x')
        self.ax.set_ylabel('y')
        self.ax.set_xlim(-3.,3.)
        self.ax.set_ylim(.0,9.)
        self.ax.set_aspect('equal')
        self.ax.grid()
        self.red_dog = [[],[]]
        self.black_dog = [[],[]]
        self.ball = [[],[]]
        self.target = [[],[]]
        self.ball_vel = [.0,.0]
        self.red_dog_vel = [.0,.0]
        self.black_dog_vel = [.0,.0]
        self.point_num = 15
    def add_loc(self,location):
        self.ball[0].append(location.ball[0])
        self.ball[1].append(location.ball[1])
        self.red_dog[0].append(location.red_dog[0])
        self.red_dog[1].append(location.red_dog[1])
        self.black_dog[0].append(location.black_dog[0])
        self.black_dog[1].append(location.black_dog[1])
        while len(self.ball[0]) > self.point_num:
            self.ball[0].pop(0)
            self.ball[1].pop(0)
            self.red_dog[0].pop(0)
            self.red_dog[1].pop(0)
            self.black_dog[0].pop(0)
            self.black_dog[1].pop(0)
    def add_target(self,target):
        self.target[0].append(target[0])
        self.target[1].append(target[1])
    def add_my_vel(self,vel):
        if C.COLOR == 0:
            self.red_dog_vel = vel
        else:
            self.black_dog_vel = vel
    def draw(self,location):
        self.ax.scatter(location.ball[0],location.ball[1],s=15,c='green')
        self.ax.scatter(location.red_dog[0],location.red_dog[1],s=15,c='red')
        self.ax.scatter(location.black_dog[0],location.black_dog[1],s=15,c='black')
        self.ax.plot(self.ball[0],self.ball[1],c='green')
        self.ax.plot(self.red_dog[0],self.red_dog[1],c='red')
        self.ax.plot(self.black_dog[0],self.black_dog[1],c='black')
        plt.show()
def main(args = None):
    record = Record()
    location = Location()
    move = move()
    for i in range(100):
        record.add_loc(location)
        record.add_my_vel(move)
        record.draw(location)
        
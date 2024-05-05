import rclpy
from rclpy.node import Node
from protocol.msg import MotionServoCmd
import time

class MoveNode(Node):
    def __init__(self, name, mode, t):
        super().__init__(name)
        self.speed_x, self.speed_y, self.speed_z = 0.0, 0.0, 0.0
        if mode == 0:
            self.speed_x = 0.5
        elif mode == 1:
            self.speed_y = 0.5
        elif mode == 2:
            self.speed_z = 0.5
        self.dog_name = "az"
        self.pub = self.create_publisher(MotionServoCmd, f"/{self.dog_name}/motion_servo_cmd", 10)
        self.timer = self.create_timer(0.1, self.timer_callback)
        self.end_time = time.time() + t

    def timer_callback(self):
        if time.time() > self.end_time:
            self.destroy_node()
            return
        msg = MotionServoCmd()
        msg.motion_id = 308
        msg.cmd_type = 1
        msg.value = 2
        msg.vel_des = [self.speed_x, self.speed_y, self.speed_z]
        msg.step_height = [0.05,0.05]
        self.pub.publish(msg)

def move_t_sec(t, mode):
    rclpy.init()
    move_node = MoveNode("move_node", mode, t)
    rclpy.spin(move_node)
    rclpy.shutdown()

def main():
    move_t_sec(1, 0)
if __name__ == "__main__":
   main()
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Range
from protocol.msg import MotionServoCmd

class transverse(Node):
    def __init__(self, name,num,v):
        super().__init__(name)
        self.speed_x, self.speed_y, self.speed_z = 0.0, v, 0.0
        self.dog_name = "az"
        self.pub = self.create_publisher(MotionServoCmd, f"/{self.dog_name}/motion_servo_cmd", 10)
        self.timer = self.create_timer(0.1, self.timer_callback)
        self.count=0
        self.num=num
    def timer_callback(self):
        msg = MotionServoCmd()
        msg.motion_id = 303
        if self.count > self.num:
            msg.cmd_type=2
        else:
            msg.cmd_type = 1
        msg.value = 2
        msg.vel_des = [self.speed_x, self.speed_y, self.speed_z]
        msg.step_height = [0.05,0.05]
        self.pub.publish(msg)
        self.count +=1
        self.get_logger().info(f"transverse,count={self.count},speed_y={self.speed_y}.")

def transverse(num,v):
    rclpy.init()
    move_node = transverse("transverse", num,v)
    for i in range(num):
    rclpy.spin_once(move_node)
    move_node.destroy_node()
    rclpy.shutdown()

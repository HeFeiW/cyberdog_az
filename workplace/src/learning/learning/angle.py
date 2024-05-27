#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Imu
from transforms3d.euler import quat2euler

class ImuOrientationListener(Node):

    def __init__(self):
        super().__init__('imu_orientation_listener')
        self.subscription = self.create_subscription(
            Imu,
            '/camera/imu',
            self.listener_callback,
            10)
        self.subscription  # prevent unused variable warning

    def listener_callback(self, msg):
        quaternion = (msg.orientation.x, msg.orientation.y, msg.orientation.z, msg.orientation.w)
        # 将四元数转换为欧拉角（以弧度为单位）
        euler_angles = quat2euler(quaternion)
        self.get_logger().info(f"Received IMU orientation in Euler angles: ({euler_angles[0]}, {euler_angles[1]}, {euler_angles[2]})")

def main(args=None):
    rclpy.init(args=args)
    imu_orientation_listener = ImuOrientationListener()
    rclpy.spin(imu_orientation_listener)
    imu_orientation_listener.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()

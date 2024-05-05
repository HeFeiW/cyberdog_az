#---get ros2 msg info of the sensor---#

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image



class rgb_suber(Node):
      '''subscribe the message of sensor'''
      def __init__(self, name) -> None:
          super().__init__(name)

          self.declare_parameter("dog_name", "az")

          dog_name = self.get_parameter("dog_name").get_parameter_value().string_value

          self.sub = self.create_subscription(Image, '/image_rgb', self.sub_callback, 10)
          pass

      def sub_callback(self, msg: Image):
          '''the callback function of subscriber'''
          width = msg.width
          self.get_logger().info(f"the width is {width}")

def main(args=None):
    rclpy.init(args=args)
    node = rgb_suber("my_sensor")
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()
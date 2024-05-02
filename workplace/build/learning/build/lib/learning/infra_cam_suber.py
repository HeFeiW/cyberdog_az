#---get image from infra camera---#

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image


class infra_cam_suber(Node):
      '''subscribe the message of infra camera'''
      def __init__(self, name) -> None:
          super().__init__(name)

          self.declare_parameter("dog_name", "az")
          self.sub = self.create_subscription(Image, '/camera/infra2/image_rect_raw', self.sub_callback, 10)
          pass

      def sub_callback(self, msg: Image):
          '''the callback function of subscriber'''
          infra_msg =msg.data
          self.get_logger().info(f"the distance is {infra_msg}")

def main(args=None):
    rclpy.init(args=args)
    node = infra_cam_suber("infra_cam_suber")
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()
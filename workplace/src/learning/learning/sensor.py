import rclpy
from rclpy.node import Node
from std_msgs.msg import String
class MyNodePublisher(Node):
    def __init__(self):
        super().__init__('ultrasonic_pub')
        print("Hello ROS2 world! This is ultrasonic_pub")
        self.publisher = self.create_publisher(String, '/ultrasonic', 10)
        timer_period = 0.5
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.count = 0
        return
    def timer_callback(self):
        msg = String()
        msg.data = "Another one {} bites the dust...".format(self.count)
        self.publisher.publish(msg)
        self.get_logger().info('Publishing: "%s"' % msg.data)
        self.count += 1
        return
def main(args = None):
    rclpy.init(args = args)
    my_node_pub = MyNodePublisher()
    rclpy.spin(my_node_pub)
    my_node_pub.destroy_node()
    rclpy.shutdown()
if __name__ == "__main__":
    main()
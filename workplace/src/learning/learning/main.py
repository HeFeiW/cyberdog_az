# if __name__ = '__main__':
#     main()
# def main(args=None):
#     rclpy.init(args=None)
#     rgb_node = rgb_cam_suber("rgb_cam_suber")
#     rotate_node = basic_rotate("rotate_node", rgb_node)
#     rclpy.spin(rgb_node)
#     rclpy.spin(rotate_node)
#     rotate_node.destroy_node()
#     rgb_node.destroy_node()
#     rclpy.shutdown()
#     cv2.destroyAllWindows()

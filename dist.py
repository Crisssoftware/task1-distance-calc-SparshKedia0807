import rclpy
from rclpy.node import Node
from turtlesim.msg import Pose
from std_msgs.msg import Float32
import math

class DistancePublisher(Node):
    def __init__(self):
        super().__init__('distance_publisher')
        self.subscription = self.create_subscription(
            Pose,
            '/turtle1/pose',
            self.pose_callback,
            10
        )
        self.publisher = self.create_publisher(Float32, '/turtle1/distance_from_origin', 10)
        self.timer = self.create_timer(0.1, self.publish_distance)
        self.current_pose = None

    def pose_callback(self, msg):
        self.current_pose = msg

    def publish_distance(self):
        if self.current_pose is not None:
            distance = math.sqrt(self.current_pose.x**2 + self.current_pose.y**2)
            msg = Float32()
            msg.data = distance
            self.publisher.publish(msg)
            self.get_logger().info(f'Distance from origin: {distance:.2f}')

def main(args=None):
    rclpy.init(args=args)
    distance_publisher = DistancePublisher()
    rclpy.spin(distance_publisher)
    distance_publisher.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()

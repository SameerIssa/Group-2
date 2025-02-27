"""
Pure Pursuit Node for Autonomous Vehicle Steering

This script implements the Pure Pursuit algorithm for autonomous vehicle path tracking using Odometry data. 
The node subscribes to odometry data, processes waypoints, and publishes drive commands.

Classes:
    - PurePursuit: Implements the Pure Pursuit algorithm.

Functions:
    - main(): Initializes and runs the ROS2 node.
"""

import numpy as np
from scipy.spatial import distance, transform
import rclpy
from rclpy.node import Node
from ackermann_msgs.msg import AckermannDriveStamped
from nav_msgs.msg import Odometry

class PurePursuit(Node):
    """ 
    Pure Pursuit Algorithm for Autonomous Vehicles.
    
    This class subscribes to odometry data, processes waypoint tracking, 
    and publishes steering and speed commands to follow a given path.
    """
    def __init__(self):
        super().__init__('pure_pursuit_node')

        self.waypoint_asc = True  # Waypoint indices are ascending during tracking

        # Topics
        drive_topic = '/drive'
        odom_topic = '/ego_racecar/odom'

        # Subscribers
        self.create_subscription(Odometry, odom_topic, self.odom_callback, 1)

        # Publishers
        self.publish_to_drive = self.create_publisher(AckermannDriveStamped, drive_topic, 1)
        self.drive_msg = AckermannDriveStamped()

        # Load waypoints
        self.declare_parameter('path', '/sim_ws/src/pure_pursuit/logs/waypoints.csv')
        self.file = self.get_parameter('path').get_parameter_value().string_value

        csv_data = np.loadtxt(self.file, delimiter=',', skiprows=1)
        self.waypoints = csv_data[:, [1, 2, 3, 4]]
        self.numWaypoints = self.waypoints.shape[0]
        
        # Control parameters
        self.speed = 0.9
        self.lookahead = 0.6
        self.max_turn_angle = 0.5

    def odom_callback(self, odom_msg):
        """Processes odometry data and computes steering and speed commands."""
        self.current_x = odom_msg.pose.pose.position.x
        self.current_y = odom_msg.pose.pose.position.y
        self.current_position = np.array([self.current_x, self.current_y]).reshape((1, 2))

        # Convert quaternion to rotation matrix
        quat = odom_msg.pose.pose.orientation
        quat = [quat.x, quat.y, quat.z, quat.w]
        R = transform.Rotation.from_quat(quat)
        self.rot = R.as_matrix()

        # Find the closest waypoint
        self.car_dist = distance.cdist(self.current_position, self.waypoints[:, :2], 'euclidean').reshape((self.numWaypoints))
        self.closest_index = np.argmin(self.car_dist)
        self.closestPoint = self.waypoints[self.closest_index]

        # Find target waypoint beyond lookahead distance
        target = self.get_closest_point_beyond_lookahead_dist(self.lookahead)
        trans_target_point = self.translatePoint(target[:2])
        
        # Compute steering angle
        y = trans_target_point[1]
        gamma = self.max_turn_angle * (2 * y / self.lookahead**2)
        gamma = np.clip(gamma, -0.35, 0.35)
        
        # Publish drive message
        self.drive_msg.drive.steering_angle = gamma
        self.drive_msg.drive.speed = self.speed
        self.publish_to_drive.publish(self.drive_msg)

    def get_closest_point_beyond_lookahead_dist(self, threshold):
        """Finds the first waypoint beyond the specified lookahead distance."""
        current_index = self.closest_index
        dist = self.car_dist[current_index]
        
        while dist < threshold:
            current_index = (current_index + 1) % len(self.waypoints) if self.waypoint_asc else (current_index - 1) % len(self.waypoints)
            dist = self.car_dist[current_index]

        return self.waypoints[current_index]

    def translatePoint(self, target):
        """Transforms a target point into the car's coordinate frame."""
        H = np.eye(4)
        H[0:3, 0:3] = np.linalg.inv(self.rot)
        H[0, 3] = self.current_x
        H[1, 3] = self.current_y
        pvect = target - self.current_position
        convertedTarget = (H @ np.array([pvect[0, 0], pvect[0, 1], 0, 0])).reshape((4))
        return convertedTarget

def main(args=None):
    """Initializes and runs the Pure Pursuit ROS2 node."""
    rclpy.init(args=args)
    print("PurePursuit Initialized")
    
    pure_pursuit_node = PurePursuit()
    rclpy.spin(pure_pursuit_node)

    pure_pursuit_node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()

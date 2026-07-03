#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from std_msgs.msg import String, Bool
from geometry_msgs.msg import Twist

class RobotController(Node):
    """
    Generic assistive robot controller node.
    Subscribes to movement commands and applies safety parameter constraints.
    """
    def __init__(self):
        super().__init__('robot_controller')
        
        # ROS2 Parameter declarations for safety limits
        self.declare_parameter('max_speed', 0.5)  # m/s
        self.declare_parameter('max_acceleration', 0.2)  # m/s^2
        self.declare_parameter('human_proximity_threshold', 1.0)  # meters
        self.declare_parameter('emergency_stop_enabled', True)
        
        # Read parameters
        self.max_speed = self.get_parameter('max_speed').value
        self.max_acceleration = self.get_parameter('max_acceleration').value
        self.proximity_threshold = self.get_parameter('human_proximity_threshold').value
        self.estop = self.get_parameter('emergency_stop_enabled').value

        self.get_logger().info("Initialized Assistive Robot Controller with safety limits:")
        self.get_logger().info(f" - Max Speed: {self.max_speed} m/s")
        self.get_logger().info(f" - Max Acceleration: {self.max_acceleration} m/s^2")
        self.get_logger().info(f" - Proximity Threshold: {self.proximity_threshold} m")
        self.get_logger().info(f" - Emergency Stop Enabled: {self.estop}")

        # Publishers
        self.cmd_vel_pub = self.create_publisher(Twist, 'cmd_vel', 10)
        self.safety_status_pub = self.create_publisher(Bool, 'safety_status', 10)

        # Subscribers
        self.telemetry_sub = self.create_subscription(Twist, 'telemetry', self.telemetry_callback, 10)
        self.estop_sub = self.create_subscription(Bool, 'estop_trigger', self.estop_callback, 10)

        # Simulation timer to publish status (simulating MQTT updates)
        self.create_timer(1.0, self.status_timer_callback)

    def telemetry_callback(self, msg):
        """
        Processes telemetry command velocity message and enforces kinematic limits.
        """
        safe_msg = Twist()
        if self.estop:
            self.get_logger().warn("Emergency Stop active. Commands ignored.")
            safe_msg.linear.x = 0.0
            safe_msg.angular.z = 0.0
        else:
            # Enforce max speed limit
            speed = msg.linear.x
            if abs(speed) > self.max_speed:
                speed = self.max_speed if speed > 0 else -self.max_speed
                self.get_logger().warn(f"Speed command exceeded max limit. Capped to {speed} m/s.")
            safe_msg.linear.x = speed
            safe_msg.angular.z = msg.angular.z

        self.cmd_vel_pub.publish(safe_msg)

    def estop_callback(self, msg):
        """
        Updates the emergency stop state when triggered by external input.
        """
        self.estop = msg.data
        self.get_logger().warn(f"Emergency stop status changed: {self.estop}")
        status_bool = Bool()
        status_bool.data = not self.estop
        self.safety_status_pub.publish(status_bool)

    def status_timer_callback(self):
        """
        Simulated heartbeat timer callback.
        """
        self.get_logger().debug("Publishing status heartbeat...")

def main(args=None):
    rclpy.init(args=args)
    node = RobotController()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()

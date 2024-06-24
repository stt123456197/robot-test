#!/usr/bin/env python3

import rospy
from std_msgs.msg import String
from geometry_msgs.msg import Twist
from gazebo_msgs.msg import ModelState
from gazebo_msgs.srv import GetModelState
import random

class RobotSimulation:
    def __init__(self):
        rospy.init_node('robot_simulation_node', anonymous=True)
        self.rate = rospy.Rate(5)  # 5 Hz
        self.robot_state_pub = rospy.Publisher('/gazebo/set_model_state', ModelState, queue_size=10)
        self.get_model_state = rospy.ServiceProxy('/gazebo/get_model_state', GetModelState)
        rospy.Subscriber('/cmd_vel', Twist, self.cmd_vel_callback)
        
        self.robot_name = 'robot'
        self.obstacles = [(3, 5), (7, 8), (2, 1)]
        
        self.robot_state = ModelState()
        self.robot_state.model_name = self.robot_name
        self.robot_state.pose.position.x = 0.0
        self.robot_state.pose.position.y = 0.0
        self.robot_state.pose.position.z = 0.0
        self.robot_state.pose.orientation.x = 0.0
        self.robot_state.pose.orientation.y = 0.0
        self.robot_state.pose.orientation.z = 0.0
        self.robot_state.pose.orientation.w = 1.0
        
        self.directions = ['up', 'down', 'left', 'right']
        self.current_direction = random.choice(self.directions)
    
    def move_robot(self):
        if self.current_direction == 'right':
            if self.robot_state.pose.position.x < 9.0:
                self.robot_state.pose.position.x += 1.0
            else:
                self.current_direction = 'left'
        elif self.current_direction == 'left':
            if self.robot_state.pose.position.x > 0.0:
                self.robot_state.pose.position.x -= 1.0
            else:
                self.current_direction = 'right'
        elif self.current_direction == 'up':
            if self.robot_state.pose.position.y < 9.0:
                self.robot_state.pose.position.y += 1.0
            else:
                self.current_direction = 'down'
        elif self.current_direction == 'down':
            if self.robot_state.pose.position.y > 0.0:
                self.robot_state.pose.position.y -= 1.0
            else:
                self.current_direction = 'up'
        
        # Check for obstacles
        if (round(self.robot_state.pose.position.x), round(self.robot_state.pose.position.y)) in self.obstacles:
            rospy.loginfo("Encountered obstacle at position ({}, {}). Changing direction.".format(
                round(self.robot_state.pose.position.x), round(self.robot_state.pose.position.y)))
            self.current_direction = random.choice(self.directions)
        
        # Publish robot state
        self.robot_state_pub.publish(self.robot_state)
    
    def cmd_vel_callback(self, data):
        # Placeholder for future implementation
        pass
    
    def run(self):
        while not rospy.is_shutdown():
            self.move_robot()
            self.rate.sleep()

if __name__ == '__main__':
    try:
        rs = RobotSimulation()
        rs.run()
    except rospy.ROSInterruptException:
        pass
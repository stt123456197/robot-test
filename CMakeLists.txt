cmake_minimum_required(VERSION 2.8.3)
project(robot_simulation)

find_package(catkin REQUIRED COMPONENTS
  roscpp
  rospy
  std_msgs
  gazebo_msgs
)

catkin_python_setup()

catkin_package()

install(PROGRAMS
  scripts/robot_simulation_node.py
  DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)
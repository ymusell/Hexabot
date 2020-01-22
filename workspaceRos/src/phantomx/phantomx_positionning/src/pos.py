#!/usr/bin/env python
# -*- coding: utf-8 -*-

import rospy
from sensor_msgs.msg import Imu
from tf.transformations import euler_from_quaternion
from geometry_msgs.msg import Point, Pose, Quaternion, Twist, Vector3

def get_rotation (msg):
    global roll, pitch, yaw
    orientation_q = msg.pose.pose.orientation
    orientation_list = [orientation_q.x, orientation_q.y, orientation_q.z, orientation_q.w]
    (roll, pitch, yaw) = euler_from_quaternion (orientation_list)
    print yaw

rospy.init_node('quaternion_to_euler')

sub = rospy.Subscriber ('/imu', Imu, get_rotation)

r = rospy.Rate(1)
while not rospy.is_shutdown():
    r.sleep()
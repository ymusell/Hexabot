#!/usr/bin/env python2


import numpy as np
import rospy
from nav_msgs.msg import OccupancyGrid
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Point
import tf
import tf2_ros
from geometry_msgs.msg import TransformStamped


pos_x = -10
pos_y = -10
heading = 0
pitch = 0
roll = 0


check_position = 0 #check if we have new data for position and orientation
check_orientation = 0

lidar = LaserScan()

def sub_lidar(msg):
    global lidar
    if (roll < 0.1 and pitch < 0.1):
        lidar = msg
        pub_lidar.publish(lidar)

def sub_position(msg):
    global pos_x, pos_y, check_position
    if ( abs(pos_x - msg.x) > 0.01):
        pos_x = msg.x
        pos_y = msg.y
        check_position = 1


def sub_orientation(msg):
    global roll, pitch, heading, check_orientation
    if ( abs(heading - msg.z) > 0.001):
        heading = msg.z
        roll = msg.x
        pitch = msg.y
        check_orientation = 1

if __name__ == "__main__":


    rospy.init_node("filtreLidar")
    pub_lidar = rospy.Publisher("phantomx/scan_filtre",LaserScan,queue_size=1)
    rospy.Subscriber("/phantomx/scan",LaserScan,sub_lidar)
    rospy.Subscriber("/vect_position",Point,sub_position)
    rospy.Subscriber("/vect_orientation",Point,sub_orientation)

    #br = tf2_ros.StaticTransformBroadcaster()
    #transformStamped = TransformStamped()

    #transformStamped.child_frame_id = "base_link"
    #transformStamped.header.frame_id = "base_stabilized"


    rate = rospy.Rate(25)
    while not rospy.is_shutdown():
        #if ( (check_orientation or check_position)):
        '''
        q = tf.transformations.quaternion_from_euler(0,0,heading)
        transformStamped.header.stamp = rospy.get_rostime()
        transformStamped.transform.translation.x = pos_x
        transformStamped.transform.translation.y = pos_y
        transformStamped.transform.rotation.x = q[0]
        transformStamped.transform.rotation.y = q[1]
        transformStamped.transform.rotation.z = q[2]
        transformStamped.transform.rotation.w = q[3]


        br.sendTransform(transformStamped)


        check_orientation = 0
        check_position = 0
        '''

        rate.sleep()

#!/usr/bin/env python2

'''

    Auteur : Corentin JEGAT
    Date : 08/01/2020
    Description : Visualize camera

'''

import numpy as np
import matplotlib.pyplot as plt
import time

import cv2
from cv_bridge import CvBridge, CvBridgeError

import rospy
#from std_msgs.msg import Float32
from geometry_msgs.msg import Vector3
from sensor_msgs.msg import PointCloud2
from sensor_msgs.msg import Image


##############################################################################################
#      ROS
##############################################################################################

def sub_image_depth(data):
    global depth_image
    depth_image = bridge.imgmsg_to_cv2(data, desired_encoding="passthrough")

def sub_image_rgb(data):
    global rgb_image, height, width
    rgb_image = bridge.imgmsg_to_cv2(data, desired_encoding="passthrough")
    height, width = data.height, data.width


##############################################################################################
#      Other functions
##############################################################################################



##############################################################################################
#      Main
##############################################################################################

if __name__ == '__main__':

    bridge = CvBridge()
    depth_image = None
    rgb_image = None
    height, width = None, None

    pub_relevent_points = rospy.Publisher('relevent_points', Vector3, queue_size=10)
    relevent_points_msg = Vector3()
    rospy.Subscriber("/camera/depth/image_raw", Image, sub_image_depth)
    rospy.Subscriber("/camera/rgb/image_raw", Image, sub_image_rgb)

    node_name = 'visualize_camera'
    rospy.init_node(node_name)
    rospy.loginfo("{} is launched".format(node_name))
    rate = rospy.Rate(10) # 10hz



    while not rospy.is_shutdown():

        plt.subplot('121')
        plt.imshow(rgb_image)
        plt.subplot('122')
        plt.imshow(depth_image)
        plt.pause(0.01)
        #np.save('rgb', rgb_image)
        #np.save('depth', depth_image)

        rate.sleep()
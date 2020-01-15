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
from visualization_msgs.msg import Marker
from sensor_msgs.msg import PointCloud2
from sensor_msgs.msg import Image
from tf.transformations import quaternion_from_euler

from camera_lib import *
from id_on_test_images import *


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

def waiting_ros_camera():
    global depth_image, rgb_image, height, width
    rgb_image = np.load('rgb.npy')
    depth_image = np.load('depth.npy')
    height, width = rgb_image.shape[0], rgb_image.shape[1]


##############################################################################################
#      Main
##############################################################################################

if __name__ == '__main__':

    bridge = CvBridge()
    depth_image = None
    rgb_image = None
    height, width = None, None

    rospy.Subscriber("/camera/depth/image_raw", Image, sub_image_depth)
    rospy.Subscriber("/camera/rgb/image_raw", Image, sub_image_rgb)

    pub_fissure = rospy.Publisher('current_fissure', Marker, queue_size=10)

    node_name = 'visualize_camera'
    rospy.init_node(node_name)
    rospy.loginfo("{} is launched".format(node_name))
    rate = rospy.Rate(2) # 10hz

    marker_fissure = Marker()
    marker_fissure.header.frame_id = 'MP_BODY'
    """
    marker_fissure.pose.position.x = 0
    marker_fissure.pose.position.y = 0
    marker_fissure.pose.position.z = 0
    """
    marker_fissure.header.stamp = rospy.get_rostime()
    #marker_fissure.ns = 'ns_'+'test'
    marker_fissure.id = 0
    marker_fissure.action = 0
    marker_fissure.type = 4
    q = quaternion_from_euler(0,0,0)
    marker_fissure.pose.orientation.x = q[0]
    marker_fissure.pose.orientation.y = q[1]
    marker_fissure.pose.orientation.z = q[2]
    marker_fissure.pose.orientation.w = q[3]

    marker_fissure.scale.x = 0.05
    marker_fissure.color.r = 1
    marker_fissure.color.g = 0
    marker_fissure.color.b = 0
    marker_fissure.color.a = 1.0

    grid = create_grid()
    
    

    while not rospy.is_shutdown():

        binary_image = rgb_fissure_to_binary(rgb_image, grid)
        print(np.sum(binary_image))
        x,y,z = binary_image_to_xyz(binary_image, depth_image)
        plt.subplot('121')
        plt.imshow(rgb_image)
        plt.subplot('122')
        plt.imshow(binary_image)
        plt.pause(0.01)
        publish_point_fissure(pub_fissure, marker_fissure, x,y,z)
        
        #np.save('rgb', rgb_image)
        #np.save('depth', depth_image)

        rate.sleep()
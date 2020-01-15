#!/usr/bin/env python2

'''

    Auteur : Corentin JEGAT
    Date : 08/01/2020
    Description : Visualize camera

'''

import numpy as np
import matplotlib.pyplot as plt
import time

import rospy
from visualization_msgs.msg import Marker
from tf.transformations import quaternion_from_euler

##############################################################################################
#      ROS
##############################################################################################

def sub_marker_fissures(data):
    l_points = data.points
    x,y,z = [],[],[]
    for p in l_points:
        x.append(p.x)
        y.append(p.y)
        z.append(p.z)
    print(np.std(x),np.std(y),np.std(z))


##############################################################################################
#      Other functions
##############################################################################################



##############################################################################################
#      Main
##############################################################################################

if __name__ == '__main__':


    rospy.Subscriber("current_fissure", Marker, sub_marker_fissures)

    node_name = 'sort_fissures'
    rospy.init_node(node_name)
    rospy.loginfo("{} is launched".format(node_name))
    rate = rospy.Rate(10) # 10hz

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
    marker_fissure.type = 8
    q = quaternion_from_euler(0,0,0)
    marker_fissure.pose.orientation.x = q[0]
    marker_fissure.pose.orientation.y = q[1]
    marker_fissure.pose.orientation.z = q[2]
    marker_fissure.pose.orientation.w = q[3]

    marker_fissure.scale.x = 0.05
    marker_fissure.scale.y = 0.05
    marker_fissure.color.r = 1
    marker_fissure.color.g = 0
    marker_fissure.color.b = 0
    marker_fissure.color.a = 1.0

    while not rospy.is_shutdown():

        rate.sleep()
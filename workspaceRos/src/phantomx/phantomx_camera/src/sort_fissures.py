#!/usr/bin/env python2

'''

    Auteur : Corentin JEGAT
    Date : 08/01/2020
    Description : Visualize camera

'''

import numpy as np
import matplotlib.pyplot as plt

import rospy
from visualization_msgs.msg import Marker
from geometry_msgs.msg import Point
from tf.transformations import quaternion_from_euler
from scipy.spatial.transform import Rotation as R

##############################################################################################
#      ROS
##############################################################################################

def sub_marker_fissures(data):
    global nb_fissure_prec, nb_fissure, marker_global, pub_fissure
    global long_fissure, prev_center, list_fissures, prev_points

    l_points = data.points
    x,y,z = [],[],[]
    for p in l_points:
        x.append(p.x)
        y.append(p.y)
        z.append(p.z)
    
    """
    if x != []:
        sx,sy,sz = np.std(x),np.std(y),np.std(z)
        list_nan = list_nan[1:] + [sx]
    else:
        list_nan = list_nan[1:] + [False]

    new_flag_full_nan = flag_state(list_nan, flag_full_nan)
    if new_flag_full_nan == False and flag_full_nan == True:
        nb_fissure+=1

    flag_full_nan = new_flag_full_nan
    """

    if x_rob != None:
        nx = np.array(x) + x_rob
        ny = np.array(y) + y_rob
        nz = np.array(z) + z_rob

        r = R.from_euler('zxy', [yaw,roll,pitch]).as_dcm()
        n_pos = np.concatenate(([x],[y],[z]), axis=0)
        n_pos = np.matmul(r,n_pos)+np.array([[x_rob],[y_rob],[z_rob]])

        center = np.mean(n_pos,axis = 1)
        dist = np.sum(np.abs(prev_center-center))

        if dist > 10:
            nb_fissure += 1
            if nb_fissure>1:
                long_fissure = 0
                if (nb_fissure_prec != nb_fissure):
                    list_fissures += prev_points

        if n_pos.shape[1] > long_fissure:
            prev_points = []
            for i in range(n_pos.shape[1]):
                p = Point()
                p.x = n_pos[0,i]
                p.y = n_pos[1,i]
                p.z = n_pos[2,i]
                prev_points.append(p)
            marker_global.points = prev_points + list_fissures
            pub_fissure.publish(marker_global)

            long_fissure = n_pos.shape[1]
            #rospy.loginfo("New fissure"+str(long_fissure))

        nb_fissure_prec = nb_fissure
        #print(dist,nb_fissure,len(list_fissures))
        prev_center = center


def sub_position(data):
    global x_rob, y_rob, z_rob
    x_rob = data.x
    y_rob = data.y
    z_rob = data.z

def sub_orientation(data):
    global roll, pitch, yaw
    roll = data.x
    pitch = data.y
    yaw = data.z


##############################################################################################
#      Other functions
##############################################################################################

def flag_state(list_nan, flag_full_nan):
    if flag_full_nan == True and not(False) in list_nan:
        return False
    elif np.sum(np.abs(list_nan)) == 0:
        return True
    else:
        return flag_full_nan

##############################################################################################
#      Main
##############################################################################################

if __name__ == '__main__':

    x_rob, y_rob, z_rob = None, None, None
    roll, pitch, yaw = None, None, None

    node_name = 'sort_fissures'
    rospy.init_node(node_name)
    rospy.loginfo("{} is launched".format(node_name))
    rate = rospy.Rate(10) # 10hz

    rospy.Subscriber("current_fissure", Marker, sub_marker_fissures)
    rospy.Subscriber("vect_position", Point, sub_position)
    rospy.Subscriber("vect_orientation", Point, sub_orientation)
    pub_fissure = rospy.Publisher('global_fissure', Marker, queue_size=10)


    marker_fissure = Marker()
    marker_fissure.header.frame_id = 'MP_BODY'
    marker_fissure.header.stamp = rospy.get_rostime()
    marker_fissure.id = 0
    marker_fissure.action = 0
    marker_fissure.type = 8

    marker_global = Marker()
    marker_global.header.frame_id = 'base_link'
    marker_global.header.stamp = rospy.get_rostime()
    marker_global.id = 0
    marker_global.action = 0
    marker_global.type = 8
    marker_global.color.r = 0
    marker_global.color.g = 0
    marker_global.color.b = 1
    marker_global.color.a = 1.0
    marker_global.scale.x = 0.08
    marker_global.scale.y = 0.08

    #nb_nan = 5
    #list_nan = [False]*nb_nan
    nb_fissure = 0
    nb_fissure_prec = 0
    prev_center = np.array([[0],[0],[0]])

    long_fissure = 0
    list_fissures = []
    prev_points = []

    #flag_full_nan = True

    while not rospy.is_shutdown():

        rate.sleep()
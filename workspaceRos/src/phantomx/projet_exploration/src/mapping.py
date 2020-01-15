#!/usr/bin/env python2

import numpy as np
import rospy
from nav_msgs.msg import OccupancyGrid
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Point

map_array = np.zeros((500,500))
map_array[:,:] = -1

angle_list = []
distance_list = []

pos_x = 0
pos_y = 0
cap_robot = 0

def mapping():
<<<<<<< HEAD
    global map_array, distance_list, angle_list, pos_x, pos_y
    print(pos_x,pos_y)
    for i in range (0,len(distance_list)):
        xWall = int(10*distance_list[i]*np.cos(angle_list[i])+250+10*pos_x)  # distance (m), grid (cm)
        yWall = int(10*distance_list[i]*np.sin(angle_list[i])+250+10*pos_y)
        map_array[yWall,xWall] = 100
=======
	global map_array, distance_list, angle_list
	for i in range (0,len(distance_list)):
                xWall = int(10*distance_list[i]*np.cos(angle_list[i]))+250+pos_x  # distance (m), grid (cm)
                yWall = int(10*distance_list[i]*np.sin(angle_list[i]))+250+pos_y
                map_array[yWall,xWall] = 100

                rangeEmpty = np.arange(0,distance_list[i]-0.1,0.1)
                for j in range(0,len(rangeEmpty)):
                    xEmpty = int(10*rangeEmpty[j]*np.cos(angle_list[i])+250+pos_x)
                    yEmpty = int(10*rangeEmpty[j]*np.sin(angle_list[i])+250+pos_y)
                    if map_array[yEmpty,xEmpty] == -1:
                        map_array[yEmpty,xEmpty] = 0

>>>>>>> 7bc4fc7fb81fa4c1f6cf3be97ff2cb8c9dfc0f90

        rangeEmpty = np.arange(0,distance_list[i]-0.1,0.1)
        for j in range(0,len(rangeEmpty)):
            xEmpty = int(10*rangeEmpty[j]*np.cos(angle_list[i])+250+10*pos_x)
            yEmpty = int(10*rangeEmpty[j]*np.sin(angle_list[i])+250+10*pos_y)
            if map_array[yEmpty,xEmpty] == -1:
                map_array[yEmpty,xEmpty] = 0



def publishMap(pub_map,msg_map):
    global map_array
    msg_map.info.origin.position.x = -25- pos_x
    msg_map.info.origin.position.y = -25- pos_y
    msg_map.data = map_array.flatten()
    pub_map.publish(msg_map)


def sub_lidar(msg):
    global angle_list, distance_list
    distance_list = msg.ranges
    angle_list = np.arange(msg.angle_min-cap_robot,msg.angle_max-cap_robot,msg.angle_increment)

def sub_position(msg):
    global pos_x, pos_y
    pos_x = msg.x
    pos_y = msg.y

if __name__ == "__main__":
<<<<<<< HEAD
    rospy.init_node("mapping")

    pub_map = rospy.Publisher("/map",OccupancyGrid,queue_size=10)

    rospy.Subscriber("/phantomx/scan",LaserScan,sub_lidar)
    rospy.Subscriber("/vect_position",Point,sub_position)
    msg_map = OccupancyGrid()

    msg_map.header.frame_id = "base_link"
    msg_map.info.map_load_time = rospy.get_rostime()
    msg_map.info.resolution = 0.1
    msg_map.info.width  = 500
    msg_map.info.height = 500
    msg_map.info.origin.position.x = -25- pos_x
    msg_map.info.origin.position.y = -25- pos_y
    msg_map.info.origin.position.z = 0
    msg_map.info.origin.orientation.x = 0
    msg_map.info.origin.orientation.y = 0
    msg_map.info.origin.orientation.z = 0
    msg_map.info.origin.orientation.w = 0


    rate = rospy.Rate(2)
    while not rospy.is_shutdown():
        mapping()
        publishMap(pub_map,msg_map)
        rate.sleep()
=======
	rospy.init_node("mapping")

	rospy.Subscriber("/phantomx/scan",LaserScan,sub_lidar)
	pub_map = rospy.Publisher("/map",OccupancyGrid,queue_size=10)
	msg_map = OccupancyGrid()

	msg_map.header.frame_id = "base_link"
	msg_map.info.map_load_time = rospy.get_rostime()
	msg_map.info.resolution = 0.1
	msg_map.info.width  = 500
	msg_map.info.height = 500
	msg_map.info.origin.position.x = -25
	msg_map.info.origin.position.y = -25
	msg_map.info.origin.position.z = 0
	msg_map.info.origin.orientation.x = 0
	msg_map.info.origin.orientation.y = 0
	msg_map.info.origin.orientation.z = 0
	msg_map.info.origin.orientation.w = 0


	rate = rospy.Rate(5)
	while not rospy.is_shutdown():
		mapping()
		publishMap(pub_map,msg_map)
		rate.sleep()
>>>>>>> 7bc4fc7fb81fa4c1f6cf3be97ff2cb8c9dfc0f90

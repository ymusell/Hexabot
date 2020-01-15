#!/usr/bin/env python2

import numpy as np
import rospy
from nav_msgs.msg import OccupancyGrid
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Point
import tf
import tf2_ros
from geometry_msgs.msg import TransformStamped

map_array = np.zeros((500,500))
map_array[:,:] = -1

angle_list = []
distance_list = []

pos_x = -10
pos_y = -10
heading = 0


check_position = 0 #check if we have new data for position and orientation
check_orientation = 0
check_lidar = 0

def mapping():


 update mapping
    global map_array, distance_list, angle_list, pos_x, pos_y
    for i in range (0,len(distance_list)):
        xWall = int(10*distance_list[i]*np.cos(angle_list[i])+250+10*pos_x)  # distance (m), grid (cm)
        yWall = int(10*distance_list[i]*np.sin(angle_list[i])+250+10*pos_y)
        map_array[yWall,xWall] = 100

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

    update mapping

        rangeEmpty = np.arange(0,distance_list[i]-0.1,0.1)
        for j in range(0,len(rangeEmpty)):
            xEmpty = int(10*rangeEmpty[j]*np.cos(angle_list[i])+250+10*pos_x)
            yEmpty = int(10*rangeEmpty[j]*np.sin(angle_list[i])+250+10*pos_y)
            map_array[yEmpty,xEmpty] = 0



def publishMap(pub_map,msg_map):
    global map_array
    msg_map.header.stamp = rospy.get_rostime()
    msg_map.data = map_array.flatten()
    pub_map.publish(msg_map)


def sub_lidar(msg):
    global angle_list, distance_list, check_lidar
    distance_list = msg.ranges
    angle_list = np.arange(msg.angle_min+heading,msg.angle_max+heading,msg.angle_increment)
    check_lidar = 1

def sub_position(msg):
    global pos_x, pos_y, check_position
    if ( abs(pos_x - msg.x) > 0.01):
        pos_x = msg.x
        pos_y = msg.y
        check_position = 1


def sub_orientation(msg):
    global heading, check_orientation
    if ( abs(heading - msg.z) > 0.001):
        heading = msg.z
        check_orientation = 1



if __name__ == "__main__":

update mapping
    rospy.init_node("mapping")

    pub_map = rospy.Publisher("/map",OccupancyGrid,queue_size=10)

    rospy.Subscriber("/phantomx/scan",LaserScan,sub_lidar)
    rospy.Subscriber("/vect_position",Point,sub_position)
    rospy.Subscriber("/vect_orientation",Point,sub_orientation)
    msg_map = OccupancyGrid()

    msg_map.header.frame_id = "map"
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

    br = tf2_ros.StaticTransformBroadcaster()
    transformStamped = TransformStamped()

    transformStamped.child_frame_id = "base_link"
    transformStamped.header.frame_id = "map"

    rate = rospy.Rate(10)
    while not rospy.is_shutdown():
        if ( (check_orientation or check_position) and check_lidar):

            q = tf.transformations.quaternion_from_euler(0,0,heading)
            transformStamped.header.stamp = rospy.get_rostime()
            transformStamped.transform.translation.x = pos_x
            transformStamped.transform.translation.y = pos_y
            transformStamped.transform.rotation.x = q[0]
            transformStamped.transform.rotation.y = q[1]
            transformStamped.transform.rotation.z = q[2]
            transformStamped.transform.rotation.w = q[3]


            br.sendTransform(transformStamped)


            mapping()
            check_orientation = 0
            check_position = 0
            check_lidar = 0
        publishMap(pub_map,msg_map)
        rate.sleep()
update mapping
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

        update mapping
        update mapping

#include "ros/ros.h"
#include "geometry_msgs/Vector3.h"
#include "geometry_msgs/Quaternion.h"
#include "tf/transform_datatypes.h"
#include <tf/LinearMath/Matrix3x3.h>
#include "std_msgs/String.h"
#include "geometry_msgs/PoseStamped.h"
#include "geometry_msgs/Pose.h"
#include "geometry_msgs/PoseWithCovariance.h"
#include "nav_msgs/Odometry.h"
#include "tf/tf.h"
#include "std_msgs/Float64.h"
#include <stdio.h>
#include <sstream>
#include <stdlib.h>
#include <cmath>
#include "sensor_msgs/Imu.h"
#include "geometry_msgs/Twist.h"
#include "gazebo_msgs/ModelStates.h"
#include "nav_msgs/Odometry.h"

ros::Publisher rpy_publisher;
ros::Subscriber quat_subscriber;

void MsgCallback(const geometry_msgs::Quaternion msg)
{
    tf::Quaternion quat;
    tf::quaternionMsgToTF(msg, quat);

    double roll, pitch, yaw;
    tf::Matrix3x3(quat).getRPY(roll, pitch, yaw);

    geometry_msgs::Vector3 rpy;
    rpy.x = roll;
    rpy.y = pitch;
    rpy.z = yaw;

    rpy_publisher.publish(rpy);
    ROS_INFO("published rpy angles: roll=%f pitch=%f yaw=%f", rpy.x, rpy.y, rpy.z);
}

int main(int argc, char **argv)
{
    ros::init(argc, argv, "phantomx_positioning");
    ros::NodeHandle n;

    rpy_publisher = n.advertise<geometry_msgs::Vector3>("/rpy_angles", 1000);
    quat_subscriber = n.subscribe("/phantomx/imu", 1000, MsgCallback);

    ros::Rate loop_rate(5);	
    // Boucle tant que le master existe (ros::ok())
    while (ros::ok()){
	    ros::spinOnce();
	    loop_rate.sleep();
	    }
    return 0;
}

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

geometry_msgs::Quaternion orien ;
geometry_msgs::Point orientation ;
geometry_msgs::Point position ;

geometry_msgs::Point ToEulerAngles(const geometry_msgs::Quaternion msg)
{
    tf::Quaternion quat;
    tf::quaternionMsgToTF(msg, quat);

    double roll, pitch, yaw;
    tf::Matrix3x3(quat).getRPY(roll, pitch, yaw);

    geometry_msgs::Point angles;
    angles.x = roll;
    angles.y = pitch;
    angles.z = yaw;

    return angles;
}

void MsgCallback(const sensor_msgs::Imu::ConstPtr& msg)
{
        orien = msg->orientation;
        ROS_INFO("Positionning Node is running");
}

void chatterCallback(const nav_msgs::Odometry &msg)
{
    position = msg.pose.pose.position;

}

int main(int argc, char **argv)
{
    ros::init(argc, argv, "phantomx_positioning");
    ros::NodeHandle n;

    ros::Publisher orientation_pub = n.advertise<geometry_msgs::Point>("/vect_orientation", 1);
    ros::Publisher position_pub = n.advertise<geometry_msgs::Point>("/vect_position", 1);

    ros::Subscriber quat_subscriber = n.subscribe("/phantomx/imu", 1, MsgCallback);
    ros::Subscriber sub = n.subscribe("ground_truth/state", 1, chatterCallback);

    ros::Rate loop_rate(25); 
    // Boucle tant que le master existe (ros::ok())
    while (ros::ok()){
    	orientation = ToEulerAngles(orien) ;
        
    	position_pub.publish(position);
    	orientation_pub.publish(orientation);
œ
    	ros::spinOnce();
    	loop_rate.sleep();
	}
    return 0;
}
#include "ros/ros.h"
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


double cosy_cosp ;
double siny_cosp ;
geometry_msgs::Quaternion orien ;
geometry_msgs::Vector3 speed ;
geometry_msgs::Point orientations ;
geometry_msgs::Point position ;



geometry_msgs::Point to_euler_angles(geometry_msgs::Quaternion q) {
    geometry_msgs::Point angles;

    // roll (x-axis rotation)
    double sinr_cosp = 2 * (q.w * q.x + q.y * q.z);
    double cosr_cosp = 1 - 2 * (q.x * q.x + q.y * q.y);
    angles.x = std::atan2(sinr_cosp, cosr_cosp);

    // pitch (y-axis rotation)
    double sinp = 2 * (q.w * q.y - q.z * q.x);
    if (std::abs(sinp) >= 1)
        angles.y = std::copysign(M_PI / 2, sinp); // use 90 degrees if out of range
    else
        angles.y = std::asin(sinp);

    // yaw (z-axis rotation)
    double siny_cosp = 2 * (q.w * q.z + q.x * q.y);
    double cosy_cosp = 1 - 2 * (q.y * q.y + q.z * q.z);
    angles.z = std::atan2(siny_cosp, cosy_cosp);

    return angles;
}

void chatter_callback(const sensor_msgs::Imu::ConstPtr& msg)
{
        orien = msg->orientation;
        ROS_INFO("Positionning Node is running");
        
}

void chatter_callback1(const nav_msgs::Odometry &msg)
{
    position = msg.pose.pose.position;

}



int main(int argc, char **argv)
{
  ros::init(argc, argv, "phantomx_positionning");

  ros::NodeHandle n;



  ros::Publisher orientation_pub = n.advertise<geometry_msgs::Point>("/vect_orientation", 1);  //Second argument changed to 1:
  ros::Publisher position_pub = n.advertise<geometry_msgs::Point>("/vect_position", 1);        //We always want the newest values.
  

  ros::Subscriber sub1 = n.subscribe("/phantomx/imu", 1, chatter_callback);
  ros::Subscriber sub = n.subscribe("ground_truth/state", 1, chatter_callback1);
  


  //ros::Publisher pub_speed = n.advertise<geometry_msgs::Point>("/vect_speed", 1000);

  ros::Rate loop_rate(25);

  while (ros::ok()){

    orientations = to_euler_angles(orien) ;


    //pub_speed.publish(speed);
    position_pub.publish(position);
    orientation_pub.publish(orientations);

    ros::spinOnce();
    loop_rate.sleep();
    }
return 0;

}





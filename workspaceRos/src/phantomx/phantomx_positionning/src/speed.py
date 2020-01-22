#!/usr/bin/env python2


import rospy
from std_msgs.msg import String
from integration import *
from sensor_msgs.msg import Imu
from geometry_msgs.msg import *

 
def publish_speed(pub, msg):
  pub.publish(msg)
   

def sub_acceleration(data):
  global x,y,z

  x = data.linear_acceleration.x
  y = data.linear_acceleration.y
  z = data.linear_acceleration.z 
     



    


if __name__ == '__main__':

  acceleration = []
  vitesse_init = 0. 
  delta_t = np.array([0.1,0.1,0.1])
  X,Y,Z = 0 , 0 , 0
  node_name = 'speed'
  rospy.init_node(node_name)
  rospy.loginfo("{} is launched".format(node_name))
  rate = rospy.Rate(10) # 10hz

  
  pub_speed = rospy.Publisher('linear_velocity', Point, queue_size=10)
  
  
  rospy.Subscriber("/phantomx/imu", Vector3, sub_acceleration)
  acceleration.append(X)
  acceleration.append(Y)
  acceleration.append(Z)
  vitesse = integration(acceleration,delta_t,vitesse_init)

  while not rospy.is_shutdown():
    
    


    


    msg = Point()
    msg.x = vitesse[0]
    msg.y = vitesse[1]
    msg.z = vitesse[2]


    publish_speed(pub_speed,msg)

    rate.sleep()
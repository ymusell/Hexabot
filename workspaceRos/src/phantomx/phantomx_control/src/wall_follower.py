#!/usr/bin/env python
import sys
import rospy

from phantomx_gazebo.phantomx import PhantomX

state_ = 0
state_dict_ = {
    0: 'turn right',
    1: 'turn left',
    2: 'go forward'
}

def change_state(state):
    global state_, state_dict_
    if state is not state_:
        #print 'Hexabot - [%s] - %s' % (state, state_dict_[state])
        state_ = state

def take_action():
    regions = regions_
    robot.set_walk_velocity(0, 0, 0)
    
    state_description = ''
    
    d = 2.
    
    if regions['right'] < 0.4:
        state_description = 'case 0 - right'
        change_state(1)
    elif regions['front'] > d and regions['fleft'] > d and regions['fright'] > d:
        state_description = 'case 1 - nothing'
        change_state(0)
    elif regions['front'] < d and regions['fleft'] > d and regions['fright'] > d:
        state_description = 'case 2 - front'
        change_state(1)
    elif regions['front'] > d and regions['fleft'] > d and regions['fright'] < d:
        state_description = 'case 3 - fright'
        change_state(2)
    elif regions['front'] > d and regions['fleft'] < d*1.5 and regions['fright'] > d:
        state_description = 'case 4 - fleft'
        change_state(0)
    elif regions['front'] < d and regions['fleft'] > d and regions['fright'] < d:
        state_description = 'case 5 - front and fright'
        change_state(1)
    elif regions['front'] < d and regions['fleft'] < d and regions['fright'] > d:
        state_description = 'case 6 - front and fleft'
        change_state(0)
    elif regions['front'] < d and regions['fleft'] < d and regions['fright'] < d:
        state_description = 'case 7 - front and fleft and fright'
        change_state(1)
    elif regions['front'] > d and regions['fleft'] < d and regions['fright'] < d:
        state_description = 'case 8 - fleft and fright'
        change_state(0)
    else:
        state_description = 'unknown case'
        rospy.loginfo(regions)

def turn_right():
    robot.set_walk_velocity(1, 0, -1)
    rospy.sleep(0.2)

def turn_left():
    robot.set_walk_velocity(0.5, 0, 0.5)
    rospy.sleep(0.2)

def go_forward():
    
    robot.set_walk_velocity(1, 0, 0)
    rospy.sleep(0.2)

if __name__ == '__main__':
    rospy.init_node('wall_follower')

    rospy.loginfo('Instantiating robot Client')
    robot = PhantomX()
    rospy.sleep(1)

    rospy.loginfo('Cave Exploration Starting')

    #print robot.lidar_ranges[180]                  #180=front, 270=left, 90=right

    while not rospy.is_shutdown():
        global regions_
        regions_ = {
            'left':  min(min(robot.lidar_ranges[700:720]), 10),
            'fleft': min(min(robot.lidar_ranges[380:700]), 10),
            'front':  min(min(robot.lidar_ranges[340:380]), 10),
            'fright':  min(min(robot.lidar_ranges[20:340]), 10),
            'right':   min(min(robot.lidar_ranges[0:20]), 10)
        }
        take_action()

        if state_ == 0:
            turn_right()
        elif state_ == 1:
            turn_left()
        elif state_ == 2:
            go_forward()
        else:
            rospy.logerr('Unknown state')

    rospy.loginfo('Cave Exploration Finished')

#!/usr/bin/env python
import sys
import rospy

from phantomx_gazebo.phantomx import PhantomX

state_ = 0
state_dict_ = {
    0: 'turn right',
    1: 'turn left',

    2: 'go forward',

    2: 'go forward'
add goal 3 (#34)
}

def change_state(state):
    global state_, state_dict_
    if state is not state_:
        print 'Hexabot - [%s] - %s' % (state, state_dict_[state])
        state_ = state

def take_action():
    regions = regions_
    robot.set_walk_velocity(0, 0, 0)
    
    state_description = ''
    

    #d=2.5
    d   = (regions['right']+regions['left'])
    dR = 0.5*(regions['right']+regions['left'])/2
    dL = (regions['right']+regions['left'])/2
    
    if regions['left'] < dL:
        state_description = 'case 0 - left'
        change_state(0)
    elif regions['right'] < dR:

    d = 2*regions['right']
    dRL = 0.5*(regions['right']+regions['left'])/2
    
    if regions['right'] < dRL:
    add goal 3 (#34)
        state_description = 'case 0 - right'
        change_state(1)
    elif regions['left'] < dRL:
        state_description = 'case 1 - left'
        change_state(0)
    elif regions['front'] > d and regions['fleft'] > d and regions['fright'] > d:
        state_description = 'case 2 - nothing'
        change_state(0)
    elif regions['front'] < d and regions['fleft'] > d and regions['fright'] > d:
        state_description = 'case 3 - front'
        change_state(1)
    elif regions['front'] > d and regions['fleft'] > d and regions['fright'] < d:
        state_description = 'case 4 - fright'
        change_state(2)
    elif regions['front'] > d and regions['fleft'] < d and regions['fright'] > d:
        state_description = 'case 5 - fleft'
        change_state(0)
    elif regions['front'] < d and regions['fleft'] > d and regions['fright'] < d:
        state_description = 'case 6 - front and fright'
        change_state(1)

    elif regions['front'] < d and regions['fleft'] < d*1.5 and regions['fright'] > d:
        state_description = 'case 6 - front and fleft'
        change_state(0)
    elif regions['front'] < d and regions['fleft'] < d and regions['fright'] < d*0.8:
        state_description = 'case 7 - front and fleft and fright'

    elif regions['front'] < d and regions['fleft'] < d and regions['fright'] > d:
        state_description = 'case 7 - front and fleft'
        change_state(1)
    elif regions['front'] < d and regions['fleft'] < d and regions['fright'] < d:
        state_description = 'case 8 - front and fleft and fright'
        add goal 3 (#34)
        change_state(1)
    elif regions['front'] > d and regions['fleft'] < d and regions['fright'] < d:
        state_description = 'case 9 - fleft and fright'
        change_state(0)
    else:
        state_description = 'unknown case'
        rospy.loginfo(regions)


def turn_right():
    robot.set_walk_velocity(0.7, 0, -0.5)

def find_wall():
    robot.set_walk_velocity(0.5, 0, -1)
add goal 3 (#34)
    rospy.sleep(0.2)

def turn_left():
    robot.set_walk_velocity(0.5, 0, 0.5)
    rospy.sleep(0.2)

def go_forward():
    
    robot.set_walk_velocity(1, 0, 0)
    rospy.sleep(0.2)

if __name__ == '__main__':
    rospy.init_node('walker_demo')

    rospy.loginfo('Instantiating robot Client')
    robot = PhantomX()
    rospy.sleep(1)

    rospy.loginfo('Walker Demo Starting')

    #print robot.lidar_ranges[180]                  #180=front, 270=left, 90=right

    while True:
        global regions_
        regions_ = {
            'left':  min(min(robot.lidar_ranges[240:280]), 10),
            'fleft': min(min(robot.lidar_ranges[210:240]), 10),
            'front':  min(min(robot.lidar_ranges[150:210]), 10),
            'fright':  min(min(robot.lidar_ranges[130:150]), 10),
            'right':   min(min(robot.lidar_ranges[80:120]), 10),
        }
        take_action()

        if state_ == 0:
            turn_right()
        elif state_ == 1:
            turn_left()
        elif state_ == 2:
            go_forward()
            pass
        else:
            rospy.logerr('Unknown state!')

        # robot.set_walk_velocity(1, 0, -0.15)
    # rospy.sleep(5)
    # robot.set_walk_velocity(1, 0, 0)
    # rospy.sleep(3)
    # robot.set_walk_velocity(0, 1, 0)
    # rospy.sleep(3)
    # robot.set_walk_velocity(0, -1, 0)
    # rospy.sleep(3)
    # robot.set_walk_velocity(-1, 0, 0)x
    # rospy.sleep(3)
    # robot.set_walk_velocity(1, 1, 0)
    # rospy.sleep(5)
    # robot.set_walk_velocity(0, 0, 0)

    rospy.loginfo('Walker Demo Finished')
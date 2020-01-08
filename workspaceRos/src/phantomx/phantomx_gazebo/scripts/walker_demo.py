#!/usr/bin/env python

import rospy

from phantomx_gazebo.phantomx import PhantomX

regions_ = {
    'right': 0,
    'fright': 0,
    'front': 0,
    'fleft': 0,
    'left': 0,
}
state_ = 0
state_dict_ = {
    0: 'find the wall',
    1: 'turn left',
    2: 'follow the wall',
}

def change_state(state):
    global state_, state_dict_
    if state is not state_:
        print 'Wall follower - [%s] - %s' % (state, state_dict_[state])
        state_ = state

def take_action():
    global regions_
    regions = regions_
    robot.set_walk_velocity(0, 0, 0)
    
    state_description = ''
    
    d = 2.0
    
    if regions['front'] > d and regions['fleft'] > d and regions['fright'] > d:
        state_description = 'case 1 - nothing'
        change_state(0)
    elif regions['front'] < d and regions['fleft'] > d and regions['fright'] > d:
        state_description = 'case 2 - front'
        change_state(1)
    elif regions['front'] > d and regions['fleft'] > d and regions['fright'] < d:
        state_description = 'case 3 - fright'
        change_state(2)
    elif regions['front'] > d and regions['fleft'] < d and regions['fright'] > d:
        state_description = 'case 4 - fleft'
        change_state(0)
    elif regions['front'] < d and regions['fleft'] > d and regions['fright'] < d:
        state_description = 'case 5 - front and fright'
        change_state(1)
    elif regions['front'] < d and regions['fleft'] < d and regions['fright'] > d:
        state_description = 'case 6 - front and fleft'
        change_state(1)
    elif regions['front'] < d and regions['fleft'] < d and regions['fright'] < d:
        state_description = 'case 7 - front and fleft and fright'
        change_state(1)
    elif regions['front'] > d and regions['fleft'] < d and regions['fright'] < d:
        state_description = 'case 8 - fleft and fright'
        change_state(0)
    else:
        state_description = 'unknown case'
        rospy.loginfo(regions)

def find_wall():
    robot.set_walk_velocity(1, 0, -1)
    rospy.sleep(0.2)

def turn_left():
    robot.set_walk_velocity(0.4, 0, 0.5)
    rospy.sleep(0.2)

def follow_the_wall():
    global regions_
    
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
            'left':  min(min(robot.lidar_ranges[260:280]), 10),
            'fleft': min(min(robot.lidar_ranges[210:240]), 10),
            'front':  min(min(robot.lidar_ranges[170:190]), 10),
            'fright':  min(min(robot.lidar_ranges[120:150]), 10),
            'right':   min(min(robot.lidar_ranges[80:100]), 10),
        }
        take_action()

        if state_ == 0:
            find_wall()
        elif state_ == 1:
            turn_left()
        elif state_ == 2:
            follow_the_wall()
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
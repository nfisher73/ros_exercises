#!/usr/bin/env python

import rospy

from sensor_msgs.msg import LaserScan
from ros_exercises.msg import OpenSpace
from numpy import pi

pub = rospy.Publisher("open_space", OpenSpace, queue_size=20)

def callback(scan):
    longest = max(scan.ranges) #longest range value
    index = scan.ranges.index(longest) #index of longest value
    angle = scan.angle_min + index*scan.angle_increment #angle at largest value calculated using min_angle, index, and angle increment
    
    custom = OpenSpace()
    custom.angle = angle
    custom.distance = longest
    pub.publish(custom)


def listen():
    rospy.init_node('open_space_publisher', anonymous = True)
    
    rospy.Subscriber('fake_scan', LaserScan, callback)

    rospy.spin() #keeps python from exiting until node stops


if __name__ == '__main__':
    listen()

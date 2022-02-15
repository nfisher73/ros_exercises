#!/usr/bin/env python

import rospy

from sensor_msgs.msg import LaserScan
from std_msgs.msg import Float32
from numpy import pi

pubD = rospy.Publisher("open_space/distance", Float32, queue_size=20)
pubA = rospy.Publisher("open_space/angle", Float32, queue_size=20)


def callback(scan):
    longest = max(scan.ranges) #longest range value
    index = scan.ranges.index(longest) #index of longest value
    angle = scan.angle_min + index*scan.angle_increment #angle at largest value calculated using min_angle, index, and angle increment
    
    pubD.publish(longest)
    pubA.publish(angle)


def listen():
    rospy.init_node('open_space_publisher', anonymous = True)
    
    rospy.Subscriber('fake_scan', LaserScan, callback)

    rospy.spin() #keeps python from exiting until node stops


if __name__ == '__main__':
    listen()

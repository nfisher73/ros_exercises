#!/usr/bin/env python 

import rospy

from random import uniform
from numpy import pi
from sensor_msgs.msg import LaserScan


def talker():
    pub = rospy.Publisher('fake_scan', LaserScan, queue_size = 20)
    rospy.init_node('fake_scan_publisher', anonymous = True)
    rate = rospy.Rate(20) # 20hz

    while not rospy.is_shutdown():
        time = rospy.Time.now() 

        scan = LaserScan()

        scan.header.stamp = time
        scan.header.frame_id = 'base_link'
        scan.angle_min = (-2.0/3.0)*pi
        scan.angle_max = (2.0/3.0)*pi
        scan.angle_increment = (1.0/300.0)*pi
        scan.scan_time = 1.0/20
        scan.range_min = 1.0
        scan.range_max = 10.0
        
        scan.ranges = []

        for i in range(401):
            scan.ranges.append(uniform(1.0, 10.0))

        pub.publish(scan)
        rate.sleep()

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass

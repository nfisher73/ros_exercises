#!/usr/bin/env python 

import rospy

from random import uniform
from numpy import pi
from sensor_msgs.msg import LaserScan



def talker():
    pub = rospy.Publisher(rospy.get_param('fake_scan/pub_topic', '/fake_scan'), LaserScan, queue_size = 20)
    rospy.init_node('fake_scan_publisher', anonymous = True)
    rate = rospy.Rate(rospy.get_param('fake_scan/pub_rate', 20)) # 20hz

    while not rospy.is_shutdown():
        time = rospy.Time.now() 

        scan = LaserScan()
        

        scan.header.stamp = time
        scan.header.frame_id = 'base_link'
        scan.angle_min = eval(rospy.get_param('fake_scan/angle_min', '(-2.0/3.0)*pi'))
        scan.angle_max = eval(rospy.get_param('fake_scan/angle_max', '(2.0/3.0)*pi'))
        scan.angle_increment = eval(rospy.get_param('fake_scan/angle_increment', '(1.0/300.0)*pi'))
        scan.scan_time = 1.0/rospy.get_param('fake_scan/pub_rate', 20)
        scan.range_min = rospy.get_param('fake_scan/range_min', 1.0)
        scan.range_max = rospy.get_param('fake_scan/range_max', 10.0)
        
        scan.ranges = []

        for i in range(1 + int(round(abs((scan.angle_max - scan.angle_min)/scan.angle_increment)))):
            scan.ranges.append(uniform(scan.range_min, scan.range_max))

        pub.publish(scan)
        rate.sleep()

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass

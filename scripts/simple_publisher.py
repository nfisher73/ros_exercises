#!/usr/bin/env python

import rospy

from random import uniform
from std_msgs.msg import Float32

def talker():
    pub = rospy.Publisher('my_random_float', Float32, queue_size=20) # topic: my_random_float, type: Float32
    rospy.init_node('simple_publisher', anonymous=True) # Publish to simple_publisher
    rate = rospy.Rate(20) # 20 hz
    while not rospy.is_shutdown():
        rando = uniform(0.0, 10.0) #generate random float from 0-10.0
        rospy.loginfo("Number Generated: %s", rando)
        pub.publish(rando)
        rate.sleep()

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass

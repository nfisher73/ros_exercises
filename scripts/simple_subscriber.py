#!/usr/bin/env python
import rospy

from std_msgs.msg import Float32
import numpy as np

pub = rospy.Publisher('random_float_log', Float32, queue_size=10)

def callback(data):
    rospy.loginfo(rospy.get_caller_id() + "I had %s", data.data)
    rospy.loginfo("Natural Log: %s", np.log(data.data))
    pub.publish(np.log(data.data))

def listener():
    rospy.init_node('simple_subscriber', anonymous = True)

    rospy.Subscriber('my_random_float', Float32, callback)
    rospy.spin()

if __name__ == '__main__':
    listener() 

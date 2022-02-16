#!/usr/bin/env python

import rospy
import tf2_ros as tf2
import numpy as np
from geometry_msgs.msg import TransformStamped
import tf.transformations as tft 



if __name__ == '__main__':
    rospy.init_node('static_tf_cam_publisher')
    broad = tf2.StaticTransformBroadcaster()
    
    left_cam = TransformStamped()
    right_cam = TransformStamped()

    time = rospy.Time.now()
    left_cam.header.stamp = time
    right_cam.header.stamp = time

    left_cam.header.frame_id = "base_link_gt"
    right_cam.header.frame_id = "base_link_gt"
    left_cam.child_frame_id = "left_cam"
    right_cam.child_frame_id = "right_cam"

    left_cam.transform.translation.x = -0.05
    left_cam.transform.translation.y = 0
    left_cam.transform.translation.z = 0

    right_cam.transform.translation.x = 0.05
    right_cam.transform.translation.y = 0
    right_cam.transform.translation.z = 0

    left_cam.transform.rotation.x = 0
    left_cam.transform.rotation.y = 0
    left_cam.transform.rotation.z = 0
    left_cam.transform.rotation.w = 1.

    right_cam.transform.rotation.x = 0
    right_cam.transform.rotation.y = 0
    right_cam.transform.rotation.z = 0
    right_cam.transform.rotation.w = 1.

    broad.sendTransform([left_cam, right_cam])
    rospy.spin()

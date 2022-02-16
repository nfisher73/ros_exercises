#!/usr/bin/env python

import rospy
import tf2_ros as tf2
import numpy as np
from geometry_msgs.msg import TransformStamped
import tf.transformations as tft 

rospy.init_node('base_link_tf_pub')

broad = tf2.TransformBroadcaster()


tfBuffer = tf2.Buffer()
listener = tf2.TransformListener(tfBuffer)

r = rospy.Rate(10)

while not rospy.is_shutdown():
    try:
        left_transform = tfBuffer.lookup_transform("world", "left_cam", rospy.Time())

    except (tf2.LookupException, tf2.ConnectivityException, tf2.ExtrapolationException):
        r.sleep()
        continue
    
    rot = left_transform.transform.rotation
    transl = left_transform.transform.translation
    
    translV = [transl.x, transl.y, transl.z]
    translMat = tft.translation_matrix(translV)

    rotV = [rot.x, rot.y, rot.z, rot.w]
    rotMat = tft.quaternion_matrix(rotV)

    leftPose = tft.concatenate_matrices(translMat, rotMat)

    robLC = tft.translation_matrix([0.05, 0, 0])
    robWrld = tft.concatenate_matrices(leftPose, robLC)
    
    rob = TransformStamped()
    rob.header.stamp = rospy.Time.now()
    rob.header.frame_id = 'world'
    rob.child_frame_id = 'base_link_gt_2'
    robWrldV = tft.translation_from_matrix(robWrld)
    rob.transform.translation.x = robWrldV[0]
    rob.transform.translation.y = robWrldV[1]
    rob.transform.translation.z = robWrldV[2]
    
    rob.transform.rotation.x = rot.x
    rob.transform.rotation.y = rot.y
    rob.transform.rotation.z = rot.z
    rob.transform.rotation.w = rot.w

    broad.sendTransform(rob)
    r.sleep()


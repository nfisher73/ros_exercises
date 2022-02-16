#!/usr/bin/env python

import rospy
import tf2_ros as tf2
import numpy as np
from geometry_msgs.msg import TransformStamped
import tf.transformations as tft 

rospy.init_node('dynamic_tf_cam_publisher')

broad = tf2.TransformBroadcaster()


tfBuffer = tf2.Buffer()
listener = tf2.TransformListener(tfBuffer)

r = rospy.Rate(10)

while not rospy.is_shutdown():
    try:
        robot_transform = tfBuffer.lookup_transform("world", "base_link_gt", rospy.Time())

    except (tf2.LookupException, tf2.ConnectivityException, tf2.ExtrapolationException):
        r.sleep()
        continue
    
    rot = robot_transform.transform.rotation
    transl = robot_transform.transform.translation
    
    translV = [transl.x, transl.y, transl.z]
    translMat = tft.translation_matrix(translV)

    rotV = [rot.x, rot.y, rot.z, rot.w]
    rotMat = tft.quaternion_matrix(rotV)

    botPose = tft.concatenate_matrices(translMat, rotMat)

    lCamRP = tft.translation_matrix([-0.05, 0, 0])
    lCamWrld = tft.concatenate_matrices(botPose, lCamRP)
    rCamLCP = tft.translation_matrix([0.1, 0, 0])
    
    leftCam = TransformStamped()
    leftCam.header.stamp = rospy.Time.now()
    leftCam.header.frame_id = 'world'
    leftCam.child_frame_id = 'left_cam'
    lCamWrldV = tft.translation_from_matrix(lCamWrld)
    leftCam.transform.translation.x = lCamWrldV[0]
    leftCam.transform.translation.y = lCamWrldV[1]
    leftCam.transform.translation.z = lCamWrldV[2]
    
    leftCam.transform.rotation.x = rot.x
    leftCam.transform.rotation.y = rot.y
    leftCam.transform.rotation.z = rot.z
    leftCam.transform.rotation.w = rot.w

    rightCam = TransformStamped()
    rightCam.header.stamp = rospy.Time.now()
    rightCam.header.frame_id = 'left_cam'
    rightCam.child_frame_id = 'right_cam'
    rCamLCV = tft.translation_from_matrix(rCamLCP)
    rightCam.transform.translation.x = rCamLCV[0]
    rightCam.transform.translation.y = rCamLCV[1]
    rightCam.transform.translation.z = rCamLCV[2]
    
    rightRL = tft.quaternion_from_matrix(rCamLCP)
    rightCam.transform.rotation.x = rightRL[0]
    rightCam.transform.rotation.y = rightRL[1]
    rightCam.transform.rotation.z = rightRL[2]
    rightCam.transform.rotation.w = rightRL[3]

    broad.sendTransform([leftCam, rightCam])
    r.sleep()


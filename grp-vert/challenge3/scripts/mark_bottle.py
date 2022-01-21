#!/usr/bin/env python3
import rospy, math
import std_msgs.msg
from sensor_msgs.msg import CameraInfo, Image
from visualization_msgs.msg import Marker
from geometry_msgs.msg import Pose
from std_msgs.msg import ColorRGBA
from image_geometry import PinholeCameraModel
from cv_bridge import CvBridge
import numpy as np
import cv2 as cv
import tf2_ros

rospy.init_node('mark_bottles', anonymous=True)

bottlePublisher = rospy.Publisher(
    '/bottle',
    Marker, queue_size=10
)

# global variables
camInfo = CameraInfo()
bottleIt = 0
depthFrame = []
bridge = CvBridge()

# reads the CameraInfo messages and updates the camera object
def updateCamera(data):
    global camInfo
    camInfo = data

# reads the depth Image data and converts it to a usable format
def getDepthImage(raw):
    global bridge
    global depthFrame
    depthFrame = np.array(bridge.imgmsg_to_cv2(raw, "passthrough"))

# recieves pixel coordinates of centers of regions of interest and determines the 3D coordinates
def get3DPosition(center, camInfo_when_detected, depthFrame_when_detected):
    cam = PinholeCameraModel()
    cam.fromCameraInfo(camInfo_when_detected)
    interest = cam.rectifyPoint(center)
    coords = cam.projectPixelTo3dRay(interest)
    depth = depthFrame_when_detected[int(center[1])][int(center[0])]

    #calculates position data of the objects with the old depth frame and camera information
    p = Pose()
    #y z x in reference to camera_link = coords 0, 1, 2 (in this order)
    if(depth != 0.0):
        p.position.x = coords[2]* (depth/1000)
        p.position.y = -(coords[0]* (depth/1000))
        p.position.z = -(coords[1]* (depth/1000))
        p.orientation.x = 0
        p.orientation.y = 0
        p.orientation.z = 0
        p.orientation.w = 1
        bottle_found(p)

# creates marker and publishes it in /bottle topic
def bottle_found(position):
    global bottleIt
    mrk= Marker()
    h = std_msgs.msg.Header()
    h.stamp = rospy.Time.now()
    h.frame_id = "camera_link"
    mrk.header = h
    mrk.ns = "bottles"
    mrk.id = bottleIt
    mrk.type = 1
    mrk.action = 0
    mrk.pose = position
    mrk.scale.x = 0.2
    mrk.scale.y = 0.2
    mrk.scale.z = 0.2

    c = ColorRGBA()
    c.g = 1.0
    c.a = 1.0
    mrk.color = c
    bottleIt = bottleIt + 1
    # publish position
    bottlePublisher.publish(mrk)


rospy.Subscriber("/camera/aligned_depth_to_color/camera_info", CameraInfo, updateCamera)
rospy.Subscriber("/camera/aligned_depth_to_color/image_raw", Image, getDepthImage)
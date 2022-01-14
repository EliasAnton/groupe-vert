#!/usr/bin/env python3
import rospy, math, time
import std_msgs.msg
from sensor_msgs.msg import CameraInfo, Image
from visualization_msgs.msg import Marker
from geometry_msgs.msg import Pose
from std_msgs.msg import ColorRGBA
from image_geometry import PinholeCameraModel
from cv_bridge import CvBridge
from nav_msgs.msg import Odometry
import numpy as np
import cv2 as cv

rospy.init_node('mark_bottles', anonymous=True)

bottlePublisher = rospy.Publisher(
    '/bottle',
    Marker, queue_size=10
)

# global variables
camera = PinholeCameraModel()
roboPose = Pose()
bottleIt = 0
# depthFrame = np.zeros((256, 256, 1), dtype = "uint16")
# # depthFrame.encoding = "mono16"
bridge = CvBridge()

# reads the CameraInfo messages and updates the camera object
def updateCamera(data):
    global camera
    camera.fromCameraInfo(data)

# reads the Odom messages and updates the robots position
def getRoboPose(data):
    global roboPose
    roboPose = data.pose.pose

# reads the depth Image data and converts it to a usable format
def getDepthImage(raw):
    global bridge
    global depthFrame
    depthFrame = bridge.imgmsg_to_cv2(depthFrame, "mono16")
    raw.encoding = "mono16"
    depthFrame = bridge.imgmsg_to_cv2(raw, "mono16")

# recieves pixel coordinates of centers of regions of interest and determines the 3D coordinates
def get3DPosition(center):

    interest = camera.rectifyPoint(center)
    coords = camera.projectPixelTo3dRay(interest)

    #calculates position data of the objects with the odom and camera information
    p = Pose()
    # p.position.x = coords[2] + roboPose.position.x
    # p.position.y = - coords[0] + roboPose.position.y
    # p.position.z = coords[1] + roboPose.position.z
    p.position.x = coords[2] 
    p.position.y = - coords[0]
    p.position.z = coords[1]
    p.orientation.x = 0.0
    p.orientation.y = 0.0
    p.orientation.z = 0.0
    p.orientation.w = 1.0

    #publish position
    bottle_found(p)

# creates marker and publishes it in /bottle topic
def bottle_found(position):
    global bottleIt
    mrk= Marker()
    h = std_msgs.msg.Header()
    h.stamp = rospy.Time.now()
    h.frame_id = "map"
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

    print("----------------------------------------------------")
    print("bottle ")
    print(bottleIt)
    print(position)
    
    bottlePublisher.publish(mrk)


rospy.Subscriber("/camera/aligned_depth_to_color/camera_info", CameraInfo, updateCamera)
rospy.Subscriber("/odom", Odometry, getRoboPose)
rospy.Subscriber("/camera/aligned_depth_to_color/image_raw", Image, getDepthImage)


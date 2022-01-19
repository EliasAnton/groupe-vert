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
import tf2_ros
from tf2_geometry_msgs import PoseStamped

rospy.init_node('mark_bottles', anonymous=True)

bottlePublisher = rospy.Publisher(
    '/bottle',
    Marker, queue_size=10
)
axisPublisher = rospy.Publisher(
    '/axes',
    PoseStamped, queue_size=10
)
# global variables
camInfo = CameraInfo()
roboOdom = Odometry()
bottleIt = 0
depthFrame = []
bridge = CvBridge()

# reads the CameraInfo messages and updates the camera object
def updateCamera(data):
    global camInfo
    camInfo = data

# reads the Odom messages and updates the robots position
def getRoboOdom(data):
    global roboOdom
    roboOdom = data

# reads the depth Image data and converts it to a usable format
def getDepthImage(raw):
    global bridge
    global depthFrame
    depthFrame = np.array(bridge.imgmsg_to_cv2(raw, "passthrough"))

# recieves pixel coordinates of centers of regions of interest and determines the 3D coordinates
def get3DPosition(center, camPos_when_detected, camInfo_when_detected, depthFrame_when_detected):
    cam = PinholeCameraModel()
    cam.fromCameraInfo(camInfo_when_detected)
    #print(center)
    interest = cam.rectifyPoint(center)
    coords = cam.projectPixelTo3dRay(interest)
    #print(coords)
    depth = depthFrame_when_detected[int(center[1])][int(center[0])]
    #print(depth)

    #calculates position data of the objects with the old camera position, depth frame and camera information
    p = Pose()
    #y z x in reference to camera_link = coords 0, 1, 2 (in this order)
    if(depth != 0.0):
        p.position.x = coords[2]* (depth/1000)
        p.position.y = -(coords[0]* (depth/1000))
        p.position.z = -(coords[1]* (depth/1000))
        print(p.position)
        p.orientation.x = camPos_when_detected.orientation.x
        p.orientation.y = camPos_when_detected.orientation.y
        p.orientation.z = camPos_when_detected.orientation.z
        p.orientation.w = camPos_when_detected.orientation.w
        print("Orientation")
        print(p.orientation)
        #publish position
        # p.position.x = p.position.x - camPos_when_detected.position.x
        # p.position.y = p.position.y - camPos_when_detected.position.y
        # p.position.z = p.position.z - camPos_when_detected.position.z
        print(p.position)

        bottle_found(p)

# transforms a position from one frame to another
def transform_pose(input_pose, from_frame, to_frame):
    # **Assuming /tf2 topic is being broadcasted
    tf_buffer = tf2_ros.Buffer()
    listener = tf2_ros.TransformListener(tf_buffer)

    pose_stamped = PoseStamped()
    pose_stamped = input_pose
    pose_stamped.header.frame_id = from_frame

    try:
        # ** It is important to wait for the listener to start listening. Hence the rospy.Duration(1)
        output_pose_stamped = tf_buffer.transform(pose_stamped, to_frame, rospy.Duration(1))
        return output_pose_stamped.pose

    except (tf2_ros.LookupException, tf2_ros.ConnectivityException, tf2_ros.ExtrapolationException):
        raise

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
    
    bottlePublisher.publish(mrk)


rospy.Subscriber("/camera/aligned_depth_to_color/camera_info", CameraInfo, updateCamera)
rospy.Subscriber("/odom", Odometry, getRoboOdom)
rospy.Subscriber("/camera/aligned_depth_to_color/image_raw", Image, getDepthImage)
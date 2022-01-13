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

rospy.init_node('mark_bottles', anonymous=True)

bottlePublisher = rospy.Publisher(
    '/bottle',
    Marker, queue_size=10
)

camera = PinholeCameraModel()
roboPose = Pose()
bottleIt = 0
# bridge = CvBridge()
# rect = Image()
# rect.encoding = "mono16"
# rect = bridge.imgmsg_to_cv2(rect, 'mono16')

def updateCamera(data):
    global camera
    camera.fromCameraInfo(data)

# def getDepthImage(raw):
#     global rect
#     global camera
#     global bridge
#     raw.encoding = "mono16"
#     changedraw = bridge.imgmsg_to_cv2(raw, "mono16")
#     camera.rectifyImage(changedraw, rect)
#     interest = camera.rectifyPoint((5,5))
#     coords = camera.projectPixelTo3dRay(interest)
#     print("rect")
#     print(coords)


def getRoboPose(data):
    global roboPose
    roboPose = data.pose.pose

def get3DPosition(center):
    #2D pixel in 3D umrechnen und publishen (Pos )
    # coords = []
    # x = center[0]
    # y = center[1]
    # for i in range(y-3, y+3 ):
    #         for j in range(x-3, x+3):
    #             interest = camera.rectifyPoint((i,j))
    #             coords.append(camera.projectPixelTo3dRay(interest))
    
    # # median = np.median(list(dict(coords).values()))

    # xMean = 0
    # yMean = 0
    # zMean = 0

    # for el in coords:
    #     xMean = xMean + el[2]
    #     yMean = yMean + el[0]
    #     zMean = zMean + el[1]

    # xMean = xMean / len(coords)
    # yMean = yMean / len(coords)
    # zMean = zMean / len(coords)

    interest = camera.rectifyPoint(center)
    coords = camera.projectPixelTo3dRay(interest)

    p = Pose()
    p.position.x = coords[2] + roboPose.position.x
    p.position.y = coords[0] + roboPose.position.y
    p.position.z = coords[1] + roboPose.position.z + 0.1
    p.orientation.x = 0.0
    p.orientation.y = 0.0
    p.orientation.z = 0.0
    p.orientation.w = 1.0

    bottle_found(p)

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
#rospy.Subscriber("/camera/aligned_depth_to_color/image_raw", Image, getDepthImage)
#rospy.spin()


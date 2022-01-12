#!/usr/bin/env python3
import rospy, math, time
import std_msgs.msg
from sensor_msgs.msg import CameraInfo, Image
from visualization_msgs.msg import Marker
from geometry_msgs.msg import Pose
from std_msgs.msg import ColorRGBA
from image_geometry import PinholeCameraModel
from cv_bridge import CvBridge

rospy.init_node('mark_bottles', anonymous=True)

bottlePublisher = rospy.Publisher(
    '/visualization_marker',
    #!!!!!!!!!!!!!!!!!Marker muss bottle sein... Topic erstellen
    Marker, queue_size=10
)

camera = PinholeCameraModel()
bridge = CvBridge()
# rect = Image()
# rect = bridge.imgmsg_to_cv2(rect, 'mono16')

def updateCamera(data):
    global camera
    camera.fromCameraInfo(data)

def getDepthImage(raw):
    global rect
    global camera
    global bridge
    changedraw = bridge.imgmsg_to_cv2(raw, 'mono16')
    camera.rectifyImage(changedraw, rect)
    print("rect")
    print(rect.item(1,1))

def get3DPosition(center):
    #2D pixel in 3D umrechnen und publishen
    global rect
    print("center in rect")
    print(rect.item(center))

def bottle_found(position):
    mrk= Marker()
    h = std_msgs.msg.Header()
    h.stamp = rospy.Time.now()
    h.frame_id = "odom"
    mrk.header = h
    mrk.ns = "bottles"
    mrk.id = 0
    mrk.type = 1
    mrk.action = 0
    # p = Pose()
    # p.position.x = 3
    # p.position.y = 3
    # p.position.z = 3
    # p.orientation.x = 0.0
    # p.orientation.y = 0.0
    # p.orientation.z = 0.0
    # p.orientation.w = 1.0
    # mrk.pose = p
    mrk.pose = position
    mrk.scale.x = 1.0
    mrk.scale.y = 1.0
    mrk.scale.z = 1.0

    c = ColorRGBA()
    c.g = 1.0
    c.a = 1.0
    mrk.color = c

    bottlePublisher.publish(mrk)

# #ungefaehr wenn kamera flasche erkennt
# rospy.Subscriber("scan", LaserScan, bottle_found)
# rospy.spin()



rospy.Subscriber("/camera/aligned_depth_to_color/camera_info", CameraInfo, updateCamera)
rospy.Subscriber("/camera/aligned_depth_to_color/image_raw", Image, getDepthImage)
rospy.spin()


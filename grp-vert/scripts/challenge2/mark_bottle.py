#!/usr/bin/env python3
import rospy, math, time
import std_msgs.msg
from sensor_msgs.msg import LaserScan
from visualization_msgs.msg import Marker
from geometry_msgs.msg import Pose
from std_msgs.msg import ColorRGBA

rospy.init_node('mark_bottles', anonymous=True)

markerPublisher = rospy.Publisher(
    '/visualization_marker',
    Marker, queue_size=10
)

def bottle_found(data):
    mrk= Marker()
    h = std_msgs.msg.Header()
    h.stamp = rospy.Time.now()
    h.frame_id = "map"
    mrk.header = h
    mrk.ns = "bottles"
    mrk.id = 0
    mrk.type = 1
    mrk.action = 0
    p = Pose()
    p.position.x = 3
    p.position.y = 3
    p.position.z = 3
    p.orientation.x = 0.0
    p.orientation.y = 0.0
    p.orientation.z = 0.0
    p.orientation.w = 1.0
    mrk.pose = p
    mrk.scale.x = 1.0
    mrk.scale.y = 1.0
    mrk.scale.z = 1.0

    c = ColorRGBA()
    c.g = 1.0
    c.a = 1.0
    mrk.color = c

    markerPublisher.publish(mrk)

#ungefaehr wenn kamera flasche erkennt
rospy.Subscriber("base_scan", LaserScan, bottle_found)
rospy.spin()
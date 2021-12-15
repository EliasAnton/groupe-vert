#!/usr/bin/env python3
import rospy, math, std_msgs.msg
from sensor_msgs.msg import LaserScan
from sensor_msgs.msg import PointCloud
from geometry_msgs.msg import Point32

obstacles= []
laserdataPublisher = rospy.Publisher(
    'PoinCloud_from_scanner',
    PointCloud, queue_size=10
)

def main():
    # In ROS, nodes are uniquely named. If two nodes with the same
    # name are launched, the previous one is kicked off. The
    # anonymous=True flag means that rospy will choose a unique
    # name for our 'listener' node so that multiple listeners can
    # run simultaneously.
    rospy.init_node('dodge', anonymous=True)

    # call the scan_data at a regular frequency:
    rospy.Timer( rospy.Duration(0.1), scan_data, oneshot=False )
    rospy.Subscriber("scan", LaserScan, callback)

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()


def callback(data):
    global obstacles
    angle= data.angle_min
    for aDistance in data.ranges :
        if 0.1 < aDistance and aDistance < 5.0 :
            aPoint= [ 
                math.cos(angle) * aDistance, 
                math.sin( angle ) * aDistance
            ]
            obstacles.append( aPoint )
        angle+= data.angle_increment
    rospy.loginfo( str(
        [ [ round(p[0], 2), round(p[1], 2) ] for p in  obstacles[0:10] ] 
    ) + " ..." )
    
# Publish scan data:
def scan_data(data):
    global obstacles
    global laserdataPublisher
    pc = PointCloud()
    header = std_msgs.msg.Header()
    header.frame_id = "laser"
    pc.header = header
    #pc.points.append = obstacles
    # Compute cmd_vel here and publish... (do not forget to reduce timer duration)
    laserdataPublisher.publish(pc)


if __name__ == '__main__':
    main()

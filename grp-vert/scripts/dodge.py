#!/usr/bin/env python3
import rospy, math, std_msgs.msg
from sensor_msgs.msg import LaserScan
from sensor_msgs.msg import PointCloud
from geometry_msgs.msg import Point32, Twist

obstacles= []
laserdataPublisher = rospy.Publisher(
    'poinCloud_from_scanner',
    PointCloud, queue_size=10
)
commandPublisher = rospy.Publisher(
    '/cmd_vel_mux/input/navi',
    Twist, queue_size=10
)

def main():
    # In ROS, nodes are uniquely named. If two nodes with the same
    # name are launched, the previous one is kicked off. The
    # anonymous=True flag means that rospy will choose a unique
    # name for our 'listener' node so that multiple listeners can
    # run simultaneously.
    rospy.init_node('dodge', anonymous=True)

    # call the scan_data at a regular frequency:
    #rospy.Timer( rospy.Duration(0.1), publish_scan_data, oneshot=False )
    rospy.sleep(0.5)
    #rospy.Subscriber("scan", LaserScan, callback)
    rospy.Subscriber("scan", LaserScan, move_command)

    #rospy.Timer( rospy.Duration(0.1), move_command, oneshot=False )

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()


def callback(data):
    global obstacles
    angle= data.angle_min
    for aDistance in data.ranges :
        if 0.1 < aDistance and aDistance < 5.0 :
            aPoint= [ 
                math.cos(angle) * aDistance, 
                math.sin( angle ) * aDistance,
                0.0
            ]
            obstacles.append( aPoint )
        angle+= data.angle_increment
    rospy.loginfo( str(
        [ [ round(p[0], 2), round(p[1], 2) ] for p in  obstacles[0:10] ] 
    ) + " ..." )
    publish_scan_data()
    

# Publish scan data:
def publish_scan_data():
    global obstacles
    global laserdataPublisher
    pc = PointCloud()
    header = std_msgs.msg.Header()
    header.frame_id = "laser"
    header.stamp = rospy.Time.now()
    header.frame_id = 'map'
    pc.header = header
    #for p in obstacles :
    #    pc.points.append(p)
    #pc.points.append(obstacles)
    pc.points.append(Point32(1.0, 1.0, 0.0))
    laserdataPublisher.publish(pc)

def move_command(data):
    # Compute cmd_vel here and publish... (do not forget to reduce timer duration)
    cmd= Twist()
    angle= data.angle_min
    for aDistance in data.ranges :
        if 0.1 < aDistance and aDistance < 5.0:
            aPoint= [ 
                math.cos(angle) * aDistance, 
                math.sin(angle) * aDistance,
                0.0
            ]
        if aPoint[0] < 1:
            cmd.linear.y= 0.5
        else:
            cmd.linear.x= 0.5
    commandPublisher.publish(cmd)

if __name__ == '__main__':
    main()

#!/usr/bin/env python3
import rospy, math, std_msgs.msg, time
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist

rospy.init_node('dodge', anonymous=True)

commandPublisher = rospy.Publisher(
    '/cmd_vel_mux/input/navi',
    Twist, queue_size=10
)

def main():
    #rospy.Subscriber("scan", LaserScan, callback)
    rospy.Subscriber("scan", LaserScan, move_command)

    #rospy.Timer( rospy.Duration(0.1), move_command, oneshot=False )

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()

def move_command(data):
    cmd= Twist()

    angle= data.angle_min
    angles= []
    for a in data.ranges :
        angles.append(angle)
        angle+= data.angle_increment
    
    middle = len(angles) / 2
    middle = int(middle)
    quarter = len(angles) / 4
    quarter = int(quarter)
    eights = len(angles) / 8
    eights = int(eights)

    close = 0
    
    for b in data.ranges[middle - quarter - 30: middle + eights + 30]:
        if b < 0.4:
            close = close + 1

    #turn, if most of the sensors in the important angle report an obstacle close by
    if close > quarter / 3:
        cmd.linear.x = 0
        cmd.angular.z= 0.8
        commandPublisher.publish(cmd)
    else:
        cmd.linear.x= 0.5
        cmd.angular.z= 0
        commandPublisher.publish(cmd)

if __name__ == '__main__':
    main()

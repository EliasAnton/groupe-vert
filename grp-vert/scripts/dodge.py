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
    rospy.Subscriber("scan", LaserScan, move_command)
    rospy.spin()

def move_command(data):
    cmd= Twist()

    #saves all the angles in a list. The list of angles corresponds to the list of ranges
    angle= data.angle_min
    angles= []
    for a in data.ranges :
        angles.append(angle)
        angle+= data.angle_increment
    
    #middle is the angle value for the position directly in front of the robot
    middle = len(angles) / 2
    middle = int(middle)
    quarter = len(angles) / 4
    quarter = int(quarter)

    #we count all the individual laser rays in a certain angle in front of the robot, which report an obstacle closer than 0,4
    close = 0
    for b in data.ranges[middle - quarter - 30: middle + quarter]:
        if b < 0.4:
            close = close + 1

    #turn, if most of the sensors in the important angle report an obstacle close by
    #we did this, because the sensor probably picked up some false readings and the robot startet to shake
    #with this solution, some false readings don't interrupt a smooth turn
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

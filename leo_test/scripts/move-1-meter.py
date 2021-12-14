#!/usr/bin/python3
import math, rospy
from geometry_msgs.msg import Twist

# Initialize ROS::node
rospy.init_node('move', anonymous=True)

commandPublisher = rospy.Publisher(
    '/cmd_vel',
    Twist, queue_size=10
)

# :
def move_command(data):
    #pub = rospy.Publisher('turtle1/cmd_vel', Twist , queue_size=10)
    #rospy.init_node('move-1-meter', anonymous=True)
    #rate = rospy.Rate(0.1) # 0.1 hz
    # Compute cmd_vel here and publish... (do not forget to reduce timer duration)
    cmd= Twist()
    cmd.linear.x= 0.1
    commandPublisher.publish(cmd)

# call the move_command at a regular frequency:
rospy.Timer( rospy.Duration(0.1), move_command, oneshot=False )

# spin() enter the program in a infinite loop

print("Start move.py")
rospy.spin()

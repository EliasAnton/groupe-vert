#!/usr/bin/env python3
from __future__ import print_function
import rospy, math, std_msgs.msg, time
import cv2 as cv
import argparse
import numpy as np
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import mark_bottle
import os
from tf2_geometry_msgs import PoseStamped
from geometry_msgs.msg import Pose

# upper and lower ranges for our color filters in HSV format
lower_red = np.array([1,120,50])
upper_red = np.array([8,255,225])
lower_white = np.array([0,0,140])
upper_white = np.array([179,50,210])
mapZero = PoseStamped()
mapZero.pose.position.x = 0
mapZero.pose.position.y = 0
mapZero.pose.position.z = 0

# recieves raw image data and uses the trained model to find regions of interest
def detectAndDisplay(raw):
    global lower_red
    global upper_red
    global lower_white
    global upper_white
    bridge = CvBridge()
    
    #transform map to camera
    global mapZero

    mapZero.pose.orientation.x = mark_bottle.roboOdom.pose.pose.orientation.x
    mapZero.pose.orientation.y = mark_bottle.roboOdom.pose.pose.orientation.y
    mapZero.pose.orientation.z = mark_bottle.roboOdom.pose.pose.orientation.z
    mapZero.pose.orientation.w = mark_bottle.roboOdom.pose.pose.orientation.w
    camPos = mark_bottle.transform_pose(mapZero, "map", "camera_link")

    camInfoNow = mark_bottle.camInfo
    depthFrameNow = mark_bottle.depthFrame

    frame = bridge.imgmsg_to_cv2(raw, desired_encoding='bgr8')
    frame_gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    frame_gray = cv.equalizeHist(frame_gray)

    hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
    maskRed = cv.inRange(hsv, lower_red, upper_red)
    maskWhite = cv.inRange(hsv, lower_white, upper_white)
    
    # maskRed =cv.blur(maskRed, (3, 3))
    # maskRed=cv.erode(maskRed, None, iterations=1)
    # maskRed=cv.dilate(maskRed, None, iterations=1)
    # maskWhite=cv.erode(maskWhite, None, iterations=1)
    # maskWhite=cv.dilate(maskWhite, None, iterations=1)
    
    bottles = bottle_cascade.detectMultiScale(image = frame_gray, scaleFactor=1.07, minNeighbors=17, minSize=(25,25), maxSize=(160,160))

    # checks detected regions for red and white details to eliminate false positives
    redCount = 0
    whiteCount = 0
    for (x,y,w,h) in bottles:
        frame = cv.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        for i in range(y + int(h/4), y + int(h*(3/4)) ):
            for j in range(x,x+w):
                pixel = maskRed.item(i,j)
                pixel2 = maskWhite.item(i,j)
                if (pixel == 255):
                    redCount = redCount + 1
                if (pixel2 ==255):
                    whiteCount = whiteCount + 1
        # filter with red and white masks
        if ((redCount >= (h*w)*0.002) and (whiteCount >= (h*w)*0.002)):
            falseCenter = (x + w//2, y + h//2)
            center = list(falseCenter)
            if center[0] >= 1280:
                center[0] = 1279
            if center[1] >= 720:
                center[1] = 719
            frame = cv.ellipse(frame, falseCenter, (w//2, h//2), 0, 0, 360, (0, 0, 255), 4)
            mark_bottle.get3DPosition(center, camPos, camInfoNow, depthFrameNow)

    # opens camera windows for debugging and seeing the detection
    #cv.imshow('RedMask',maskRed)
    #cv.imshow('WhiteMask',maskWhite)
    cv.imshow('Capture - Bottle detection', frame)
    cv.waitKey(1)

dirname = os.path.dirname(__file__)
bottle_cascade_name = os.path.join(dirname, './cascade.xml')
bottle_cascade = cv.CascadeClassifier()

# Load the cascade
if not bottle_cascade.load(cv.samples.findFile(bottle_cascade_name)):
    print('--(!)Error loading bottle cascade')
    exit(0)

# raw cam data subscriber
rospy.Subscriber("/camera/color/image_raw", Image, detectAndDisplay, buff_size = 2048)
rospy.spin()
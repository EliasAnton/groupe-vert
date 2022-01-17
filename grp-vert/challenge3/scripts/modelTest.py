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

# upper and lower ranges for our color filters in HSV format
lower_red = np.array([3,150,50])
upper_red = np.array([8,245,220])
lower_white = np.array([0,0,150])
upper_white = np.array([179,50,220])

# recieves raw image data and uses the trained model to find regions of interest
def detectAndDisplay(raw):
    global lower_red
    global upper_red
    global lower_white
    global upper_white
    bridge = CvBridge()

    frame = bridge.imgmsg_to_cv2(raw, desired_encoding='bgr8')
    frame_gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    frame_gray = cv.equalizeHist(frame_gray)
    
    hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
    maskRed = cv.inRange(hsv, lower_red, upper_red)
    maskWhite = cv.inRange(hsv, lower_white, upper_white)
    frame=cv.blur(frame, (7, 7))
    maskRed=cv.erode(maskRed, None, iterations=3)
    maskRed=cv.dilate(maskRed, None, iterations=3)
    maskWhite=cv.erode(maskWhite, None, iterations=3)
    maskWhite=cv.dilate(maskWhite, None, iterations=3)


    # Detect bottles
    bottles = bottle_cascade.detectMultiScale(image = frame_gray, scaleFactor=1.4, minNeighbors=8, minSize=(10,10))
    
    # checks detected regions for red and white details to eliminate false positives
    redCount = 0
    whiteCount = 0
    for (x,y,w,h) in bottles:
        #print((x,y,w,h))
        frame = cv.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        #frame = cv.rectangle(frame, (x, int(y + (h/4))), (x+w, (y + int(h*(3/4)) ) ), (0, 255, 0), 2)   # smaller rectangle
        for i in range(y + int(h/4), y + int(h*(3/4)) ):
            for j in range(x,x+w):
                pixel = maskRed.item(i,j)
                pixel2 = maskWhite.item(i,j)
                if (pixel == 255):
                    redCount = redCount + 1
                if (pixel2 ==255):
                    whiteCount = whiteCount + 1
        #filter with red and white masks
        if ((redCount >= (h*w)*0.04) and (whiteCount >= (h*w)*0.04)):
            falseCenter = (x + w//2, y + h//2)
            center = list(falseCenter)
            if center[0] >= 1280:
                center[0] = 1279
            if center[1] >= 720:
                center[1] = 719
            frame = cv.ellipse(frame, falseCenter, (w//2, h//2), 0, 0, 360, (0, 0, 255), 4)
            mark_bottle.get3DPosition(center)


    # opens camera windows for debugging
    cv.imshow('RedMask',maskRed)
    cv.imshow('WhiteMask',maskWhite)
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
rospy.Subscriber("/camera/color/image_raw", Image, detectAndDisplay)
rospy.spin()
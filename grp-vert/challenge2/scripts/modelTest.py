#!/usr/bin/env python3
from __future__ import print_function
import rospy, math, std_msgs.msg, time
import cv2 as cv
import argparse
import numpy as np
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
#import mark_bottle

rospy.init_node('bottleDetection', anonymous=True)

lower_red = np.array([4,150,50])
upper_red = np.array([7,245,220])
lower_white = np.array([0,0,150])
upper_white = np.array([179,50,220])

def detectAndDisplay(raw):
    global lower_red
    global upper_red
    global lower_white
    global upper_white
    bridge = CvBridge()

    frame = bridge.imgmsg_to_cv2(raw, desired_encoding='bgr8')

    frame_gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    frame_gray = cv.equalizeHist(frame_gray)
    #-- Detect bottles
    hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
    maskRed = cv.inRange(hsv, lower_red, upper_red)
    maskWhite = cv.inRange(hsv, lower_white, upper_white)
    bottles = bottle_cascade.detectMultiScale(frame_gray)
    redCount = 0
    whiteCount = 0
    for (x,y,w,h) in bottles:
        #bottleROI = frame_gray[y:y+h,x:x+w]
        #frame = cv.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        frame = cv.rectangle(frame, (x, int(y + (h/4))), (x+w, (y + int(h*(3/4)) ) ), (0, 255, 0), 2)
        for i in range(y + int(h/4), y + int(h*(3/4)) ):
            for j in range(x,x+w):
                pixel = maskRed.item(i,j)
                pixel2 = maskWhite.item(i,j)
                if (pixel == 255):
                    redCount = redCount + 1
                if (pixel2 ==255):
                    whiteCount = whiteCount + 1
                
        if ((redCount >= (h*w)*0.04) and (whiteCount >= (h*w)*0.04)):
            center = (x + w//2, y + h//2)
            frame = cv.ellipse(frame, center, (w//2, h//2), 0, 0, 360, (0, 0, 255), 4)
            #get3DPosition(center)
            
    cv.imshow('RedMask',maskRed)
    cv.imshow('WhiteMask',maskWhite)
    cv.imshow('Capture - Bottle detection', frame)
    cv.waitKey(3)

# parser = argparse.ArgumentParser(description='Code for Cascade Classifier tutorial.')
# parser.add_argument('--bottle_cascade', help='Path to bottle cascade.', default='/home/elias.anton/catkin-ws/src/bilderkennung/data2/cascade.xml')
# parser.add_argument('--camera', help='Camera divide number.', type=int, default=4)
# args = parser.parse_args()
# bottle_cascade_name = args.bottle_cascade
# bottle_cascade = cv.CascadeClassifier()

bottle_cascade_name = '/home/elias.anton/catkin-ws/src/grp-vert/bilderkennung/data3/cascade.xml'
bottle_cascade = cv.CascadeClassifier()

#-- 1. Load the cascade
if not bottle_cascade.load(cv.samples.findFile(bottle_cascade_name)):
    print('--(!)Error loading bottle cascade')
    exit(0)

rospy.Subscriber("/camera/color/image_raw", Image, detectAndDisplay)
# if cv.waitKey(10) == 27:
#     break
rospy.spin()

#-- 2. Read the video stream
# cap=cv.VideoCapture(4)
# if not cap.isOpened:
#     print('--(!)Error opening video capture')
#     exit(0)
# while True:
#     ret, frame = cap.read()
#     if frame is None:
#         print('--(!) No captured frame -- Break!')
#         break
#     detectAndDisplay(frame)
#     if cv.waitKey(10) == 27:
#         break
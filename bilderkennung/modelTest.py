#!/usr/bin/env python3
from __future__ import print_function
import cv2 as cv
import argparse
def detectAndDisplay(frame):
    frame_gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    frame_gray = cv.equalizeHist(frame_gray)
    #-- Detect bottles
    bottles = bottle_cascade.detectMultiScale(frame_gray)
    for (x,y,w,h) in bottles:
        center = (x + w//2, y + h//2)
        frame = cv.ellipse(frame, center, (w//2, h//2), 0, 0, 360, (255, 0, 255), 4)
        faceROI = frame_gray[y:y+h,x:x+w]
    cv.imshow('Capture - Bottle detection', frame)
parser = argparse.ArgumentParser(description='Code for Cascade Classifier tutorial.')
parser.add_argument('--bottle_cascade', help='Path to bottle cascade.', default='/home/elias.anton/catkin-ws/src/bilderkennung/data2/cascade.xml')
parser.add_argument('--camera', help='Camera divide number.', type=int, default=4)
args = parser.parse_args()
bottle_cascade_name = args.bottle_cascade
bottle_cascade = cv.CascadeClassifier()
#-- 1. Load the cascades
if not bottle_cascade.load(cv.samples.findFile(bottle_cascade_name)):
    print('--(!)Error loading bottle cascade')
    exit(0)
camera_device = args.camera
#-- 2. Read the video stream
cap = cv.VideoCapture(camera_device)
if not cap.isOpened:
    print('--(!)Error opening video capture')
    exit(0)
while True:
    ret, frame = cap.read()
    if frame is None:
        print('--(!) No captured frame -- Break!')
        break
    detectAndDisplay(frame)
    if cv.waitKey(10) == 27:
        break
# Groupe Vert
Leonie Schleiter & Elias Anton\
Script language: Python 3\
The project uses the ROS framework

## Installation on new computer:
The project needs the [mb6-tbot files](https://bitbucket.org/imt-mobisyst/mb6-tbot/src/master/) intalled aside to work.
```
mkdir catkin-ws
cd catkin-ws
mkdir src
git clone https://github.com/EliasAnton/groupe-vert.git src/grp-vert
git clone https://bitbucket.org/imt-mobisyst/mb6-tbot src/mb6-tbot
catkin_make
source devel/setup.bash
```

## Challenge 1
### Introduction
This project branch can be used to make a robot move in a real or a simulated environment.

### Strategy: Amoeba strategy
The Robot moves straight until it detects an obstacle. It notes if the obstacle was more at the right side or more at the left side. With this observation it decides if it is going to do a right or a left turn. The turning angle also depends on this observation.

### Run
In catkin-ws/src/grp-vert run: `git checkout challendge1`\
To start the simulation run: `roslaunch grp-vert challendge1_simulation.launch`\
To start the real robot run: `roslaunch grp-vert challendge1_turtlebot.launch`\
(To start the real robot, the robot and the laser scanner have to be connected via USB)

## Challenge 2
### Introduction
This project branch includes a program, which maps an environent by receiving data from a rosbag file. The rosbag file includes the recorded data of a moving robot using an Intel RealSense (color and depth) camera and a laserscanner. Inside this environment bottles are detected and marked on the map with green cubes.\
This part of the project needs to have OpenCV installed.

### Strategy: Bottle detection via Machine Learning - using a trained OpenCV haar classifier
This repository already includes a classifier, which was trained to detect black Nuka Cola bottles by using the OpenCV cascade classifier training (you can find a tutorial here: "https://docs.opencv.org/3.4/dc/d88/tutorial_traincascade.html"). In order to optimize bottle detection, additional color filtering was applied.

### Run
In catkin-ws/src/grp-vert run: `git checkout challenge2`\
To start the program logic and the visualization run: `roslaunch grp-vert challenge2.launch`\
Data has to be given via a rosbag file: `rosbag play --clock <your_bag_file.bag>`\
It has to output the topics:
- /scan
- /odom
- /tf
- /camera/aligned_depth_to_color/camera_info
- /camera/aligned_depth_to_color/image_raw
- /camera/color/image_raw
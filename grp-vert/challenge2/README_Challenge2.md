# Groupe Vert
Leonie Schleiter & Elias Anton

## Introduction
This Projects maps an environent by receiving data from a rosbag file. The rosbag file includes the recorded data of a moving robot using an Intel RealSense depth camera and a Laserscanner. Inside this environment bottles are detected and marked at the map with a green cube.

## Strategy: Bottle detection via Machine Learning - using a trained opencv haar classifier
This repository already includes a classifier, which was trained to detect black Nuka Cola bottles by using the opencv cascade classifier training (you can find a tutorial here: "https://docs.opencv.org/3.4/dc/d88/tutorial_traincascade.html"). In order to optimise bottle detection, additional colour filtering was applied.

## Installation on new computer:
```
mkdir catkin-ws
cd catkin-ws
mkdir src
git clone https://github.com/EliasAnton/groupe-vert.git src/grp-vert
git clone https://bitbucket.org/imt-mobisyst/mb6-tbot src/mb6-tbot
catkin_make
source devel/setup.bash
```

To start the simulation run: `roslaunch grp-vert challendge2.launch`\
To start the real robot run: `roslaunch grp-vert challendge1_turtlebot.launch`\
(To start the real robot, the robot and the laser scanner have to be connected via USB)

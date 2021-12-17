# Groupe Vert
Leonie Schleiter & Elias Anton

## Introduction
This project can be used to make a robot move in a real or a simulated environment. It needs the  [mb6-tbot files](https://bitbucket.org/imt-mobisyst/mb6-tbot/src/master/) to work.
The robot moves forward until it is close to the wall and then turns to the left, continuing the cycle.

To start the simulation run: `roslaunch grp-vert challendge1_simulation.launch`
To start the real robot run: `roslaunch grp-vert challendge1_turtlebot.launch`
(To start the real robot, the robot and the laser scanner have to be connected via bluetooth)

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
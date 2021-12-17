# Groupe Vert
Leonie Schleiter & Elias Anton

## Introduction
This project can be used to make a robot move in a real or a simulated environment. It needs the [mb6-tbot files](https://bitbucket.org/imt-mobisyst/mb6-tbot/src/master/) to work.

## Strategy: Amoeba strategy
The Robot moves straight until it detects an obstacle. It notes if the obstacle was more at the right side or more at the left side. With this observation it decides if it is going to do a right or a left turn. The turning angle also depends on this observation.

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

To start the simulation run: `roslaunch grp-vert challendge1_simulation.launch`\
To start the real robot run: `roslaunch grp-vert challendge1_turtlebot.launch`\
(To start the real robot, the robot and the laser scanner have to be connected via USB)

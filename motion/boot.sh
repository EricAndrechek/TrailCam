#!/bin/bash

sleep 10 &
su - pi -c "screen -S main -dm bash -c 'cd /home/pi/TrailCam/motion && python3 filehandler.py'" &
date > /home/pi/TrailCam/motion/startlog.txt
screen -S main -dm bash -c 'sudo motion -c /home/pi/TrailCam/motion/motion conf' &
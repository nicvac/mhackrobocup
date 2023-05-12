#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor, InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile

from resque_line_setup import *

import time

# Configurazione robot
#@@@ Correggere i valori di axle e wheel secondo la guida riportata qui:
# Measuring and validating the robot dimensions, https://pybricks.com/ev3-micropython/robotics.html#
robot = DriveBase(left_motor, right_motor, wheel_diameter=wheel, axle_track=axle)


while True:
    print(color_sensor_left.color(), "        ", color_sensor_right.color())
    print(light_sensor_front.reflection())
    time.sleep(0.3)

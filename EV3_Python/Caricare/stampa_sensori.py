#!/usr/bin/env pybricks-micropython

# from rescue_line_setup import *
# from rescue_line_functions import *

from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor, InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile


light_sensor_front = ColorSensor(Port.S4)
import time

#Stampa sensori
# while True:  
#     print(color_sensor_left.color(), " - ", color_sensor_right.color(), "\t\t F:", light_sensor_front.reflection() )
#     #print(light_sensor_front.reflection())
#     time.sleep(0.5)


#Test scan
# lineLocked = False
# scanDegree = 100
# while not lineLocked:
#     robot.straight(50) #5 cm
#     robot.stop()
#     lineLocked = scan_double(scanDegree, 0)

while True:
    print(light_sensor_front.color())

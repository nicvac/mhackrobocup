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
color_sensor_left = ColorSensor(Port.S3)
color_sensor_right = ColorSensor(Port.S2)

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
    rgbleft = color_sensor_left.rgb()
    rgbright = color_sensor_right.rgb()

    colorl = color_sensor_left.color()
    colorr = color_sensor_right.color()

    lr = rgbleft[0]
    lg  = rgbleft[1]
    lb = rgbleft[2]

    rr = rgbright[0]
    rg = rgbright[1]
    rb = rgbright[2]

    lp1 = lg / (lg + lr)
    slp1 = "{:.2f}".format(lp1)
    lp2 = lg / (lg + lb)
    slp2 = "{:.2f}".format(lp2)

    rp1 = rg / (rg + rr)
    srp1 = "{:.2f}".format(rp1)
    rp2 = rg / (rg + rb)
    srp2 = "{:.2f}".format(rp2)

    print("Sinistra - r: ", lr, " g: ", lg, " b: ", lb, " Color: ", colorl, "  Destra - r: ", rr, " g: ", rg, " b: ", rb, " Color: ", colorr,  "\t lp1: ", slp1, " lp2: ", slp2, " rp1: ", srp1, " rp2: ", srp2)

    
#!/usr/bin/env pybricks-micropython

from resque_line_setup import *
from resque_line_functions import *

import time

#Stampa sensori
while True:  
    print(color_sensor_left.color(), " - ", color_sensor_right.color(), "\t\t F:", light_sensor_front.reflection() )
    #print(light_sensor_front.reflection())
    time.sleep(0.5)


#Test scan
# lineLocked = False
# scanDegree = 100
# while not lineLocked:
#     robot.straight(50) #5 cm
#     robot.stop()
#     lineLocked = scan_double(scanDegree, 0)

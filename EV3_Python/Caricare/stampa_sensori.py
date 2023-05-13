#!/usr/bin/env pybricks-micropython

from resque_line_setup import *

import time

while True:
    
    print(color_sensor_left.color(), " - ", color_sensor_right.color(), "\t\t F:", light_sensor_front.reflection() )
    #print(light_sensor_front.reflection())
    time.sleep(0.5)


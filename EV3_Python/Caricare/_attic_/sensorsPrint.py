#!/usr/bin/env pybricks-micropython
from rescue_line_functions import *
from rescue_line_setup import *
from client_functions import *

sensorReadingFront = getDistanceCm(DIST_FRONT)
sensorReadingLeft = getDistanceCm(DIST_LEFT)
sensorReadingRight = getDistanceCm(DIST_RIGHT)

print("Front: ", str(sensorReadingFront), "   Left: ", str(sensorReadingLeft), "  Right: ", str(sensorReadingRight))

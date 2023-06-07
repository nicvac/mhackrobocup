#!/usr/bin/env pybricks-micropython
from rescue_line_functions import *
from rescue_line_setup import *
from stanza_main import *
#from guadagna_centro import *


while True:
    left = getDistanceCm(DIST_LEFT)
    right = getDistanceCm(DIST_RIGHT)
    # time.sleep(.3)
    print("{} {}   {}".format(left, right, time.time()))

    

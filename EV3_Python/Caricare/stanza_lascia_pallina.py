#!/usr/bin/env pybricks-micropython
from rescue_line_setup import *
from math import *
from rescue_line_functions import *
from client_functions import *

def lascia_pallina():
    upper_left_motor.run_until_stalled(50)
    upper_left_motor.hold()
    upper_right_motor.hold()
    time.sleep(2.0)
    imposta_carrello_stanza()

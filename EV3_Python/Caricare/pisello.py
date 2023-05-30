#!/usr/bin/env pybricks-micropython
from rescue_line_setup import *
from math import *
from rescue_line_functions import *
from client_functions import *

def lascia_pallina(gradi):
    upper_left_motor.hold()
    upper_right_motor.hold()
    robot_gyro_turn(gradi)
    robot.reset()
    robot.drive(-100,0)
    while getDistanceCm(DIST_BACK) > 10:
        pass
    stop()
    
    dist_percorsa = robot.distance()

    robot_gyro_turn(180)

    extDist.send(30)

#    if light_sensor_front.color() == Color.GREEN:

    if 1==1:
        upper_left_motor.run_angle(50, 50)
        upper_left_motor.hold()
        upper_right_motor.hold()
        upper_left_motor.run_angle(50, -50)
        upper_left_motor.hold()
        upper_right_motor.hold()

    robot_gyro_turn(180)
    robot.straight(0-dist_percorsa)
    robot_gyro_turn(0-gradi)

lascia_pallina(50)


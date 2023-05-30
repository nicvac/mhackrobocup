#!/usr/bin/env pybricks-micropython
from rescue_line_setup import *
from math import *
from rescue_line_functions import *
from client_functions import *

def lascia_pallina(gradi):
    getDistanceCm(DIST_BACK)
    time.sleep(0.5)

    robot_gyro_turn(gradi)
    robot.reset()
    robot.drive(-100,0)
    while getDistanceCm(DIST_BACK) > 10:
        pass
    stop()
    
    dist_percorsa = robot.distance()

    robot_gyro_turn(180)

    #color = light_sensor_front.color()
    color = Color.GREEN 
    if  color == Color.GREEN:
        upper_left_motor.run_angle(50, 50)
        upper_left_motor.hold()
        upper_right_motor.hold()
        time.sleep(2.0)
        upper_left_motor.run_angle(50, -50)
        upper_left_motor.hold()
        upper_right_motor.hold()

    robot_gyro_turn(180)
    robot.straight(0-dist_percorsa)
    robot_gyro_turn(0-gradi)

#@@@ TEST DELLA FUNZIONE: DA CANCELLARE

#@@@ ABBASSA IL CARRELLO E LO ALZA ALLA POSIZIONE DI START
#@@@ METTERE NEL CODICE PRINCIPALE ALLO START!!!
upper_right_motor.stop()
upper_left_motor.run_until_stalled(-50)
time.sleep(1)

upper_left_motor.reset_angle(0)
while upper_left_motor.angle() < 70: #80 120
    upper_left_motor.dc(50)
    upper_right_motor.dc(50)

upper_left_motor.hold()
upper_right_motor.hold()

while True: pass

quit_and_restart_server()
sys.exit()

intosta_il_pisello()
lascia_pallina(50)

#!/usr/bin/env pybricks-micropython
from rescue_line_setup import *
from math import *
from rescue_line_functions import *
from client_functions import *

uscita = False

distanzaTarget = 10

robot.drive(80, 0)

while(getDistanceCm(DIST_FRONT) > distanzaTarget):
    pass
robot.stop()

gyro_sensor.reset_angle(0)

robot.drive(0, 30)

while(abs(gyro_sensor.angle() < 90)):
    pass

robot.stop()

while not uscita:
    robot.drive(80, 0);
    linea = light_sensor_front.color()
    while(getDistanceCm(DIST_FRONT) > distanzaTarget or not isLine(linea)):
        pass
    robot.stop()

    if(isLine(linea)):
        uscita = True
    else:
        gyro_sensor.reset_angle(0)
        robot.drive(0, 30)
        while(abs(gyro_sensor.angle() < 90)):
            pass

        robot.stop()

print("Ho trovato l'uscita")

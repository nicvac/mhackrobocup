#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor, InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile


import time



# Motore grande destra
right_motor = Motor(Port.A)

# Motore grande sinistra
left_motor = Motor(Port.B)

# Diametro ruota in mm
wheel = 32.5

# Distanza dal centro delle ruote da sinistra a destra
axle = 205

lungCingoli = 140

maxSpeed = 1020


# Sensore di colore destra
color_sensor_right = ColorSensor(Port.S2)

# Sensore di colore sinistra
color_sensor_left = ColorSensor(Port.S3)

# Giroscopio
gyro_sensor = GyroSensor(Port.S1)


# Configurazione robot
#@@@ Correggere i valori di axle e wheel secondo la guida riportata qui:
# Measuring and validating the robot dimensions, https://pybricks.com/ev3-micropython/robotics.html#
robot = DriveBase(left_motor, right_motor, wheel_diameter=wheel, axle_track=axle)


def isGreen(color):
    return (color == Color.GREEN)


def verde(sinistra, destra):
    if sinistra and destra: #se vede doppio verde
        robot.straight(lungCingoli)

        gyro_sensor.reset_angle(0)

        robot.drive(0, 60)

        while gyro_sensor.angle() < 180: print(gyro_sensor.angle())

        robot.drive(0, 0)
    
    elif sinistra and not destra: #se vede verse a sinistra
        robot.straight(lungCingoli)

        gyro_sensor.reset_angle(0)

        robot.drive(0, -60)

        while gyro_sensor.angle() > -89: print(gyro_sensor.angle())

        robot.drive(0, 0)

    else: #se vede verde a destra
        robot.straight(lungCingoli)

        gyro_sensor.reset_angle(0)

        robot.drive(0, 60)

        while gyro_sensor.angle() < 89: print(gyro_sensor.angle())

        robot.drive(0, 0)






while True:
    gl = isGreen(color_sensor_left.color())
    gr = isGreen(color_sensor_right.color())


    if gl or gr:
        verde(gl, gr)

    left_motor.dc((maxSpeed / 7) * 0.5)
    right_motor.dc((maxSpeed / 7) * 0.5)

    
    
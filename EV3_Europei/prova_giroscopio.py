#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor, InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile


wheel = 30

axle = 150

# Motore grande destra
right_motor = Motor(Port.A)

# Motore grande sinistra
left_motor = Motor(Port.B)

robot = DriveBase(right_motor, left_motor, wheel_diameter = wheel, axle_track = axle)

gyro_sensor = GyroSensor(Port.S1)



while True:

    gyro_sensor.reset_angle(0)

    robot.drive(0, 60)

    while gyro_sensor.angle() > -360:
        pass
    robot.drive(0, 0)
    #wait(1000)

    gyro_sensor.reset_angle(0)

    robot.drive(0, -60)

    while gyro_sensor.angle() < 360:
        pass
    robot.drive(0, 0)
    #wait(1000)
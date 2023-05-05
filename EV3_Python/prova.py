#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor, InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile



# Diametro ruota in mm
wheel = 30

# Distanza dal centro delle ruote da sinistra a destra
axle = 160

# Motore grande destra
right_motor = Motor(Port.A)

# Motore grande sinistra
left_motor = Motor(Port.B)

# Sensore di colore destra
color_sensor_right = ColorSensor(Port.S2)

# Sensore di colore sinistra
color_sensor_left = ColorSensor(Port.S3)

# Sensore in luce riflessa fronte
#light_sensor_front = ColorSensor(Port.S4)

#Sensore in colore trasformato fronte
#color_sensor_front = ColorSensor(Port.S4)

# Sensore ultrasuoni
# ultrasonic_sensor = UltrasonicSensor(Port.S1)

# Configurazione robot
robot = DriveBase(left_motor, right_motor, wheel_diameter=wheel, axle_track=axle)

maxpower = 1020 





    #robot.straight(100) #muovi dritto
    #wait(500)
    #right_motor.run_angle(300, 500)
    #wait(500)

    # robot.settings(30, 100, 90)

    # robot.turn(90) 
    # robot.turn(-90) #gira di 90 gradi senso antiorario

    # robot.stop()
# while True:
#     left_motor.run(300)
#     right_motor.run(300)
# stampa = True

# while True:

    

#     colorl = color_sensor_left.color()
    
#     colorr = color_sensor_right.color()
    
#     if stampa == True:
#         print(right_motor.speed())
#         print(colorl)
#         print(colorr)
    
#     if colorl == Color.BLACK:
#         left_motor.hold()
#         while color_sensor_left.color() == Color.BLACK:
#             left_motor.run(-408)
#             right_motor.run(510)

#     elif colorr == Color.BLACK:
#         right_motor.hold()
#         while color_sensor_right.color() == Color.BLACK:
#             right_motor.run(-408)
#             left_motor.run(510)

#     # elif colorr == Color.WHITE and colorl == Color.WHITE and

#     else: # colorl != Color.BLACK and colorr != Color.BLACK:

#         left_motor.run(408)
#         right_motor.run(408)

#     stampa = not stampa





left_motor.dc(100)
right_motor.dc(-100)

while True:
    pass
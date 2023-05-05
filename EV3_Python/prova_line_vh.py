#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor, InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile

import time

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

# Giroscopio
gyro_sensor = GyroSensor(Port.S1)

# Sensore in luce riflessa fronte
#light_sensor_front = ColorSensor(Port.S4)

#Sensore in colore trasformato fronte
#color_sensor_front = ColorSensor(Port.S4)

# Sensore ultrasuoni
# ultrasonic_sensor = UltrasonicSensor(Port.S1)

# Configurazione robot
robot = DriveBase(left_motor, right_motor, wheel_diameter=wheel, axle_track=axle)

# Motor max power deg/s
motor_maxpower = 1020 

    #robot.straight(100) #muovi dritto
    #right_motor.run_angle(300, 500)
    # robot.settings(30, 100, 90)
    # robot.turn(90) 
    # robot.turn(-90) #gira di 90 gradi senso antiorario
    # robot.stop()


###############
#DEBUG SENSORS
''' 
while True:  
    colorl = color_sensor_left.color()
    colorr = color_sensor_right.color()
    print (colorl)
'''


#motor_maxpower /= 10 #@@@ RIMUOVI 
#mtr_pwr_side_black = -motor_maxpower * 40/100
#mtr_pwr_side_white =  motor_maxpower * 50/100
mtr_pwr_side_black = -motor_maxpower * 50/100
mtr_pwr_side_white =  motor_maxpower * 50/100


stampa = True

def isLine( color ):
    return (color == Color.BLACK or color == Color.BLUE or color == Color.BROWN)

lc = 0; rc = 0
gyro_sensor.reset_angle(0)

while True:  
    colorl = color_sensor_left.color()
    colorr = color_sensor_right.color()
    
    if stampa == True:
        #print(right_motor.speed())
        #print("L: ", colorl, "; Line: ", isLine(colorl))
        #print("R: ", colorr, "; Line: ", isLine(colorr))
        dl = 1 if isLine(colorl) else 0
        dr = 1 if isLine(colorr) else 0
        print ( dl, " ", dr )

    if not isLine(color_sensor_left.color()) and not isLine(color_sensor_right.color()) :
        lc = 0; rc = 0
        gyro_sensor.reset_angle(0)

        left_motor.dc (mtr_pwr_side_white)
        right_motor.dc(mtr_pwr_side_white)

    if isLine(color_sensor_left.color()) :
        lc += 1
        left_motor.dc ( mtr_pwr_side_black )
        right_motor.dc( mtr_pwr_side_white )

    if isLine(color_sensor_right.color()):
        rc += 1
        right_motor.dc( mtr_pwr_side_black )
        left_motor.dc ( mtr_pwr_side_white )

    if lc > 50 or rc > 50:
        angle = gyro_sensor.angle()
        print("Angolo: ", angle)
        if lc > 50:
            print("Curva stretta a sinitra.")
        if rc > 50:
            print("Curva stretta a destra")

        right_motor.hold()
        left_motor.hold()

        #Torno nella posizione prima che cominciasse la curva stretta
        robot.turn(-angle)
        
        #Avanzo di mezzo robot
        lungCingoli = 140

        robot.straight( lungCingoli/2 )

        if lc > 50:
            #robot.turn(-90)
            robot.drive(0, 60)
            while gyro_sensor.angle() >= 0:
                pass
            robot.drive(0, 0)

        else: # if rc > 50:
            #robot.turn(90)
            robot.drive(60, 0)
            while gyro_sensor.angle() >= 0:
                pass
            robot.drive(0, 0)

        lc = 0; rc = 0
        gyro_sensor.reset_angle(0)

        exit()




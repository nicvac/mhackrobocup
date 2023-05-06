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

curvaGomitoSoglia = 75

#Quante volte vedo CONSECUTIVAMENTE una linea, sul sensore sinistro e destro
lc_l = 0; lc_r = 0
gyro_sensor.reset_angle(0)

isLine_l = False; isLine_r = False

while True:  
    color_l = color_sensor_left.color()
    color_r = color_sensor_right.color()

    isLine_l = isLine(color_l)
    isLine_r = isLine(color_r)
    
    if stampa == True:
        #print(right_motor.speed())
        #print("L: ", colorl, "; Line: ", isLine(colorl))
        #print("R: ", colorr, "; Line: ", isLine(colorr))
        dl = 1 if isLine_l else 0
        dr = 1 if isLine_r else 0
        print ( dl, " ", dr )

    #Incremento il contatore se è linea e lo era anche al giro precedente
    lc_l = lc_l + 1 if isLine_l else 0
    lc_r = lc_r + 1 if isLine_r else 0

    #Finchè riesce a correggersi in poche iterazioni, considero la posizione stabile => sono ad angolo 0.
    if max(lc_l, lc_r) <= 4:
        gyro_sensor.reset_angle(0)

    #Nessuno dei due sensori è sulla linea => vado dritto
    if not isLine_l and not isLine_r :
        left_motor.dc (mtr_pwr_side_white)
        right_motor.dc(mtr_pwr_side_white)
    
    else:
        #Almeno uno dei due sensori è sulla linea
        correctLeft = False; correctRight = False
        #Se entrambi sono sulla linea, continuo con la stessa correzione con cui ho cominciato
        if isLine_l and isLine_r:
            if lc_l >= lc_r:
                correctLeft = True;  correctRight = False
            else:
                correctLeft = False; correctRight = True
        #Se solo uno dei due è sulla linea, applico la correzione opportuna
        else:
            correctLeft  = isLine_l
            correctRight = isLine_r 

        if correctLeft: 
            left_motor.dc ( mtr_pwr_side_black )
            right_motor.dc( mtr_pwr_side_white )
        if correctRight:
            right_motor.dc( mtr_pwr_side_black )
            left_motor.dc ( mtr_pwr_side_white )

    #Detection curva a gomito: sono sulla linea da diverse iterazioni: nonostante la correzione continuo a leggere linea.
    # tipico di una curva a gomito
    gomitoSx = lc_l > curvaGomitoSoglia
    gomitoDx = lc_r > curvaGomitoSoglia

    if gomitoSx or gomitoDx:

        print("Curva a gomito a sinitra.") if gomitoSx else print("Curva a gomito a destra")
        # Mi Fermo
        right_motor.hold()
        left_motor.hold()

        #Ripristino l'angolazione a prima che cominciasse la curva a gomito
        angle = gyro_sensor.angle()
        print("Angolo da ripristinare: ", angle)
        
        if gomitoSx:
            right_motor.dc( mtr_pwr_side_black )
            left_motor.dc ( mtr_pwr_side_white )
        else: # if gomitoDx:
            left_motor.dc ( mtr_pwr_side_black )
            right_motor.dc( mtr_pwr_side_white )

        while gyro_sensor.angle() >= 0:
            pass
        right_motor.hold()
        left_motor.hold()

        #Avanzo di mezzo robot, posizionando la curva a gomito sotto il robot, al centro
        lungCingoli = 140
        robot.straight( lungCingoli/2 )

        if gomitoSx:
            pass
            #@@@ IMPLEMENTA SCAN A SINITRA
            #ruota in senso antiorario fino a ritrovare la linea
            exit()
        else:
            pass
            #@@@ IMPLEMENTA SCAN A DESTRA (senso orario)
            exit()

        #Qui ho ritrovato la linea
        lc_l = 0; lc_r = 0
        gyro_sensor.reset_angle(0)


#Ritorna vero se linea
def isLine( color ):
    return (color == Color.BLACK or color == Color.BLUE or color == Color.BROWN)

#Scan orario
def isLine( color ):
    return (color == Color.BLACK or color == Color.BLUE or color == Color.BROWN)

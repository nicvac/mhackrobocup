#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor, InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile

import time

#Ritorna vero se linea
def isLine( color ):
    return (color == Color.BLACK or color == Color.BLUE or color == Color.BROWN)

#Scan
#Ruoto sul mio asse fino a degree angoli fino a centrare la linea fra i due sensori L e R
#Senso orario: degree positivo
def scan( degree ):

    print("Scan di max ", degree, "°")

    # if degree < 0:
    #     motor_scan_degs = motor_max_degs * 0.5 * ( -1)
    # else:
    #     motor_scan_degs = motor_max_degs * 0.5

    motor_scan_degs = motor_max_degs * 0.5 * ( -1 if degree < 0 else 1)
    
    #seleziono il sensore corretto a seconda della scansione oraria/antioraria
    color_sensor = color_sensor_right if degree > 0 else color_sensor_left

    lineLocked = False
    lineMet = False
    linePassed = False

    #Dovo aver scelto il sensore giusto, ruoto su asse fino a incontrare la linea e a sorpassarla
    gyro_sensor.reset_angle(0)
    robot.drive(0, motor_scan_degs)
    deg_abs = abs(degree)
    while abs(gyro_sensor.angle()) < deg_abs and not lineLocked:
        color = color_sensor.color()
        if not lineMet:
            lineMet = isLine(color)
        else:
            linePassed = not isLine(color)
        lineLocked = lineMet and linePassed
        
    robot.drive(0, 0)

    #Se lo scan non ha trovato linee => Torno alla posizione di partenza
    if not lineLocked:
        robot.drive(0, -motor_scan_degs)
        if degree < 0:
            while ( gyro_sensor.angle() < 0 ) : pass
        else:
            while ( gyro_sensor.angle() > 0 ) : pass
        robot.drive(0, 0)

    print("Scan lock ", lineLocked)

    robot.stop()
    return lineLocked



# Diametro ruota in mm
wheel = 32.5

# Distanza dal centro delle ruote da sinistra a destra
axle = 205

# Lunghezza dei cingoli (i due sensori di colore devono essere allineati all'inizio dei cingoli)
lungCingoli = 140

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
#@@@ Correggere i valori di axle e wheel secondo la guida riportata qui:
# Measuring and validating the robot dimensions, https://pybricks.com/ev3-micropython/robotics.html#
robot = DriveBase(left_motor, right_motor, wheel_diameter=wheel, axle_track=axle)

# Motor max power deg/s
# Da specifica 1020. Da test arriva a 780 (forse a causa delle batterie scariche)
motor_max_degs = 1020 

###############
#DEBUG SENSORS
''' 
while True:  
    colorl = color_sensor_left.color()
    colorr = color_sensor_right.color()
    print (colorl, " ",colorr)
'''

motor_max_degs /= 2 #@@@ RIMUOVI 
#mtr_side_black_degs = -motor_max_degs * 40/100
#mtr_side_white_degs =  motor_max_degs * 50/100
mtr_side_black_degs = -motor_max_degs * 50/100
mtr_side_white_degs =  motor_max_degs * 50/100

stampa = True

#Dopo X correzioni, se vedo ancora linea sullo stesso sensore per X volte ==> è una curva a gomito
curvaGomitoSoglia = 45 #50 originale, 35 seconda

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
        left_motor.dc(mtr_side_white_degs)
        right_motor.dc(mtr_side_white_degs)
    
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
            left_motor.dc ( mtr_side_black_degs )
            right_motor.dc( mtr_side_white_degs )
        if correctRight:
            right_motor.dc( mtr_side_black_degs )
            left_motor.dc ( mtr_side_white_degs )

    #Detection curva a gomito: sono sulla linea da diverse iterazioni: nonostante la correzione continuo a leggere linea.
    # tipico di una curva a gomito
    gomitoSx = lc_l > curvaGomitoSoglia
    gomitoDx = lc_r > curvaGomitoSoglia

    if gomitoSx or gomitoDx:

        print("Curva a gomito a sinitra.") if gomitoSx else print("Curva a gomito a destra")
        # Mi Fermo
        right_motor.hold()
        left_motor.hold()

        #Ripristino la posizione allo stesso angolo di quando ero stabile (prima della curva a gomito)
        angle = gyro_sensor.angle()
        print("Angolo da ripristinare: ", angle)
        
        if gomitoSx:
            right_motor.dc( mtr_side_black_degs )
            left_motor.dc( mtr_side_white_degs )
        else: # if gomitoDx:
            left_motor.dc( mtr_side_black_degs )
            right_motor.dc( mtr_side_white_degs )

        current_angle = gyro_sensor.angle()
        if current_angle < 0:
            while gyro_sensor.angle() < 0: pass
        else:
            while gyro_sensor.angle() > 0: pass



        #while abs(gyro_sensor.angle()) >= 2 : pass
        right_motor.hold()
        left_motor.hold()

        #Avanzo di mezzo robot, posizionando la curva a gomito sotto il robot, al centro
        robot.straight( lungCingoli/4 )

        #Avendo il vertice della curva a gomito sotto il mio asse perpendicolare, eseguo uno scan
        lineLocked = False
        #ruota in senso orario o antiorario (a seconda della curva a gomito) fino a ritrovare la linea
        
        scanDegree = 170 * (-1 if gomitoSx else 1)
        

        lineLocked = scan(scanDegree)
        if not lineLocked:
            #Si mette male... non ho trovato la linea dove mi sarei aspettato. Provo dall'altra parte
            lineLocked = scan(-scanDegree)

        if lineLocked :
            #Qui ho ritrovato la linea
            lc_l = 0; lc_r = 0
            gyro_sensor.reset_angle(0)
        else:
            print("MI SONO PERSO DOPO LA CURVA A GOMITO.")
            #@@@ GESTIRE QUESTO CASO.
            quit()



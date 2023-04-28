#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor, InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile

#
#
# Configurazione robot
#
#

# Diametro ruota in mm
wheel = 30

# Distanza dal centro delle ruote da sinistra a destra
axle = 150

# Motore grande destra
right_motor = Motor(Port.A)

# Motore grande sinistra
left_motor = Motor(Port.B)

# Sensore di colore destra
color_sensor_right = ColorSensor(Port.S2)

# Sensore di colore sinistra
color_sensor_left = ColorSensor(Port.S3)

# Sensore in luce riflessa fronte
light_sensor_front = ColorSensor(Port.S4)

#Sensore in colore trasformato fronte
color_sensor_front = ColorSensor(Port.S4)

# Sensore ultrasuoni
ultrasonic_sensor = UltrasonicSensor(Port.S1)

# Configurazione robot
robot = DriveBase(left_motor, right_motor, wheel_diameter=wheel, axle_track=axle)



#
#
# Dichiarazione variabili codice
#
#

# Valore percentuale del bianco
white = 60

# Valore percentuale del nero
black = 9

# Valore percentuale della carta riflettente
silver = 100

threshold = (black + white + silver) / 2

# Counter curve effettuate in evacuation zone per rilasciare il rescue kit e le palline. 
couter_curve = 0

# Costante per curva a 70 gradi per aggirare l'ostacolo
curva_ostacolo = 70 * (axle / wheel)

# Costante per curva a 90 gradi
curva_90 = 90 * (axle / wheel)

# costante per curva a 30 gradi. Volendo si può fare una funzione in cui inserisco il valore della curva, così il codice viene più ordinato
curva_30 = 30 * (axle / wheel)

# Costante pi greco per calcolare la distanza in cm percorsa dal robot
pi = 3.1415926535897

# Distanza da percorrere per far arrivare i sensori di dietro a fare il check sulla linea argentata
check_distance = (5 * 360) / (pi * wheel)

# Angolo di 15 gradi per controllare se sotto il robot c'è la linea nera o no
curva_check_linea_ostacolo = 15 * (axle / wheel)

# Quante volte ha visto il verde nella stanza
verdi_visti = 0

# Quante volte ha visto il rosso nella stanza
rossi_visti = 0

# Flag per eseguire o no la scansione
flag_scan = True

# Gradi per la scansione quando perde la linea
e = 50




#
#
# Dichiarazione funzioni codice
#
#

# rilascio rescue kit
def rescue_kit():
    return 0
    # # Muovi per 3 secondi a velocità -40 -40
    # # Muovi per 2.9 rotazioni a velocità -30 30
    # # Muovi per 3 secondi a velocità -40 -40
    # # Muovi per 135 gradi alla velocità 75%
    # wait(500)
    # # Muovi per -135 gradi alla velocità 75%
    # wait(500)
    # # Muovi per 135 gradi alla velocità 75%
    # wait(500)
    # # Muovi per -135 gradi alla velocità 75%
    # wait(500)
    # # Muovi per 135 gradi alla velocità 75%
    # wait(500)
    # # Muovi per -135 gradi alla velocità 75%
    # wait(500)


#def uscita_rescue_kit():
    # Muovi per 3 secondi alla velocità 40 40
    # Muovi per 2.9 rotazioni alla velocità 30 -30


# evacuation zone
def stanza():
    return 0
#     if color_sensor_front.color() == Color.BLACK:
#         return 0
#     wait(300)
#     # Muovi per 1.5 secondi a velocità 30 30
#     wait(1000)
#     first_distance = ultrasonic_sensor.distance()
#     # Muovi per 30 gradi a velocità 30 -30
#     wait(1000)
#     wall_distance = ultrasonic_sensor.distance()
#     if wall_distance < first_distance:
#         curva = -1
#     else:
#         curva = 1
#     # Muovi per 30 gradi a velocità 30 -30
#     while True:
#         # Start movint at 30 30 speed
#         if color_sensor_front.color() == Color.GREEN and counter_curve == 0:
#             rescue_kit()
#             uscita_rescue_kit()
#         elif color_sensor_front.color() == Color.GREEN and counter_curve > 1:
#             rescue_kit()
#             uscita_rescue_kit()
#             # Muovi per (2.8 * curva * -1) rotazioni a velocità 20 -20
#         elif color_sensor_front.color() == Color.RED or color_sensor_front.color() == Color.YELLOW and counter_curve == 0:
#             counter_curve = 2
#             # Muovi per 1.4 * curva rotazioni a velocità 20 -20
#             # Muovi per 2 secondi a velocità 25 25
#             # Muovi per 1.4 * curva rotazioni a velocità 20 -20
#             curva = curva * -1
#         elif color_sensor_front.color() == Color.RED or color_sensor_front.color() == Color.YELLOW and counter_curve > 1 and verdi_visti == 0:
#             # Muovi per 2.8 * curva * -1 rotazioni a velocità 20 -20
#         elif color_sensor_front.color() == Color.RED or color_sensor_front.color() == Color.YELLOW and counter_curve > 1 and verdi_visti > 0:
#             # Muovi per 2 rotazioni a velocità -30 -30
#             return 0
#         elif ultrasonic_sensor.distance() < 6:
#             # Muovi per 1.4 * curva rotazioni a velocità 20 -20
#             # Muovi per 2 secondi a velocità 25 25
#             # Muovi per 1.4 * curva rotazioni a velocità 20 -20
#             curva = curva * -1
#             counter_curve += 1

    



# aggira ostacolo
def ostacolo():
    return 0
    # # Muovi per "curva_ostacolo" gradi a velocità -30 30
    # if color_sensor_right.color() == Color.BLACK or color_sensor_left.color() == Color.BLACK:
    #     # Muovi per "curva_ostacolo" * -1 gradi alla velocità -30 30
    #     aggira()
    #     return 0

    # else:
    #     # Muovi per "curva_ostacolo" * -1 gradi alla velocità -30 30
    #     # Muovi per "curva_ostacolo" * -1 gradi alla velocità -30 30
        
    #     if color_sensor_right.color() == Color.BLACK or color_sensor_left.color() == Color.BLACK:
    #     # Muovi per "curva_ostacolo" * -1 gradi alla velocità -30 30
    #     aggira()
    #     return 0

    #     else:
    #         # Muovi per 3 rotazioni a velocità -30 -30 (agguingere il blocco in cui si rimette dritto)
    #         stanza()


# scansione per aggirare la linea
def scan():
    i = 0
    robot.straight(20)
    while color_sensor_right.color() != Color.BLACK  or color_sensor_left.color() != Color.BLACK or color_sensor_right.color() != Color.BLACK or color_sensor_left.color() != Color.BLACK or light_sensor_front.reflection() < 40:
        if i < 13:
            # Muovi per "e" gradi a velocità 60 -60
            robot.settings(30, 100, 5)
            robot.turn(60)
            robot.stop()
        elif i < 35:
            # Muovi per "e" gradi a velocità -60 60 
            robot.settings(30, 100, 5)
            robot.turn(-60)
            robot.stop()
        else:
            # Muovi per  500 gradi a velocità 60 -60
            robot.settings(30, 100, 60)
            robot.turn(60)
            robot.stop()
            # Muovi per 0.5 rotazioni a velocità 50 50
            robot.straight(20)
            i = 0
        i += 1




#
#
# Main
#
#

while True: 
    if light_sensor_front.reflection() > 95:
        # Aggiungere doppio check sensore
        stanza()
    elif light_sensor_front.reflection() < 10 and color_sensor_right.color() == Color.BLACK and color_sensor_left.color() == Color.BLACK:
        flag_scan = True
        # Muovi per 0.5 secondi alla velocità 30 30
        robot.straight(20)
    elif color_sensor_right.color() == Color.BLACK or color_sensor_right.color() == Color.BLUE:
        # Start moving at -40 50 speed
        left_motor.coast(-50)
        right_motor.coast(40)
        flag_scan = True
    elif color_sensor_left.color() == Color.BLACK or color_sensor_left.color() == Color.BLUE:
        # Start moving at 50 -40 speed
        left_motor.coast(50)
        right_motor.coast(-40)
        flag_scan = True
    elif color_sensor_right.color() == Color.GREEN and color_sensor_left.color() == Color.GREEN:
        # Muovi per 2.27 secondi alla velocità -50 50
        robot.settings(30, 100, 180)
        robot.turn(50)
        robot.stop()
    elif color_sensor_right.color() == Color.GREEN:
        # Muovi per 1 secondo alla velocità -20 60
        robot.settings(30, 100, 90)
        robot.move(30)
        robot.stop()
    elif color_sensor_left.color() == Color.GREEN:
        # Muovi per 1 secondo alla velocità 60 -20
        robot.settings(30, 100, 90)
        robot.move(-30)
        robot.stop()
    elif color_sensor_right.color() == Color.WHITE and color_sensor_left.color() == Color.WHITE and light_sensor_front.reflection() > 50 and light_sensor_front.reflection() < 90 and flag_scan == True:
        scan()
    elif ultrasonic_sensor.distance() < 5: # Da sostituire con distanza 1 minore di 5 cm
        ostacolo()
    else:
        # Start moving at 40 40 
        left_motor.coast(40, 40)
        right_motor.coast(40, 40)

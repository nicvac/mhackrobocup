#!/usr/bin/env pybricks-micropython

from rescue_line_functions import *
from rescue_line_setup import * 



found = False
flag = 0
turn_side = 1

gyro_sensor.reset_angle(0)

# lato da cui fare il lato del controllo. Se è 1 gira a destra, se è -1 gira a sinistra
side = 1

left_motor.dc(-50)
right_motor.dc(-50)

# ci siamo persi, inizia ad andare indietro finchè almeno uno dei due sensori vede nero
while True:
    color_l = color_sensor_left.color()
    color_r = color_sensor_right.color()

    isLine_l = isLine(color_l)
    isLine_r = isLine(color_r)

    if isLine_l or isLine_r:
        break



# se il sinistro ha visto la linea vuol dire che deve iniziare a fare il controllo a destra (-1)
if isLine_l and not isLine_r:
    side = -1
# se il destrro ha visto la linea vuol dire che deve iniziare a farer il controllo a sinistra (1)
elif isLine_r and not isLine_l:
    side = 1
# coprire anche il caso in cui entrambi i sensori l'hanno vista contemporaneamente

# fa un passetto in avanti per spostarsi dalla linea, sennò inizia lo scan e vede già la linea
robot.straight(50)
robot.stop()

found = False

# finchè non trova la linea
while found == False:

    gyro_sensor.reset_angle(0)
    
    if side == 1:
        print("Controlla a destra")
        left_motor.dc(100)
        right_motor.dc(17)
    else:
        print("Controlla a sinistra")
        left_motor.dc(17)
        right_motor.dc(100)
    
    # angolo 80 a velocità 100 - 17 dovrrebbe riprendere la linea 20 cm dopo, ma non funziona.
    # continua a girere o finchè non raggiunge gli 80 gradi o finchè uno dei tre sensori vede la linea
    while abs(gyro_sensor.angle()) < 80 and found == False:
        color_l = color_sensor_left.color()
        color_r = color_sensor_right.color()
        color_f = light_sensor_front.color()

        isLine_l = isLine(color_l)
        isLine_r = isLine(color_r)
        isLine_f = isLine(color_f)

        if isLine_l or isLine_r or isLine_f:
            found = True
        else:
            found = False

    left_motor.hold()
    right_motor.hold()
    

    # caso in cui non ha trovato la linea dopo gli 80 gradi
    if found == False:
        print("Ho fatto 80 gradi e non ho trovato nessuna linea")
        
        # se ha fatto il controllo a destra torna indietro prendendo la posizione iniziale
        # quando ritorna a 80 gradi (posizione iniziale) moltiplica il contatore per -1
        if side == 1:
            print("Torno indietro da destra")
            gyro_sensor.reset_angle(0)
            left_motor.dc(-100)
            right_motor.dc(-15)
            while abs(gyro_sensor.angle()) < 80:
                pass
            left_motor.hold()
            right_motor.hold()
            side *= -1
            continue

        # se ha fatto il controllo a sinistra torna indietro prendendo la posizione iniziale
        # quando ritorna a 80 gradi (posizione iniziale) moltiplica il contatore per -1
        elif side == -1:
            print("Torna indietro da sinistra")
            gyro_sensor.reset_angle(0)
            left_motor.dc(-15)
            right_motor.dc(-100)
            while abs(gyro_sensor.angle()) < 80:
                pass
            left_motor.hold()
            right_motor.hold()
            side *= -1
            continue
    
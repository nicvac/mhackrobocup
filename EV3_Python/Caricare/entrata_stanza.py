#!/usr/bin/env pybricks-micropython
from rescue_line_functions import *
from rescue_line_setup import *

def isStagnola(reading):
    return True if reading == 100 else False


def stanza():
    pass

def resetAngle():
    angle = gyro_sensor.angle()

    if angle > 0:
        ruotaSuAsse(-1)
    else:
        ruotaSuAsse(1)

    if angle > 0:
        while gyro_sensor.angle() > 0: pass
        stop()
    else:
        while gyro_sensor.angle() < 0: pass
        stop()


def resetAngleBack(firstAngle):
    if gyro_sensor.angle() > firstAngle:
        ruotaSuAsse(-1)
        while gyro_sensor.angle() > firstAngle: pass
        stop()
    else:
        ruotaSuAsse(1)
        while gyro_sensor.angle() < firstAngle: pass
        stop()


dritto()

while True:
    lightFront = light_sensor_front.reflection()
    stagnola = isStagnola(lightFront)
    
    if stagnola:
        print("Ho visto la luminosità maggiore del 90%")
        robot.drive(0,0)
        stop()
        break
    else:
        pass

if stagnola:
    angleStagnola = gyro_sensor.angle()
    resetAngle()    
    # far andare dritto il robot finchè anche i sensori di dietro vedono la stagnola, prendere bene le misure
    robot.straight(43)
    time.sleep(1)
    lightL = color_sensor_left.reflection()
    lightR = color_sensor_right.reflection()
    stagnolaL = isStagnola(lightL)
    stagnolaR = isStagnola(lightR)

    print("Luminosità sinistra: ", lightL, " Luminosità destra: ", lightR)
    if stagnolaL and stagnolaR:
        print("Ho trovato la stanza mader fader ")
        
    else:
        # non c'è la stanza. Riprendo l'angolo a prima che ho trovato la stagnola e vado avanti, sperando che non mi incastro nelle rampe mannaggia
        print("Non ho trovato la stanza azzo ")
        robot.straight(-40)
        resetAngleBack(angleStagnola)
        # Ignorare la lettura del sensore davanti per qualche secondo. sennò torna indietro e siamo punto e a capo


# while True:
#     print("Sinistra: ", color_sensor_left.reflection(), " Destra: ", color_sensor_right.reflection(), " Fronte: ", light_sensor_front.reflection())
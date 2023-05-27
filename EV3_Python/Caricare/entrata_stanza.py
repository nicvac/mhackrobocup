#!/usr/bin/env pybricks-micropython
from rescue_line_functions import *
from rescue_line_setup import *

def isStagnola(reading):
    return True if reading == 100 else False


def stanza():
    pass

lightFront = light_sensor_front.reflection()

stagnola = isStagnola(lightFront)

if stagnola:
    currentAngle = gyro_sensor.angle()
    resetAngleGreen()
    # far andare dritto il robot finchè anche i sensori di dietro vedono la stagnola, prendere bene le misure
    robot.straight(50)
    lightL = color_sensor_left.reflection()
    lightR = color_sensor_right.reflection()
    stagnolaL = isStagnola(lightL)
    stagnolaR = isStagnola(lightR)

    if stagnolaL and stagnolaR:
        stanza()
    else:
        # non c'è la stanza. Riprendo l'angolo a prima che ho trovato la stagnola e vado avanti, sperando che non mi incastro nelle rampe mannaggia
        robot.straight(-50)
        resetBackAngleAfterNoGreen(currentAngle)
        # Ignorare la lettura del sensore davanti per qualche secondo. sennò torna indietro e siamo punto e a capo

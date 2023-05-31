#!/usr/bin/env pybricks-micropython
from rescue_line_setup import *
from math import *
from rescue_line_functions import *
from client_functions import *

def getRoomSize(storicoDimensioneSx, storicoDimensioneDx):
    distTraSensori = 14
    sx = getDistanceCm(DIST_LEFT)
    dx = getDistanceCm(DIST_RIGHT)
    storicoDimensioneSx.append(sx)
    storicoDimensioneDx.append(dx)
    somma = sx + dx + distTraSensori
    return somma


def guadagnaCentro():
    #Avanza di 45 cm 
    robot.reset()
    robot.drive(70, 0)
    storicoDimensioneSx = []
    storicoDimensioneDx = []
    dimMaggiore = 120
    dimMinore = 80
    asseMaggiore = True
    distTraSensori = 14
    distanzaSx = 0
    distanzaDx = 0
    contDimMinore = 0
    contDimMaggiore = 0
    distanzaSxminore = 0
    distanzaDxminore = 0
    distanzaSxmaggiore = 0
    distanzaDxmaggiore = 0

    while(robot.distance() < 530):
        print(str(robot.distance()) + "  " + str(getRoomSize(storicoDimensioneSx, storicoDimensioneDx)))
    robot.stop()

    for i in range(len(storicoDimensioneSx)):
        if(abs(storicoDimensioneSx[i] + storicoDimensioneDx[i] + distTraSensori - dimMinore) < 3):
            distanzaSxminore = storicoDimensioneSx[i]
            distanzaDxminore = storicoDimensioneDx[i]
            contDimMinore += 1
            

        if(abs(storicoDimensioneSx[i] + storicoDimensioneDx[i] + distTraSensori - dimMaggiore) < 3):
            asseMaggiore = False
            distanzaSxmaggiore = storicoDimensioneSx[i]
            distanzaDxmaggiore = storicoDimensioneDx[i]
            contDimMaggiore += 1
            
        print(str(storicoDimensioneSx[i]) + " - " + str(storicoDimensioneDx[i]))

    print("Contaori: ", contDimMinore, " ", contDimMaggiore)
    if(contDimMaggiore > contDimMinore): 
        asseMaggiore = False
        distanzaSx = distanzaSxmaggiore
        distanzaDx = distanzaDxmaggiore
    else:
        distanzaSx = distanzaSxminore
        distanzaDx = distanzaDxminore

    if (asseMaggiore):
        print("Avanzando di 15cm")
        robot.reset()
        robot.drive(70, 0)

        while(robot.distance() < 150):
            pass
        robot.stop()    

    gyro_sensor.reset_angle(0)

    print("Sx: " + str(distanzaDx) + " Dx: " + str(distanzaDx))

    if(contDimMaggiore < contDimMinore):
        robot.drive(0, 30)
    else:
        robot.drive(0, -30)

    while(abs(gyro_sensor.angle()) < 90):
        pass

    robot.stop()


    robot.reset()
    robot.drive(70, 0)

    print("Ultimo avanzameto")
    print(abs(distanzaSx - distanzaDx) / 2)
    while(robot.distance() < (abs(distanzaSx - distanzaDx) / 2) * 10):
        pass

    robot.stop()


#!/usr/bin/env pybricks-micropython
from rescue_line_setup import *
from math import *
from rescue_line_functions import *
from client_functions import *

def getRoomSize(storicoDimensioneSx, storicoDimensioneDx):
    distTraSensori = 15
    sx = getDistanceCm(DIST_LEFT)
    time.sleep(0.3)
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
    dimMinore = 90
    asseMaggiore = True
    distTraSensori = 15
    distanzaSx = 0
    distanzaDx = 0
    contDimMinore = 0
    contDimMaggiore = 0
    distanzaSxminore = 0
    distanzaDxminore = 0
    distanzaSxmaggiore = 0
    distanzaDxmaggiore = 0
    dimTriangolo1 = 0
    dimTriangolo2 = 0
    
    #Spengo i sensori che non mi servono
    sensorOff(DIST_FRONT_OFF)
    time.sleep(0.5)
    sensorOff(DIST_BACK_OFF)
    time.sleep(0.5)

    #FARE alcune letture a vuoto! E' importante per stabilizzare il sensore
    for i in range(4):
        currCm = getDistanceCm(DIST_LEFT)
        time.sleep(0.5)
        currCm = getDistanceCm(DIST_RIGHT)
        time.sleep(0.5)


    print("sto cazzo")
    while(robot.distance() < 530):
        print(str(robot.distance()) + "  " + str(getRoomSize(storicoDimensioneSx, storicoDimensioneDx)))
    robot.stop()

    dimTriangolo1 = 53

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
        dimTriangolo1 += 15

    if (asseMaggiore):
        print("Avanzando di 15cm")
        robot.reset()
        robot.drive(70, 0)

        while(robot.distance() < 150):
            pass
        robot.stop()    

    gyro_sensor.reset_angle(0)

    print("Sx: " + str(distanzaSx) + " Dx: " + str(distanzaDx))

    if(distanzaSx > distanzaDx):
        robot.drive(0, 30)
    else:
        robot.drive(0, -30)

    while(abs(gyro_sensor.angle()) < 90):
        pass

    robot.stop()


    print("Ultimo avanzameto")
    dimTriangolo2 = (abs(distanzaSx - distanzaDx) + distTraSensori - 6) / 2
    angolo = degrees(acos(dimTriangolo2 / sqrt(dimTriangolo1 ** 2 + dimTriangolo2 ** 2)))
    print("dimTriangolo1: ", dimTriangolo1, " - dimTriangolo2: ", dimTriangolo2, " - angolo: ", angolo)

    robot.reset()
    robot.drive(70, 0)

    while(robot.distance() < dimTriangolo2 * 10):
        pass

    robot.stop()

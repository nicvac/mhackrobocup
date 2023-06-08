#!/usr/bin/env pybricks-micropython
from rescue_line_setup import *
from math import *
from rescue_line_functions import *
from client_functions import *

def getRoomSize(storicoDimensioneSx, storicoDimensioneDx):
    global contMaggiore90
    global contMinore90
    distTraSensori = 15
    sx = getDistanceCm(DIST_LEFT)
    dx = getDistanceCm(DIST_RIGHT)
    time.sleep(0.1) #0.3
    if sx == 255.0:
        sx = 2
    if dx == 255.0:
        dx = 2
    storicoDimensioneSx.append(sx)
    storicoDimensioneDx.append(dx)
    somma = sx + dx + distTraSensori
    if somma > 92: contMaggiore90 += 1
    else: contMinore90 += 1
        
    return somma


def guadagnaCentro():

    robot.straight(530)
    robot_gyro_turn(-90)
    robot.straight(400)

    # #Avanza di 45 cm
    # robot.reset()
    # storicoDimensioneSx = []
    # storicoDimensioneDx = []
    # dimMaggiore = 120
    # dimMinore = 90
    # asseMaggiore = True
    # distTraSensori = 15
    # distanzaSx = 0
    # distanzaDx = 0
    # contDimMinore = 0
    # contDimMaggiore = 0
    # distanzaSxminore = 0
    # distanzaDxminore = 0
    # distanzaSxmaggiore = 0
    # distanzaDxmaggiore = 0
    # dimTriangolo1 = 0
    # dimTriangolo2 = 0
    # contMaggiore90 = 0
    # contMinore90 = 0
    
    # #Spengo i sensori che non mi servono
    # sensorOff(DIST_FRONT_OFF)
    # time.sleep(0.5)
    # sensorOff(DIST_BACK_OFF)
    # time.sleep(0.5)

    # #FARE alcune letture a vuoto! E' importante per stabilizzare il sensore
    # for i in range(206):
    #     currCm = getDistanceCm(DIST_LEFT)
    #     time.sleep(0.5)
    #     currCm = getDistanceCm(DIST_RIGHT)
    #     time.sleep(0.5)

    # robot.drive(70, 0)
    # print("sto cazzo")
    # while(robot.distance() < 530):
    #     print(str(robot.distance()) + "  " + str(getRoomSize(storicoDimensioneSx, storicoDimensioneDx)))
    # robot.stop()

    # dimTriangolo1 = 53

    # for i in range(len(storicoDimensioneSx)):
    #     if(abs(storicoDimensioneSx[i] + storicoDimensioneDx[i] + distTraSensori - dimMinore) < 3):
    #         distanzaSxminore = storicoDimensioneSx[i]
    #         distanzaDxminore = storicoDimensioneDx[i]
    #         contDimMinore += 1
            

    #     if(abs(storicoDimensioneSx[i] + storicoDimensioneDx[i] + distTraSensori - dimMaggiore) < 3):
    #         asseMaggiore = False
    #         distanzaSxmaggiore = storicoDimensioneSx[i]
    #         distanzaDxmaggiore = storicoDimensioneDx[i]
    #         contDimMaggiore += 1
            
    #     print(str(storicoDimensioneSx[i]) + " - " + str(storicoDimensioneDx[i]))

    # print("Contaori: ", contDimMinore, " ", contDimMaggiore)
    # if(contDimMaggiore > contDimMinore): 
    #     asseMaggiore = False
    #     distanzaSx = distanzaSxmaggiore
    #     distanzaDx = distanzaDxmaggiore
    # else:
    #     if contDimMaggiore == 0 and contDimMinore == 0:
    #         if contMaggiore90 > contMinore90:
    #             asseMaggiore = False
    #         else:
    #             dimTriangolo1 += 15
    #         distanzaSx = getDistanceCm(DIST_LEFT)
    #         distanzaDx = getDistanceCm(DIST_RIGHT)
    #     else:
    #         distanzaSx = distanzaSxminore
    #         distanzaDx = distanzaDxminore
    #         dimTriangolo1 += 15
    

    # if (asseMaggiore):
    #     print("Avanzando di 15cm")
    #     robot.reset()
    #     robot.drive(70, 0)

    #     while(robot.distance() < 150):
    #         pass
    #     robot.stop()    

    # gyro_sensor.reset_angle(0)

    # print("Sx: " + str(distanzaSx) + " Dx: " + str(distanzaDx))

    # if(distanzaSx > distanzaDx):
    #     robot.drive(0, 30)
    # else:
    #     robot.drive(0, -30)

    # while(abs(gyro_sensor.angle()) < 90):
    #     pass

    # robot.stop()


    # print("Ultimo avanzameto")
    # dimTriangolo2 = (abs(distanzaSx - distanzaDx) + distTraSensori - 6) / 2
    # angolo = degrees(acos(dimTriangolo2 / sqrt(dimTriangolo1 ** 2 + dimTriangolo2 ** 2)))
    # print("dimTriangolo1: ", dimTriangolo1, " - dimTriangolo2: ", dimTriangolo2, " - angolo: ", angolo)

    # robot.reset()
    # robot.drive(70, 0)

    # while(robot.distance() < dimTriangolo2 * 10):
    #     pass

    # robot.stop()

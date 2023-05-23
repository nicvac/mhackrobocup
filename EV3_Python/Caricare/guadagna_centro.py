#!/usr/bin/env pybricks-micropython
from rescue_line_setup import *
from math import *
from rescue_line_functions import *

def getRoomSize():
    global distTraSensori
    sx = getDistanceCm(2)
    dx = getDistanceCm(3)
    storicoDimensioneSx.append(sx)
    storicoDimensioneDx.append(dx)
    somma = sx + dx + distTraSensori
    return somma

def getDistanceMM(sensore):
        extDist.send(sensore)
        extDist.wait()
        return extDist.read()

def getDistanceCm(sensore):
    curr = getDistanceMM(sensore) / 10
    #print(curr)
    return curr

#Avanza di 45 cm 
robot.reset()
robot.drive(70, 0)
storicoDimensioneSx = []
storicoDimensioneDx = []
dimMaggiore = 120
dimMinore = 80
asseMaggiore = True
distTraSensori = 17
distanzaSx = 0
distanzaDx = 0

while(robot.distance() < 530):
    print(str(robot.distance()) + "  " + str(getRoomSize()))
robot.stop()

for i in range(len(storicoDimensioneSx)):
    if(abs(storicoDimensioneSx[i] + storicoDimensioneSx[i] + distTraSensori - dimMinore) < 4):
        distanzaSx = storicoDimensioneSx[i]
        distanzaDx = storicoDimensioneDx[i]

    if(abs(storicoDimensioneSx[i] + storicoDimensioneSx[i] + distTraSensori - dimMaggiore) < 4):
        asseMaggiore = False
        distanzaSx = storicoDimensioneSx[i]
        distanzaDx = storicoDimensioneDx[i]
        break

if (asseMaggiore):
    print("Avanzando di 15cm")
    robot.reset()
    robot.drive(70, 0)

    while(robot.distance() < 150):
         pass
    robot.stop()    

gyro_sensor.reset_angle(0)

if(distanzaSx < distanzaDx):
    robot.drive(0, 30)
else:
    robot.drive(0, -30)

while(abs(gyro_sensor.angle()) < 90):
    pass

robot.stop()


robot.reset()
robot.drive(70, 0)

print("Ultimo avanzameto")
while(robot.distance() < abs(distanzaSx - distanzaDx) / 2):
    pass

'''
avanti = getDistanceCm(1)
dietro = getDistanceCm(4)
while(abs(avanti - dietro) > 3):
    print(str(dietro) + " / " + str(avanti))
    avanti = getDistanceCm(1)
    dietro = getDistanceCm(4)
'''

robot.stop()
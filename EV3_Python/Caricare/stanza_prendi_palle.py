#!/usr/bin/env pybricks-micropython
from rescue_line_setup import *
from math import *
from rescue_line_functions import *
from client_functions import *

#La distanza finale fra robot e oggetto da raggiungere
distFinaleCm = 2.0

#La distanza fra il robot e la pallina da catturare
distPallina = 7.0

# MAIN

evac_motor_scan_degs = 30
evac_motor_scan_degs /= 3

evac_motor_go_degs = 40

distanza_precedente=500 #pallina.distance
distanza_attuale=getDistanceCm(DIST_BACK)


# robot.drive(0, -10)
# gyro_sensor.reset_angle(0)
# while gyro_sensor.angle() > -180:
#     print(gyro_sensor.angle())

# robot.drive(0, 0)
# quit
targetCm=9
noCorrCm=min(getDistanceCm(DIST_BACK)*(2/3), getDistanceCm(DIST_BACK)-targetCm)
print("Avanzo senza correzioni di: ", noCorrCm)
robot.straight(-10*noCorrCm)

while getDistanceCm(DIST_BACK) > targetCm :
    print (distanza_precedente," dist att:", distanza_attuale, " angolo:", gyro_sensor.angle())
    if distanza_attuale < distanza_precedente+2.5:
        distanza_precedente=distanza_attuale
        distanza_attuale=getDistanceCm(DIST_BACK)
        robot.drive(-50, 0)
    else:
        i=0
        cazzo=True
        print("Ho perso la pallina")
        gyro_sensor.reset_angle(0)
        while True:
            if gyro_sensor.angle() < 10 and cazzo==True:
                robot.drive(0, 30)
                print ("giro orario: " + str(gyro_sensor.angle()))
            else:
                #robot.stop()
                gyro_sensor.reset_angle(0)
                cazzo=False
                if gyro_sensor.angle() > -20:
                    robot.drive(0, -30)
                    print ("giro antiorario: " + str(gyro_sensor.angle()))
                #else:
                    #non so più dove '''cazzo''' è la palla
                #    break
            if getDistanceCm(DIST_BACK) < distanza_precedente + 2.5 :
                i+=1
                if i==3:
                    # robot.drive(0, -30)
                    # time.sleep(0.1)
                    robot.straight(-10)
                    break

# robot.straight(-45)
robot.drive(0, 0)
robot.stop()
print("Distanza dopo il loop: ", getDistanceCm(DIST_BACK))

robot.straight(10*(targetCm-getDistanceCm(DIST_BACK)))
print("Distanza finale: ", getDistanceCm(DIST_BACK))

for i in range(100):
    print(getDistanceCm(DIST_BACK))


# upper_left_motor.run_angle(700, -130)
# upper_left_motor.hold()
# time.sleep(0.2)
# upper_left_motor.run_angle(300, 130)
# upper_left_motor.hold()

upper_left_motor.reset_angle(0)
while upper_left_motor.angle()>-100:
    upper_left_motor.dc(-100)
    upper_right_motor.dc(-100)

upper_left_motor.hold()
upper_right_motor.hold()
time.sleep(5)
upper_right_motor.stop()
upper_left_motor.run_angle(300, 100)
upper_left_motor.hold()


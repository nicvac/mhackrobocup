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


robot.straight(-10*getDistanceCm(DIST_BACK)*(2/3))


while getDistanceCm(DIST_BACK) > 7 :
    print (str(distanza_precedente) + " dist att:" + str(distanza_attuale) + " angolo:" + str(gyro_sensor.angle()))
    if distanza_attuale < distanza_precedente+2.5:
        distanza_precedente=distanza_attuale
        distanza_attuale=getDistanceCm(DIST_BACK)
        robot.drive(-70, 0)
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
                robot.stop()
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
# upper_left_motor.angle(90)
# upper_left_motor.hold()
# upper_left_motor.angle(-90)
# upper_left_motor.hold()
#!/usr/bin/env pybricks-micropython
from rescue_line_setup import *
from math import *
from rescue_line_functions import *
from client_functions import *

def prendi_palla(distanza_pallina):
    start_dist=robot.distance()

    print("Prendi palla: begin")

    #Spengo sensori per ridurre il rumore
    sensorOff(DIST_FRONT_OFF)
    time.sleep(0.5)
    sensorOff(DIST_LEFT_OFF)
    time.sleep(0.5)
    sensorOff(DIST_RIGHT_OFF)
    time.sleep(0.5)

    for i in range(4):
        dist_cm = getDistanceCm(DIST_BACK)
        print("prendi_palla: Distanza iniziale: ", dist_cm)
        time.sleep(0.5)
    
    #La distanza finale fra robot e oggetto da raggiungere
    distFinaleCm = 2.0

    #La distanza fra il robot e la pallina da catturare
    distPallina = 7.0

    distanza_precedente=500 #distanza_pallina #pallina.distance
    distanza_attuale=getDistanceCm(DIST_BACK)

    # robot.drive(0, -10)
    # gyro_sensor.reset_angle(0)
    # while gyro_sensor.angle() > -180:
    #     print(gyro_sensor.angle())

    # robot.drive(0, 0)
    # quit
    targetCm=9
    noCorrCm=min(getDistanceCm(DIST_BACK)*(2/3), getDistanceCm(DIST_BACK)-targetCm)
    print("prendi_palla: Avanzo senza correzioni di: ", noCorrCm)
    robot.straight(-10*noCorrCm)
    while getDistanceCm(DIST_BACK) > targetCm :
        print ("prendi_palla: dist pre: ", distanza_precedente," dist att:", distanza_attuale, " angolo:", gyro_sensor.angle())
        if distanza_attuale < distanza_precedente+2.5:
            distanza_precedente=distanza_attuale
            distanza_attuale=getDistanceCm(DIST_BACK)
            robot.drive(-50, 0)
        else:
            i=0
            cazzo=True
            print("prendi_palla: Ho perso la pallina")
            gyro_sensor.reset_angle(0)
            while True:
                if gyro_sensor.angle() < 30 and cazzo==True:
                    robot.drive(0, 30)
                    print ("prendi_palla: giro orario: " + str(gyro_sensor.angle()))
                else:
                    #robot.stop()
                    if cazzo==True: gyro_sensor.reset_angle(0)
                    cazzo=False
                    if gyro_sensor.angle() > -60:
                        robot.drive(0, -30)
                        print ("prendi_palla: giro antiorario: " + str(gyro_sensor.angle()))
                    else:
                        robot.stop()
                        print("prendi_palla: non so più dove cazzo è la palla")
                        cazzo=True
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
    print("prendi_palla: Distanza dopo il loop: ", getDistanceCm(DIST_BACK))

    robot.straight(10*(targetCm-getDistanceCm(DIST_BACK)))
    print("prendi_palla: Distanza finale: ", getDistanceCm(DIST_BACK))

    #Catturo palla
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

    # torno indietro
    robot.straight(-(robot.distance()-start_dist))

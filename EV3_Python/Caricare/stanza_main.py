#!/usr/bin/env pybricks-micropython
from rescue_line_setup import *
from rescue_line_functions import *
from client_functions import *

from stanza_wip.stanza_func import *
from stanza_guadagna_centro import *

def rilascia_recue_kit():
    robot_gyro_turn(-90)
    srv_rilascia_rescue_kit()
    time.sleep(5)
    robot_gyro_turn(90)


def stanza_main():
    #Costruisco il Reference data 
    evac_build_ref_data()

    #Alzo il sensore frontale
    intosta_il_pisello()

    #Guadagnp il centro della stanza
    #@@@ NON FUNZIONA
    #@@@guadagnaCentro()

    #Cerco il tipo di triangoli
    triaA_deg = 55
    triaA_cm = deg2cm_tria[triaA_deg]
    robot_gyro_turn(triaA_deg)
    robot.straight(-triaA_cm * 10)
    print("Vado a Triangolo A, mi sposto di ", -triaA_cm, " cm")

    robot_gyro_turn(165)

    #Leggo il colore del triangolo
    color = light_sensor_front.color()
    print("Ho letto ", color)
    if color == Color.RED:        
        rilascia_recue_kit()
    
    robot_gyro_turn(-165)
    print("Torno al centro, mi sposto di ", triaA_cm, " cm")
    robot.straight(triaA_cm * 10)
    robot_gyro_turn(-triaA_deg)

    #@@@ QUI RIPRISTINA L'ANGOLO CHE AVEVA AL CENTRO!


    #@evac_get_ball_main(cm_list, deg_list)

stanza_main()

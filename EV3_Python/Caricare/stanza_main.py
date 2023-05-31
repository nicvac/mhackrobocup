#!/usr/bin/env pybricks-micropython
from rescue_line_setup import *
from rescue_line_functions import *
from client_functions import *

from stanza_wip.stanza_func import *
from stanza_guadagna_centro import *

#Parametri centro
centro_ref_back_cm=0
centro_ref_front_cm=0
centro_ref_left_cm=0
centro_ref_right_cm=0
#Angolo resettato a 0 quando arrivo a centro stanza

ho_lasciato_kit = False

def imposta_centro_ref():
    global centro_ref_back_cm
    global centro_ref_front_cm
    global centro_ref_left_cm
    global centro_ref_right_cm

    gyro_sensor.reset_angle()

    #Spengo i sensori per eliminare il rumore
    sensorOff(DIST_BACK_OFF); time.sleep(0.1)
    sensorOff(DIST_FRONT_OFF); time.sleep(0.1)
    sensorOff(DIST_LEFT_OFF); time.sleep(0.1)
    sensorOff(DIST_RIGHT_OFF); time.sleep(0.1)

    centro_ref_back_cm = getDistanceCm_off(DIST_BACK_OFF); time.sleep(0.1)
    centro_ref_front_cm = getDistanceCm_off(DIST_FRONT_OFF); time.sleep(0.1)
    centro_ref_left_cm = getDistanceCm_off(DIST_LEFT_OFF); time.sleep(0.1)
    centro_ref_right_cm = getDistanceCm_off(DIST_RIGHT_OFF); time.sleep(0.1)

    print("Parametri riferimento centro")
    print("B: ", centro_ref_back_cm,"F: ",centro_ref_front_cm,"L: ",centro_ref_left_cm,"R: ",centro_ref_right_cm)
    print("Angle: ", gyro_sensor.angle())

#Sono più o meno al centro. Raffino la posizione al centro
def ricentra_fine():
    curr_left_cm = getDistanceCm_off(DIST_LEFT_OFF); time.sleep(0.1)
    left_cm = curr_left_cm - centro_ref_left_cm
    #compenso andando a sinistra o a destra
    if left_cm > 1:
        robot_gyro_turn(-90)
    elif left_cm < -1:
        robot_gyro_turn(90)
    if abs(left_cm) > 1:
        robot.drive(left_cm)
        robot_gyro_turn( 0 - gyro_sensor.angle() )

    curr_right_cm = getDistanceCm_off(DIST_RIGHT_OFF); time.sleep(0.1)
    right_cm = curr_right_cm - centro_ref_right_cm
    #compenso andando a sinistra o a destra
    if right_cm > 1:
        robot_gyro_turn(90)
    elif right_cm < -1:
        robot_gyro_turn(-90)
    if abs(right_cm) > 1:
        robot.drive(right_cm)
        robot_gyro_turn( 0 - gyro_sensor.angle() )

    curr_back_cm = getDistanceCm_off(DIST_BACK_OFF); time.sleep(0.1)
    back_cm = curr_back_cm - centro_ref_back_cm
    robot.straight(-back_cm)

    curr_front_cm = getDistanceCm_off(DIST_FRONT_OFF); time.sleep(0.1)
    front_cm = curr_front_cm - centro_ref_back_cm
    robot.straight(front_cm)


#Mi giro di lato e Chiede al server il rilascio del rescue kit
#Alla fine ripristino l'angolazione prima del rilascio
def rilascia_recue_kit():
    angle_save = gyro_sensor.angle()

    robot_gyro_turn(-90)
    srv_rilascia_rescue_kit()
    time.sleep(5)
    robot_gyro_turn(angle_save - gyro_sensor.angle())

#Raggiungo i triangoli, memorizzo il tipo e rilascio il rescue kit
#tria_deg: angolo a cui si trova il triangolo
def vai_a_triangolo_e_torna_indietro(tria_deg):
    global ho_lasciato_kit

    #Ouput
    triangle_color = Color.NONE

    #Ricavo i cm da percorrere a partire dai gradi
    tria_cm = deg2cm_tria[tria_deg]
    robot_gyro_turn(tria_deg)
    
    print("Vado a Triangolo ",tria_deg,": mi sposto di ", -tria_cm, " cm")
    robot.straight(-tria_cm * 10)

    #Mi posiziono di fronte al triangolo per leggere il colore
    angle_save = gyro_sensor.angle()
    robot_gyro_turn(165)

    #Leggo il colore del triangolo
    triangle_color = light_sensor_front.color()
    print("Ho letto ", triangle_color)

    if not ho_lasciato_kit and triangle_color == Color.RED:
        rilascia_recue_kit()
        ho_lasciato_kit = True
    
    #Ripristino la direzione verso il centro
    robot_gyro_turn( angle_save - gyro_sensor.angle() )

    print("Torno al centro: mi sposto di ", tria_cm, " cm")
    robot.straight(tria_cm * 10)

    #Ripristino l'angolo zero al centro stanza
    robot_gyro_turn( 0 - gyro_sensor.angle() )

    #Mi riposiziono al centro
    ricentra_fine()

    return triangle_color

#Scan stanza e detection palline
def scan_e_raggiungipalla():

    print("scan_e_raggiungipalla")

    evac_motor_scan_degs = 30
    evac_motor_scan_degs /= 3

    evac_motor_go_degs = 40

    cm_list = list()
    deg_list = list()

    # Ruota come un radar
    sensorOff(DIST_FRONT_OFF)
    time.sleep(0.5)
    sensorOff(DIST_LEFT_OFF)
    time.sleep(0.5)
    sensorOff(DIST_RIGHT_OFF)
    time.sleep(0.5)

    #FARE alcune letture a vuoto! E' importante per stabilizzare il sensore
    for i in range(10):
        currCm = getDistanceCm(DIST_BACK)
        time.sleep(0.5)

    #Scan
    robot.drive(0, evac_motor_scan_degs)
    gyro_sensor.reset_angle(0)
    cTurnAngle = 0
    while abs(cTurnAngle) < 360+90:
        #time.sleep(0.5)
        currCm = getDistanceCm(DIST_BACK)
        cTurnAngle = gyro_sensor.angle()
        print("distCm Angle: ", currCm, " ", cTurnAngle)
        cm_list.append(currCm)
        deg_list.append(cTurnAngle)
    robot.drive(0,0)
    robot.stop()

    #Punto la pallina
    pallina = evac_get_ball_main(cm_list, deg_list)
    
    angle_dest = pallina.angle if pallina != None else 0
    robot.drive(0, -evac_motor_go_degs)
    while gyro_sensor.angle() > angle_dest: pass
    robot.drive(0,0)
    robot.stop()



def stanza_main():
    #Costruisco il Reference data 
    evac_build_ref_data()

    #Alzo il sensore frontale
    intosta_il_pisello()

    #Guadagnp il centro della stanza
    #@@@ NON FUNZIONA
    #@@@guadagnaCentro()

    triaA_deg = 55
    triaB_deg = 125
    triaC_deg = 235
    triaD_deg = 305

    triaA_color = triaB_color = triaC_color = triaD_color = Color.NONE
    
    c=0
    triaA_color = vai_a_triangolo_e_torna_indietro(triaA_deg)
    if triaA_color != Color.NONE: c+=1
    triaB_color = vai_a_triangolo_e_torna_indietro(triaB_deg)
    if triaB_color != Color.NONE: c+=1
    if c < 2:
        triaC_color = vai_a_triangolo_e_torna_indietro(triaC_deg)
        if triaC_color != Color.NONE: c+=1
    if c < 2:
        triaD_color = vai_a_triangolo_e_torna_indietro(triaD_deg)
        if triaD_color != Color.NONE: c+=1    

    #Parte lo scan e la detection delle palline
    scan_e_raggiungipalla()

stanza_main()

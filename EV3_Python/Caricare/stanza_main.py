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

    gyro_sensor.reset_angle(0)

    #Spengo i sensori per eliminare il rumore
    sensorOff(DIST_BACK_OFF); time.sleep(0.1)
    sensorOff(DIST_FRONT_OFF); time.sleep(0.1)
    sensorOff(DIST_LEFT_OFF); time.sleep(0.1)
    sensorOff(DIST_RIGHT_OFF); time.sleep(0.1)

    centro_ref_back_cm = getDistanceCm_off(DIST_BACK_OFF); time.sleep(0.1)
    centro_ref_front_cm = getDistanceCm_off(DIST_FRONT_OFF); time.sleep(0.1) #ATTENZIONE! NELLA STANZA IL FRONT E' INAFFIDABILE!
    centro_ref_left_cm = getDistanceCm_off(DIST_LEFT_OFF); time.sleep(0.1)
    centro_ref_right_cm = getDistanceCm_off(DIST_RIGHT_OFF); time.sleep(0.1)

    print("Parametri riferimento centro")
    print("B: ", centro_ref_back_cm,"F: ",centro_ref_front_cm,"L: ",centro_ref_left_cm,"R: ",centro_ref_right_cm)
    print("Angle: ", gyro_sensor.angle())

#Sono più o meno al centro. Raffino la posizione al centro
def ricentra_fine():

    #Ripristino l'angolo zero al centro stanza
    print("Ripristino l'angolo zero al centro stanza", )
    currangle = gyro_sensor.angle()
    if abs(currangle) < 180:
        angolo_centro = (0 - currangle) % 360
    else :
        angolo_centro = (360 - currangle) % 360
    robot_gyro_turn( angolo_centro )
    print("Ricentro: compesazione angolo: ",angolo_centro,". Angolo attuale: ", gyro_sensor.angle())
    
    # curr_left_cm = getDistanceCm_off(DIST_LEFT_OFF); time.sleep(0.1)
    # left_cm = curr_left_cm - centro_ref_left_cm
    # print("Ricentro: compesazione Left: ", left_cm)

    # curr_right_cm = getDistanceCm_off(DIST_RIGHT_OFF); time.sleep(0.1)
    # right_cm = curr_right_cm - centro_ref_right_cm
    # print("Ricentro: compesazione Right: ", right_cm)

    # curr_cm = curr_left_cm if abs(curr_left_cm) < abs(curr_right_cm) else -curr_right_cm

    # #compenso andando a sinistra o a destra
    # if curr_cm > 1:
    #     robot_gyro_turn(-90)
    # elif curr_cm < -1:
    #     robot_gyro_turn(90)
    # if abs(curr_cm) > 1:
    #     robot.straight(curr_cm * 10)
    #     robot_gyro_turn( 0 - gyro_sensor.angle() )

    # curr_back_cm = getDistanceCm_off(DIST_BACK_OFF); time.sleep(0.1)
    # back_cm = curr_back_cm - centro_ref_back_cm
    # print("Ricentro: compesazione Back: ", back_cm)
    # robot.straight(-back_cm * 10)

    #NON USARE LA COMPENSAZIONE FRONT: NELLA STANZA IL FRONT E' INAFFIDABILE (TROPPO ALTO)
    # curr_front_cm = getDistanceCm_off(DIST_FRONT_OFF); time.sleep(0.1)
    # front_cm = curr_front_cm - centro_ref_back_cm
    # print("Ricentro: compesazione Front: ", front_cm)
    # robot.straight(front_cm)

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
    tria_cm = 38

    #Ouput
    triangle_color = None

    #delta = -8 #Rispetto alla misura del sensore back, il front avrebbe misurato delta cm in meno

    #Ricavo i cm da percorrere a partire dai gradi
    #tria_cm = deg2cm_tria[tria_deg] - delta
    robot_gyro_turn(tria_deg-180)
    
    print("Vado a Triangolo ",tria_deg,": mi sposto di ", -tria_cm, " cm")
    robot.straight(tria_cm * 10)

    #Leggo il colore del triangolo
    triangle_color = leggi_colore_triangolo()
    print("Ho letto ", triangle_color)

    if not ho_lasciato_kit and triangle_color == Color.GREEN:
        rilascia_recue_kit()
        ho_lasciato_kit = True
    
    print("Torno al centro: mi sposto di ", tria_cm, " cm")
    
    #+2 perchè leggi colore triangolo avanza di 2 centrimetri
    robot.straight(-(tria_cm+2) * 10)

    #Mi riposiziono al centro
    #ricentra_fine()

    return triangle_color

#Scan stanza e detection palline
def scan_e_punta_palla():

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

    return pallina

def leggi_colore_triangolo():
    count_color=dict()
    robot.drive(10, 0)
    start_mm = robot.distance()
    while robot.distance() - start_mm < 20:
        color = light_sensor_front.color()
        if color != None:
            count_color.setdefault(color, list())
            count_color[color].append(1)
    robot.stop()

    count_color.setdefault(Color.RED, list())
    count_color.setdefault(Color.GREEN, list())

    count_red=len(count_color[Color.RED])
    count_green=len(count_color[Color.GREEN])
    if count_red > count_green and count_red > 1:
        return Color.RED
    elif count_green > count_red and count_green > 1:
        return Color.GREEN
    else:
        return None
        

def stanza_main():
    #Costruisco il Reference data 
    evac_build_ref_data()

    #Alzo il sensore frontale
    intosta_il_pisello()

    #Guadagnp il centro della stanza
    #@@@ NON FUNZIONA
    #@@@guadagnaCentro()

    imposta_centro_ref()

    triaA_deg = 125
    triaB_deg = 55
    triaC_deg = 305
    triaD_deg = 235

    triaA_color = triaB_color = triaC_color = triaD_color = None
    
    c=0
    triaA_color = vai_a_triangolo_e_torna_indietro(triaA_deg)
    if triaA_color in [Color.RED, Color.GREEN]: c+=1

    triaB_color = vai_a_triangolo_e_torna_indietro(110)
    if triaB_color in [Color.RED, Color.GREEN]: c+=1

    if c < 2:
        triaC_color = vai_a_triangolo_e_torna_indietro(70)
        if triaC_color in [Color.RED, Color.GREEN]: c+=1

    if c < 2:
        triaD_color = vai_a_triangolo_e_torna_indietro(110)
        if triaD_color in [Color.RED, Color.GREEN]: c+=1

    sys.exit()

    #Parte lo scan e la detection delle palline
    found = True
    while found:
        pallina = scan_e_punta_palla()
        #@@@ Raggiungi la pallina e catturala
        #@@@ vai al triangolo del colore giusto
        #@@@ Scarica la pallina
        #@@@ Torna al centro

        #Riposizionamento fine e reimposta centro
        ricentra_fine()
        imposta_centro_ref()

        found = (pallina != None)

    #@@@ Uscire dalla stanza (algo scan_e_punta_palla modificato)


stanza_main()

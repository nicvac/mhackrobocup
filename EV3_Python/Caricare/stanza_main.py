#!/usr/bin/env pybricks-micropython
from rescue_line_setup import *
from rescue_line_functions import *
from client_functions import *

from stanza_wip.stanza_func import *
from stanza_guadagna_centro import *

from stanza_prendi_palle import *
from stanza_lascia_pallina import *
#Parametri centro
centro_ref_back_cm=0
centro_ref_front_cm=0
centro_ref_left_cm=0
centro_ref_right_cm=0
#Angolo resettato a 0 quando arrivo a centro stanza

ho_lasciato_kit = False

#Spengo i sensori per eliminare il rumore
def imposta_centro_ref():
    global centro_ref_back_cm
    global centro_ref_front_cm
    global centro_ref_left_cm
    global centro_ref_right_cm

    gyro_sensor.reset_angle(0)

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

#Ripristino angolo al centro stanza
#Dall'angolo attuale percorre la distanza minore per raggiungere l'angolo 0
def vai_ad_angolo_zero():
    #Ripristino l'angolo zero al centro stanza
    # x = 90; y= x%360 =  90
    # x =-90; y= x%360 = 270
    currangle = gyro_sensor.angle()
    currangle360 = currangle % 360
    print("vai_ad_angolo_zero: Ripristino l'angolo zero al centro stanza", currangle, "-->", currangle360 )
    #currangle360 in 0..360
    if 0 <= currangle360 <= 180:
        #Compenso in senso antiorario
        angle = -currangle360
    else:
        #Compenso in senso orario
        angle = 360-currangle360

    print("vai_ad_angolo_zero: compenso angolo: ", angle )
    robot_gyro_turn( angle )


#Sono più o meno al centro. Raffino la posizione al centro
def ricentra_fine():

    vai_ad_angolo_zero()
    
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

#IN QUESTA FUNZIONE SI AVANZA FRONTALMENTE!
#Raggiungo i triangoli, memorizzo il tipo e rilascio il rescue kit
#tria_deg: quanto devo ruotare dalla posizione corrente per puntare il triangolo. 
def vai_a_triangolo_e_torna_indietro(tria_deg):
    global ho_lasciato_kit

    #Ouput
    triangle_color = None

    #Distanza dal centro al triangolo (dall'angolazione di tria_deg)    
    tria_cm = 46
    #Distanza per lo scan del colore
    scan_color_cm = 2

    #L'angolo 0 è in corrispondenza di back. Ma il rilascio del rescue kit lo faccio avanzando frontalmente.
    print("Sto ruotando: ", tria_deg)
    robot_gyro_turn(tria_deg)
    print("Ho finito di ruotare")
    

    print("vai_a_triangolo_e_torna_indietro: Vado a Triangolo ",tria_deg,": mi sposto di ", -tria_cm, " cm")
    robot.straight((tria_cm-scan_color_cm) * 10)

    #Leggo il colore del triangolo
    triangle_color = leggi_colore_triangolo(scan_color_cm)
    print("vai_a_triangolo_e_torna_indietro: Scan color: ", triangle_color)

    if not ho_lasciato_kit and triangle_color == Color.GREEN:
        rilascia_recue_kit()
        ho_lasciato_kit = True
    
    print("vai_a_triangolo_e_torna_indietro: Torno al centro: mi sposto di ", tria_cm, " cm")
    
    robot.straight(-tria_cm * 10)

    #Mi riposiziono al centro
    #ricentra_fine()

    return triangle_color

#Scan stanza e detection palline
evac_motor_go_degs = 40
cm_list = list()
deg_list = list()
def scan_e_punta_palla():
    global cm_list
    global deg_list

    print("scan_e_punta_palla")

    evac_motor_scan_degs = 30
    #evac_motor_scan_degs /= 3 #sei campioni a grado
    #evac_motor_scan_degs /= 1 #due sample a grado
    evac_motor_scan_degs /= 2

    cm_list.clear()
    deg_list.clear()

    # Ruota come un radar

    #Spengo i sensori che non mi servono
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

        #SE PREMO UN PULSANTE (TRANNE STOP!!!) RIAVVIA IL SERVER ED ESCE DAL PROGRAMMA
        check_quit_and_restart_server()

        #time.sleep(0.5)
        currCm = getDistanceCm(DIST_BACK)
        cTurnAngle = gyro_sensor.angle()
        print("distCm Angle: ", currCm, " ", cTurnAngle)
        cm_list.append(currCm)
        deg_list.append(cTurnAngle)
    robot.drive(0,0)
    robot.stop()

    #Punto la pallina
    pallina = evac_get_ball(cm_list, deg_list)
    
    angle_dest = pallina.angle if pallina != None else 0
    robot.drive(0, -evac_motor_go_degs)
    while gyro_sensor.angle() > angle_dest: pass
    robot.drive(0,0)
    robot.stop()

    return pallina

#Legge il colore scansionando mentre avanza di dist_cm
def leggi_colore_triangolo(dist_cm):

    color, count = color_scan(light_sensor_front, dist_cm, 1)

    if color != None and color in [Color.RED, Color.GREEN] and count > 1:
        return color
    else:
        return None
        

def stanza_main():
    #Costruisco il Reference data 
    print("Entrato in stanza_main")
    imposta_carrello_rescueline()
    evac_build_ref_data()

    #Alzo il sensore frontale
    print("Alzo sensore")
    intosta_il_pisello()
    print("Sensore alzato")
    
    #Guadagno il centro della stanza
    guadagnaCentro()

    gyro_sensor.reset_angle(0)
    #Angoli rispetto allo 0 (0 è sul back)
    #Rispetto allo 0, faccio prima 125°, poi 55°, ecc...
    triaA_deg = 125
    triaB_deg = 55
    triaC_deg = 305
    triaD_deg = 235

    triaRedDeg = 0
    triaGreenDeg = 0

    triaA_color = triaB_color = triaC_color = triaD_color = None
    
    c=0
    #Ruoterà di -55 = 125-180. -180 perchè voglio puntare il triangolo con front e non con back
    triaA_color = vai_a_triangolo_e_torna_indietro(-55)
    if triaA_color in [Color.GREEN]: c+=1

    #if triaA_color == Color.RED: triaRedDeg = gyro_sensor.angle() 
    if triaA_color == Color.GREEN: triaGreenDeg = gyro_sensor.angle()


    #Secondo triangolo
    #routo di altri -70 = -1 * (125 - 55) (senso antiorario)
    if c < 1:
        triaB_color = vai_a_triangolo_e_torna_indietro( -70 )
        if triaB_color in [Color.GREEN]: c+=1

        #if triaB_color == Color.RED: triaRedDeg = gyro_sensor.angle() 
        if triaB_color == Color.GREEN: triaGreenDeg = gyro_sensor.angle()

    if c < 1:
        #Terzo: ruoto di altri -110 = -1 * ((360-305)+55)
        triaC_color = vai_a_triangolo_e_torna_indietro(-110)
        if triaC_color in [Color.GREEN]: c+=1

        #if triaC_color == Color.RED: triaRedDeg = gyro_sensor.angle() 
        if triaC_color == Color.GREEN: triaGreenDeg = gyro_sensor.angle()
            

    if c < 1:
        #Quarto: ruoto di altri -70 = -1 * (360 - 235) - (360-305)
        triaD_color = vai_a_triangolo_e_torna_indietro(-70)
        if triaD_color in [Color.GREEN]: c+=1
        #if triaD_color == Color.RED: triaRedDeg = gyro_sensor.angle() 
        if triaD_color == Color.GREEN: triaGreenDeg = gyro_sensor.angle()  

    #Ripristino l'angolo per allinearmi allo 0_back
    vai_ad_angolo_zero()

    #Parte lo scan e la detection delle palline
    found = True
    while found:
        pallina = scan_e_punta_palla()

        #Raggiungi la pallina e catturala
        prendi_palla(pallina.distance)
        ricentra_fine()

        # vai al triangolo del colore giusto
        tria_cm = 41
        print("Rilascio in triangolo. Ruoto: ", triaGreenDeg)
        robot_gyro_turn(triaGreenDeg)

        print("Rilascio in triangolo. Vado a Triangolo ",triaGreenDeg,": mi sposto di ", tria_cm, " cm")
        robot.straight((tria_cm) * 10)
        
        # Scarica la pallina
        lascia_pallina()

        # Torna al centro
        robot.straight(-(tria_cm)*10)
        #Riposizionamento fine e reimposta centro
        ricentra_fine()
        imposta_centro_ref()

        found = (pallina != None)

    # Uscire dalla stanza (algo scan_e_punta_palla modificato)
    evac_exit = evac_get_exits(cm_list, deg_list)
    #Punto l'uscita
    angle_dest = evac_exit.angle if evac_exit != None else 0
    robot.drive(0, -evac_motor_go_degs)
    while gyro_sensor.angle() > angle_dest: pass
    robot.drive(0,0)
    robot.stop()

    #Avanzare fino all'uscita
    robot.straight((evac_exit.distance + 2) * 10)
    imposta_carrello_rescueline()


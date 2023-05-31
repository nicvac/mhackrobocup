#!/usr/bin/env pybricks-micropython
from rescue_line_setup import *
from math import *
from rescue_line_functions import *
from client_functions import *

#@@@ TEMP
from stanza_wip import stanza_func01

#Dimensione della pallina
sizePallinaCm = 4.5

#La distanza finale fra robot e oggetto da raggiungere
distFinaleCm = 2.0

#La distanza fra il robot e la pallina da catturare
distPallina = 7.0

#Dimensioni della stanza
dimRoom1 = 90
dimRoom2 = 120
dimRoomDiag = sqrt( dimRoom1 * dimRoom1 + dimRoom2 * dimRoom2)

#Dimensioni Evacuation points
dimEcavPoint = 30
dimEvacPointAltezza = sqrt( dimEcavPoint * dimEcavPoint + dimEcavPoint * dimEcavPoint ) / 2

#Tipo di Evacuation zone da raggiungere
EV_VERDE = 0
EV_ROSSA = 1
EV_USCITA = 2

#VERSO
SGORARIO=0
SGANTIORARIO=1

# Nella stanza uso il robot al contrario rispetto al seguilinea
# robot = DriveBase(right_motor, left_motor, wheel_diameter=wheel, axle_track=axle)

    
# Determina il verso di rotazione da usare per riagganciare l'oggetto.
# Il verso di rotazione va determinato solo una volta e si userà sempre lo stesso per riagganciare l'oggetto
def evacDetectScanDirection( scanMinCm ):
    print("evacDetectScanDirection")

    gyro_sensor.reset_angle(0)

    # Ruota come un radar, in senso antiorario per 10 gradi
    angleLimit = 10.0
    robot.drive(0, -evac_motor_scan_degs)
    cTurnAngle = gyro_sensor.angle()
    trovato = False
    while not trovato and abs(cTurnAngle) <= angleLimit:
        cTurnAngle = gyro_sensor.angle()
        tempDist = getDistanceCm(DIST_BACK)
        if tempDist <= scanMinCm + 0.5:
            trovato = True

    robot.drive(0, 0)
    robot.stop()

    # Rimettiti in posizione, prima di questa scansione
    # Ruota In senso orario di N gradi per compensare la rotazione antioraria usata durante la scansione per riagganciare l'oggetto
    robot_gyro_turn(abs(cTurnAngle))

    dirScan = SGANTIORARIO if trovato else SGORARIO

    print("evacDetectScanDirection Fine")

    return dirScan


# Gira in senso antioratio, come un radar, per individuare uno spike nella distanza
# Continua a ruotare finche le misurazioni successive sono "smooth", cioè finchè osservi un muro
# Fermati quando hai individuato uno spike: potenzialmente un oggetto da prendere.
# Note:
# - se si parte osservando già l'oggetto, la scansione prenderà il prossimo oggetto o lo stesso dopo una rotazione di 360 gradi.
# - LA SCANSIONE DEVE ESSERE FATTA PARTENDO DAL CENTRO STANZA, PER TROVARE SOLO PALLINE E NON GLI SPIGOLI DELLE ENTRATE / USCITE!
# - SE ENTRATA E USCITA NON SONO NEGLI ANGOLI, POTREBBE PRENDERE COME SPIKE L'ANGOLO DEL MURO DI UNA ENTRATA O UNA USCITA
def evacIndividuaSpike():
    print("evacIndividuaSpike")

    gyro_sensor.reset_angle(0)

    # Ruota come un radar, in senso antiorario
    robot.drive(0, -evac_motor_scan_degs)

    # Individua lo spike. Fa due giri su se stesso. Se non trova nulla restituisce false.
    gyro_sensor.reset_angle(0)
    cTurnAngle = 0

    isScanInteresting = False
    currCm = 0

    while not isScanInteresting and abs(cTurnAngle) <= 360 * 2:
        prevCm = currCm
        currCm = getDistanceCm(DIST_BACK)
        diffCm = abs(prevCm - currCm)

        cTurnAngle = gyro_sensor.angle()
        print("distCm Angle: ", currCm, " ", cTurnAngle)

        daLontanoAVicino = prevCm > currCm + 1.0
        isSpike = diffCm >= sizePallinaCm
        nellaStanza = currCm < (dimRoomDiag/2.0 - dimEvacPointAltezza)
        isScanInteresting = isSpike and daLontanoAVicino and nellaStanza
    
    robot.drive(0,0)
    robot.stop()

    # Ritorna l'ultima distanza
    distCm = currCm
    
    print("evacIndividuaSpike Fine")

    return isScanInteresting, distCm

    

# Sto puntando l'oggetto. Lo raggiungo.
def evacRaggiungiOggetto( oggDistCm ):
    print("evacRaggiungiOggetto")

    # Il verso di rotazione deve essere determinato solo una volta in questa funzione.
    dirScan = SGANTIORARIO
    dirScanDetected = False

    scanDistCurrCm = oggDistCm
    scanMinCm = oggDistCm

    isAgganciato = True

    while scanDistCurrCm >= distFinaleCm:
        # Avanza finchè la distanza si riduce
        robot.drive(motor_max_degs, 0)
        while isAgganciato and (scanDistCurrCm > distFinaleCm):
            scanDistCurrCm = getDistanceCm(DIST_BACK)

            if scanDistCurrCm <= scanMinCm + 0.5:
                scanMinCm = min(scanMinCm, scanDistCurrCm)
            else:
                isAgganciato = False
        
        robot.drive(0, 0)
        robot.stop()

        # Qui sono sganciato oppure ho raggiunto l'oggetto
        # Se ho rggiunto l'oggetto esco dal ciclo principale
        if scanDistCurrCm <= distFinaleCm:
            break

        # Qui sono sganciato dall'oggetto. Lo riaggancio, scansionando un'area di pochi gradi a destra e a sinistra.

        # Devo determinare il verso di rotazione da usare per riagganciare l'oggetto.
        # Il verso di rotazione va determinato solo una volta e si userà sempre lo stesso per riagganciare l'oggetto corrente
        if not dirScanDetected:
            dirScan = evacDetectScanDirection(scanMinCm)
            dirScanDetected = True

        # Gira nella direzione individuata, finchè non riaggancio l'oggetto
        robot.drive(0, evac_motor_scan_degs * (1 if dirScan == SGORARIO else -1 ))
        while not isAgganciato:
            scanDistCurrCm = getDistanceCm(DIST_BACK)
            isAgganciato = scanDistCurrCm <= scanDistCurrCm + 0.5
        
        robot.drive(0, 0)
        robot.stop()

        # Una volta riagganciato, giro di ulteriori 5 gradi per centrare meglio l'oggetto
        angolo = 5 * (1 if dirScan == SGORARIO else -1 )
        robot.turn(angolo)
    
    print("evacRaggiungiOggetto Fine")
    return dirScan, dirScanDetected



# Raggiunto l'oggetto, ruoto il robot per centrare al meglio l'oggetto.
# Ruoto finchè non raggiungo la distanza minima.
def evacCentratiRispettoAlloggetto( dirScan ):

    print("evacCentratiRispettoAlloggetto")

    curCm = getDistanceCm(DIST_BACK)
    scanMinCm = curCm

    robot.drive(0, evac_motor_scan_degs * (1 if dirScan == SGORARIO else -1 ) )

    minimoMigliorato = True

    while minimoMigliorato:
        currCm = getDistanceCm(DIST_BACK)
        minimoMigliorato = (currCm <= scanMinCm)
    
    robot.stop()

    print("evacCentratiRispettoAlloggetto Fine")


#L'oggetto raggiunto è una pallina
#Restituisce vero se abbiamo raggiunto una pallina
#Restituisce evacuationType: il colore della evacuation zone in cui portare la pallina
def evacIsPallina():
    print("evacIsPallina")
    evacuationType = EV_VERDE
    isPallina = True
    #@@@  DA SCRIVERE
    # RESTITUISCI FALSE SE LEGGI UNA LINEA DI ENTRATA O USCITA
    print("evacIsPallina Fine")
    return isPallina, evacuationType

#Cattura la pallina
def evacCatturaPallina():
    # @@@
    # upper_left_motor.run_angle(300, -100)
    # upper_right_motor.run_angle(300, -100)

    # upper_right_motor.hold()
    # upper_left_motor.hold()
        
    # upper_left_motor.run_angle(300, 100)
    # upper_right_motor.run_angle(300, 100)
    brick_speaker_beep(1)



# MAIN
#Questa funzione va chiamata dal centro stanza!
#Trova una palla nella stanza e la raggiunge
#Restituisce evacuationType: il colore della evacuation zone in cui portare la pallina oppure uscita (non ci sono palline)
def evacTrovaERaggiungiPalla():
    print("evacTrovaERaggiungiPalla")

    isPallina = False
    
    while not isPallina:
        # Radar, ruota fino a individuare un oggetto da raggiungere
        print("evacIndividuaSpike begin")
        oggDistCm = 0 # la distanza dall'oggetto che mi ha determinato lo spike (che ho agganciato)
        trovato, oggDistCm = evacIndividuaSpike()

        print("evacIndividuaSpike end. oggDistCm: ", oggDistCm, "; trovato: ", trovato)

        if not trovato:
            return EV_USCITA
                
        # Tieni agganciato l'oggetto ed avvicinati
        print("evacRaggiungiOggetto begin")
        dirScanDetected = False
        
        dirScan, dirScanDetected = evacRaggiungiOggetto(oggDistCm)
        print("evacRaggiungiOggetto end. oggDistCm: ",oggDistCm,"; dirScan: ",dirScan,"; dirScanDetected: ", dirScanDetected); 


        #Raggiunto l'oggetto ad una distanza di distFinaleCm
        #Ruoto il robot per centrare meglio l'oggetto
        if dirScanDetected:
            print("evacCentratiRispettoAlloggetto begin. dirScan: ", dirScan)
            evacCentratiRispettoAlloggetto( dirScan )
            print("evacCentratiRispettoAlloggetto end.")

        #Controlliamo se l'oggetto raggiunto è una pallina
        isPallina, evacuationType = evacIsPallina()


    #Qui sono vicino alla pallina. Devo essere distante di 7 cm per catturare la pallina
    robot.straight( -(distPallina - distFinaleCm) )

    #Cattura la pallina 
    evacCatturaPallina()

    print("evacTrovaERaggiungiPalla END")
    return evacuationType


# MAIN

evac_motor_scan_degs = 30
evac_motor_scan_degs /= 3

evac_motor_go_degs = 40

#upper_left_motor.run_angle(300, 100)
#upper_right_motor.run_angle(300, 90) #Devono girare insieme.
upper_left_motor.hold()
upper_right_motor.hold()

#@@@ evacTrovaERaggiungiPalla()

#@@@ DEBUG: Togliere questo codice dopo aver testato
########
########
########

cm_list = list()
deg_list = list()

print("IndividuaSpike")

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

#Controlla se devo uscire (premendo qualunque tasto)
while True:
    check_quit_and_restart_server()


#Punto la pallina
# pallina = stanza_func.evac_get_sample(cm_list, deg_list)
# angle_dest = pallina.angle if pallina != None else 0
# robot.drive(0, -evac_motor_go_degs)
# while gyro_sensor.angle() > angle_dest: pass
# robot.drive(0,0)
# robot.stop()

#@@@ 





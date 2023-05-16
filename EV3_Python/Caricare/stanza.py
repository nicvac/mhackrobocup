#!/usr/bin/env pybricks-micropython
from rescue_line_setup import *
from math import *
from rescue_line_functions import *

upper_left_motor.run_angle(300, 90)
upper_right_motor.run_angle(300, 90)
upper_left_motor.hold()
upper_right_motor.hold()

SERVER = 'ev3devExt'

client = BluetoothMailboxClient()
mbox = TextMailbox('greeting', client)
extReq = NumericMailbox('extReq', client)
extDist = NumericMailbox('extDist', client)

print('establishing connection...')
client.connect(SERVER)
print('connected!')


sizePallinaCm = 4.5

distFinaleCm = 7.0

dimRoom1 = 90
dimRoom2 = 120
dimRoomDiag = sqrt( dimRoom1 * dimRoom1 + dimRoom2 * dimRoom2)

dimEcavPoint = 30
dimEvacPointAltezza = sqrt( dimEcavPoint * dimEcavPoint + dimEcavPoint * dimEcavPoint ) / 2

EV_VERDE = 0
EV_ROSSA = 1
EV_USCITA = 2

SGORARIO=0
SGANTIORARIO=1


def ruotaSuAsse(senso):
    if senso == -1:
        left_motor.dc(-60)
        right_motor.dc(60)
    else:
        left_motor.dc(60)
        right_motor.dc(-60)
    

#ferma tutti i motori
def motoriFerma ():
    left_motor.hold()
    right_motor.hold()


#Trasforma la distanza in mm del sensore in cm
def getDistanceCm():
    extReq.send(4)
    extDist.wait()
    distanzaMm = extDist.read()
    distanzaCm = distanzaMm / 10
    print(distanzaCm)
    return distanzaCm
    
# Determina il verso di rotazione da usare per riagganciare l'oggetto.
# Il verso di rotazione va determinato solo una volta e si userà sempre lo stesso per riagganciare l'oggetto
def evacDetectScanDirection( scanMinCm ):
    print("evacDetectScanDirection")

    gyro_sensor.reset_angle(0)


    # Ruota come un radar, in senso antiorario per 10 gradi
    angleLimit = 10.0
    robot.drive(0, -300)
    cTurnAngle = gyro_sensor.angle()
    trovato = False
    while not trovato and abs(cTurnAngle) <= angleLimit:
        cTurnAngle = gyro_sensor.angle()
        tempDist = getDistanceCm()
        if tempDist <= scanMinCm + 0.5:
            trovato = True

    robot.stop()

    # Rimettiti in posizione, prima di questa scansione
    # Ruota In senso orario di N gradi per compensare la rotazione antioraria usata durante la scansione per riagganciare l'oggetto
    robot.drive(0, 300)
    gyro_sensor.reset_angle(0)
    while gyro_sensor.angle() < abs(cTurnAngle):
        pass
    robot.stop()

    dirScan = SGANTIORARIO if trovato else SGORARIO

    print("Fine")

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
    ruotaSuAsse(-1)

    # Individua lo spike. Fa due giri su se stesso. Se non trova nulla restituisce false.
    cTurnAngle = 0

    isScanInteresting = False
    currCm = 0

    while not isScanInteresting and abs(cTurnAngle) <= 360 * 2:
        prevCm = currCm
        currCm = getDistanceCm()
        diffCm = abs(prevCm - currCm)

        cTurnAngle = gyro_sensor.angle()

        daLontanoAVicino = prevCm > currCm + 1.0
        isSpike = diffCm >= sizePallinaCm
        nellaStanza = currCm < (dimRoomDiag/2.0 - dimEvacPointAltezza)
        isScanInteresting = isSpike and daLontanoAVicino and nellaStanza
    
    motoriFerma()

    # Ritorna l'ultima distanza
    distCm = currCm
    
    print("Fine")

    return isScanInteresting, distCm

    

# Sto puntando l'oggetto. Lo raggiungo.
def evacRaggiungiOggetto( oggDistCm ):
    print("evacRaggiungiOggetto")

    # Il verso di rotazione deve essere determinato solo una volta in questa funzione.
    dirScanDetected = False
    dirScan = SGANTIORARIO

    scanDistCurrCm = oggDistCm
    scanMinCm = oggDistCm

    isAgganciato = True

    print("evacRaggiungiOggetto", " ",scanDistCurrCm, " ", distFinaleCm)

    while scanDistCurrCm > distFinaleCm:
        print("evacRaggiungiOggetto: entrato nel while", scanDistCurrCm, " ", distFinaleCm)
        # Avanza finchè la distanza si riduce
        robot.drive(300, 0)
        while isAgganciato and (scanDistCurrCm > distFinaleCm):
            scanDistCurrCm = getDistanceCm()

            if scanDistCurrCm <= scanMinCm + 0.5:
                scanMinCm = min(scanMinCm, scanDistCurrCm)
            else:
                isAgganciato = False
        
        robot.stop()
        #motoriFerma()

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
        robot.drive(0, 300)
        while not isAgganciato:
            scanDistCurrCm = getDistanceCm()
            isAgganciato = scanDistCurrCm <= scanDistCurrCm + 0.5
        
        motoriFerma()

        # Una volta riagganciato, giro di ulteriori 5 gradi per centrare meglio l'oggetto
        # angolo = -5 if dirScan == SGANTIORARIO else 5
        # robot.turn(angolo, True)
    
    print("Fine")
    quit()
    return dirScanDetected, dirScan



# Raggiunto l'oggetto, ruoto il robot per centrare al meglio l'oggetto.
# Ruoto finchè non raggiungo la distanza minima.
def evacCentratiRispettoAlloggetto( dirScan ):
    print("evacCentratiRispettoAlloggetto")

    curCm = getDistanceCm()
    scanMinCm = curCm

    ruotaSuAsse(1 if dirScan == SGORARIO else SGANTIORARIO)

    minimoMigliorato = True

    while minimoMigliorato:
        currCm = getDistanceCm()
        minimoMigliorato = currCm <= scanMinCm
    
    motoriFerma()

    print("Fine")


def evacCatturaPallina():
    # upper_left_motor.run_angle(300, -100)
    # upper_right_motor.run_angle(300, -100)

    # upper_right_motor.hold()
    # upper_left_motor.hold()
        
    # upper_left_motor.run_angle(300, 100)
    # upper_right_motor.run_angle(300, 100)
    brick_speaker_beep(1)



# MAIN
# Trova una palla nella stanza e la raggiunge
# Restituisce evacuationType: il colore della evacuation zone in cui portare la pallina oppure uscita (non ci sono palline)
#def evacTrovaERaggiungiPalla():
while True:
    isPallina = False
    
    while not isPallina:
        # Radar, ruota fino a individuare un oggetto da raggiungere
        print("evacIndividuaSpike begin")
        oggDistCm = 0 # la distanza dall'oggetto che mi ha determinato lo spike (che ho agganciato)
        trovato, oggDistCm = evacIndividuaSpike()

        print("evacIndividuaSpike end. oggDistCm: ", oggDistCm, "; trovato: ", trovato)

        if not trovato:
            evacuationType = EV_USCITA
            # return
                
        # Tieni agganciato l'oggetto ed avvicinati
        print("evacRaggiungiOggetto begin")
        dirScanDetected = False
        
        dirScan, dirScanDetected = evacRaggiungiOggetto(oggDistCm)


        #Raggiunto l'oggetto ad una distanza di distFinaleCm
        #Ruoto il robot per centrare meglio l'oggetto
        if dirScanDetected:
            print("evacCentratiRispettoAlloggetto begin. dirScan: ", dirScan)
            evacCentratiRispettoAlloggetto( dirScan )
            print("evacCentratiRispettoAlloggetto end.")

        #Controlliamo se l'oggetto raggiunto è una pallina
        #isPallina = evacIsPallina( evacuationType )
        isPallina = True

    #Ruoto su me stesso in modo da posizionare la gabbia per catturare la pallina

   #Cattura la pallina 
    evacCatturaPallina()

    print("fine")
    # return evacuationType


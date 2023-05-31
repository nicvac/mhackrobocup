# Messaging
# https://pybricks.com/ev3-micropython/messaging.html
# ATTENZIONE: USANDO IL MECCANISMO DI WAIT REQUEST DAL CLIENT, SI RISCHIA DI PERDERSI LA SINCRONIA 
#  FRA SERVERE E CLIENT, SERVER PERDE LA RICHIESTA DEL CLIENT E RIMANE INDEFINITIVAMENTE IN WAIT.
#  QUINDI LA WAIT LA FA SOLO IL SERVER E IL CLIENT LEGGE A RIPETIZIONE SENZA WAIT

from pybricks.hubs import EV3Brick
from pybricks.messaging import BluetoothMailboxClient, TextMailbox, NumericMailbox

from server.server_commands import *

import time
import sys

clientEv3 = EV3Brick() 

#Ritorna la distanza del sensore server in mm.
#Gestisce la sincronizzazione dei messaggi con il server.
#Come da guida, avrei dovuto usare una wait, ma ci sono casi di deadlock.
#Abbiamo gestito la wait con un while e se passa un tot tempo rimandiamo la richiesta perchè il
#server potrebbe averla persa.
def getDistanceMM(sensore):
    c=1
    start = time.time()
    extDist.send(sensore)
    dist_mm = None
    while dist_mm == None:
        stop = time.time()
        if (stop - start) > 0.15:
            c += 1
            extDist.send(sensore)
        dist_mm = extDist.read()
    #count += 1
    #print(count)
    if c > 1:
        print("############### getDistanceMM: Richiesta mandata ", c, "volte")
    return dist_mm


#Spegne i sensori che non servono, per ridurre l'interferenza con il sensore che effettua la lettura
# NON CHIAMARLO A LOOP STRETTO!!! PUO' IMPALLARE I SENSORI!!!
def sensorOff(sensore_off):
    c=1
    start = time.time()
    extDist.send(sensore_off)
    dist_mm = None
    while dist_mm == None:
        stop = time.time()
        if (stop - start) > 0.15:
            c += 1
            extDist.send(sensore_off)
        dist_mm = extDist.read()
    if c > 1:
        print("############### offSensor: Richiesta mandata ", c, "volte")
    print("Sensor off ", sensore_off)
    return dist_mm

#Ritorna la distanza in cm
def getDistanceCm(sensore):
    dist_cm = getDistanceMM(sensore) / 10
    return dist_cm

#Ritorna la distanza in cm e spegne il sensore
def getDistanceCm_off(sensore):
    dist_cm = sensorOff(sensore) / 10
    return dist_cm


#Intosta il pisello
def intosta_il_pisello():
    c=1
    start = time.time()
    extDist.send(ALZA_SENSORE_FRONTALE)
    risp = None
    while risp == None:
        stop = time.time()
        if (stop - start) > 10.0:
            c += 1
            extDist.send(ALZA_SENSORE_FRONTALE)
        risp = extDist.read()
    if c > 1:
        print("############### intosta_il_pisello: Richiesta mandata ", c, "volte")
    return risp

#Rilascia il rescue kit
def srv_rilascia_rescue_kit():
    c=1
    start = time.time()
    extDist.send(RILASCIA_RESCUE_KIT)
    risp = None
    while risp == None:
        stop = time.time()
        if (stop - start) > 20.0:
            c += 1
            extDist.send(RILASCIA_RESCUE_KIT)
        risp = extDist.read()
    if c > 1:
        print("############### rilascia_rescue_kit: Richiesta mandata ", c, "volte")
    return risp


#SE PREMO QUALUNQUE PULSANTE (TRANNE PULSANTE STOP!!!)
#RIAVVIA IL SERVER ED ESCE!
server_restart_request = False
def check_quit_and_restart_server():
    global server_restart_request
    if server_restart_request == False and clientEv3.buttons.pressed():
        print("RIAVVIO IL SERVER ED ESCO")
        server_restart_request = True
        extDist.send(CONNECTION_RESTART)
        sys.exit()

#RIAVVIA IL SERVER ED ESCE!
def quit_and_restart_server():
    global server_restart_request
    if server_restart_request == False:
        print("RIAVVIO IL SERVER ED ESCO")
        server_restart_request = True
        extDist.send(CONNECTION_RESTART)
        sys.exit()



print("OPERAZIONE DI CONNESSIONE AL SERVER AVVIATA, COMMENTARE SE NON SERVE")

client = BluetoothMailboxClient()

print('establishing connection...')
client.connect(SERVER)
print('connected!')

#USARE LE STESSE ETICHETTE DEL SERVER
extDist = NumericMailbox('extDist', client)


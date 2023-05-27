# Messaging
# https://pybricks.com/ev3-micropython/messaging.html
# ATTENZIONE: USANDO IL MECCANISMO DI WAIT REQUEST DAL CLIENT, SI RISCHIA DI PERDERSI LA SINCRONIA 
#  FRA SERVERE E CLIENT, SERVER PERDE LA RICHIESTA DEL CLIENT E RIMANE INDEFINITIVAMENTE IN WAIT.
#  QUINDI LA WAIT LA FA SOLO IL SERVER E IL CLIENT LEGGE A RIPETIZIONE SENZA WAIT

from pybricks.messaging import BluetoothMailboxClient, TextMailbox, NumericMailbox

import time

#Il brick server (fornisce le distanze)
SERVER = 'ev3devExt'

#Tipo di sensore di distanza
DIST_FRONT = 1
DIST_BACK = 4
DIST_LEFT = 2
DIST_RIGHT = 3


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
        print("############### Richiesta mandata ", c, "volte")
    return dist_mm


#Ritorna la distanza in cm
def getDistanceCm(sensore):
    dist_cm = getDistanceMM(sensore) / 10
    return dist_cm

print("OPERAZIONE DI CONNESSIONE AL SERVER AVVIATA, COMMENTARE SE NON SERVE")

client = BluetoothMailboxClient()

print('establishing connection...')
client.connect(SERVER)
print('connected!')

#USARE LE STESSE ETICHETTE DEL SERVER
extDist = NumericMailbox('extDist', client)


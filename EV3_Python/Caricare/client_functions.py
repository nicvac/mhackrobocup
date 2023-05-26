# Messaging
# https://pybricks.com/ev3-micropython/messaging.html
# ATTENZIONE: USANDO IL MECCANISMO DI WAIT REQUEST DAL CLIENT, SI RISCHIA DI PERDERSI LA SINCRONIA 
#  FRA SERVERE E CLIENT, SERVER PERDE LA RICHIESTA DEL CLIENT E RIMANE INDEFINITIVAMENTE IN WAIT.
#  QUINDI LA WAIT LA FA SOLO IL SERVER E IL CLIENT LEGGE A RIPETIZIONE SENZA WAIT

from pybricks.messaging import BluetoothMailboxClient, TextMailbox, NumericMailbox

#Il brick server (fornisce le distanze)
SERVER = 'ev3devExt'

#Tipo di sensore di distanza
DIST_FRONT = 1
DIST_BACK = 4
DIST_LEFT = 2
DIST_RIGHT = 3

#count = 0

#Ritorna la distanza del sensore server in cm
def getDistanceMM(sensore):
    #global count
    dist_mm = None
    while dist_mm == None:
        extDist.send(sensore)
        dist_mm = extDist.read()
    #count += 1
    #print(count)
    return dist_mm


#Ritorna la distanza in cm, con contatore di stabilità
def getDistanceCm(sensore):
    dist_cm = getDistanceMM(sensore) / 10
    #print(dist_cm)
    return dist_cm

print("OPERAZIONE DI CONNESSIONE AL SERVER AVVIATA, COMMENTARE SE NON SERVE")

client = BluetoothMailboxClient()

print('establishing connection...')
client.connect(SERVER)
print('connected!')

#USARE LE STESSE ETICHETTE DEL SERVER
extDist = NumericMailbox('extDist', client)


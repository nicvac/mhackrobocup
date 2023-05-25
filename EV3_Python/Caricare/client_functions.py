# Messaging
# https://pybricks.com/ev3-micropython/messaging.html
# ATTENZIONE: USANDO IL MECCANISMO DI WAIT REQUEST DAL CLIENT, SI RISCHIA DI PERDERSI LA SINCRONIA 
#  FRA SERVERE E CLIENT, SERVER PERDE LA RICHIESTA DEL CLIENT E RIMANE INDEFINITIVAMENTE IN WAIT.
#  QUINDI RACCOLGO I DATI DAL SENSORE E LI SPARO A RIPETIZIONE. SARA' SOLO IL CLIENT A FARE WAIT 
#  QUANDO GLI SERVE

from pybricks.messaging import BluetoothMailboxClient, TextMailbox, NumericMailbox

#Il brick server (fornisce le distanze)
SERVER = 'ev3devExt'

#Tipo di sensore di distanza
DIST_FRONT = 1
DIST_BACK = 4
DIST_LEFT = 2
DIST_RIGHT = 3

#Ritorna la distanza del sensore server in cm
def getDistanceMM(sensore):
    #Attenzione! Serve leggerli tutti per svuotare la coda del server!
    extDistFront.wait()
    dist_f_cm = extDistFront.read()
    extDistBack.wait()
    dist_b_cm = extDistBack.read()
    extDistLeft.wait()
    dist_l_cm = extDistLeft.read()
    extDistRight.wait()
    dist_r_cm = extDistRight.read()

    if sensore == DIST_FRONT:
        dist_cm = dist_f_cm
    elif sensore == DIST_BACK:
        dist_cm = dist_b_cm
    elif sensore == DIST_LEFT:
        dist_cm = dist_l_cm
    elif sensore == DIST_RIGHT:
        dist_cm = dist_r_cm
    return dist_cm

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
extDistFront = NumericMailbox('extDistFront', client)
extDistBack  = NumericMailbox('extDistBack', client)
extDistLeft  = NumericMailbox('extDistLeft', client)
extDistRight  = NumericMailbox('extDistRight', client)

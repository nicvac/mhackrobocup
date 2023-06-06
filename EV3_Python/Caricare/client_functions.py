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

#Funzione generica di richiesta
#Gestisce la sincronizzazione dei messaggi con il server.
#Come da guida, avrei dovuto usare una wait, ma ci sono casi di deadlock.
#Abbiamo gestito la wait con un while e se passa un tot tempo rimandiamo la richiesta perchè il
#server potrebbe averla persa.
def request( req_code, timeout ):
    global extDist
    #Output
    response = None
    while response == None:
        try:
            #@@@ TBC: serve ricreare l'oggetto?
            extDist = NumericMailbox('extDist', client)

            c=1
            start = time.time()
            extDist.send(req_code)
            response = None
            while response == None:
                stop = time.time()
                if (stop - start) > timeout:
                    c += 1
                    extDist.send(req_code)
                response = extDist.read()
            if c > 1:
                print("############### request: Richiesta", req_code, " mandata ", c, "volte")

        except Exception as e:
            # Catch the exception and print the error message
            print("############### request: Richiesta", req_code,". An exception occurred:", str(e))
            time.sleep(0.05)
            clientEv3.speaker.beep()
            response = None

    return response


#Ritorna la distanza del sensore server in mm.
def getDistanceMM(req_code):
    return request(req_code, 0.15)


#Spegne i sensori che non servono, per ridurre l'interferenza con il sensore che effettua la lettura
# NON CHIAMARLO A LOOP STRETTO!!! PUO' IMPALLARE I SENSORI!!!
def sensorOff(req_code):
    return request(req_code, 0.15)

#Ritorna la distanza in cm
def getDistanceCm(req_code):
    dist_cm = getDistanceMM(req_code) / 10
    return dist_cm

#Ritorna la distanza in cm e spegne il sensore
def getDistanceCm_off(req_code):
    dist_cm = sensorOff(req_code) / 10
    return dist_cm


#Intosta il pisello
def intosta_il_pisello():
    return request(ALZA_SENSORE_FRONTALE, 10.0)

#Rilascia il rescue kit
def srv_rilascia_rescue_kit():
    return request(RILASCIA_RESCUE_KIT, 20.0)


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


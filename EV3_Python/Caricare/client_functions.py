from pybricks.messaging import BluetoothMailboxClient, TextMailbox, NumericMailbox

#Il brick server (fornisce le distanze)
SERVER = 'ev3devExt'

#Messaggio per le distanze
mailbox_extDist = 'extDist'

#Porte dei sensori sul server
DIST_FRONT = 1
DIST_BACK = 4
DIST_LEFT = 2
DIST_RIGHT = 3

#Ritorna la distanza del sensore server in cm
def getDistanceMM(sensore):
        extDist = NumericMailbox( mailbox_extDist, client)
        extDist.send(sensore)
        extDist.wait()
        dist_cm = extDist.read()
        return dist_cm

#Ritorna la distanza in cm, con contatore di stabilità
def getDistanceCm(sensore):
    curr = getDistanceMM(sensore) / 10
    #print(curr)
    return curr

print("OPERAZIONE DI CONNESSIONE AL SERVER AVVIATA, COMMENTARE SE NON SERVE")


client = BluetoothMailboxClient()
#mbox = TextMailbox('greeting', client)

print('establishing connection...')
client.connect(SERVER)
print('connected!')

#!/usr/bin/env pybricks-micropython
from rescue_line_setup import *
from rescue_line_functions import *


robot = 14
halfRobot = robot/2

front = 1
left = 2
right = 3
back = 4

sensorReadingFront = getDistanceCmPort(1)
sensorReadingLeft = getDistanceCmPort(2)
sensorReadingRight = getDistanceCmPort(3)

side = 0
longOrShort = 0


def dritto():
    robot.drive(100, 0)

def ruotaSuAsse( verso ):
    robot.drive(0, (30 * verso))

def stop():
    robot.stop()


### FUNZIONI PER GUADAGNARE IL CENTRO

def leftShort():
    print("Ho rilevato l'entrata a sinistra sul lato corto della stanza\n")

    gyro_sensor.reset_angle(0)
    ruotaSuAsse(1)
    while abs(gyro_sensor.angle()) < 90:
        pass
    stop()

    print("Ho ruotato a destra perchè ho visto il muro a sinistra, raggiungo il centro del lato corto\n")

    distance = getDistanceCmPort(4)
    dritto()  
    while distance < (40 - halfRobot):
        distance = getDistanceCmPort(4)
    stop()

    print("Sono al centro del lato corto della stanza\n\nRuoto sull'asse in senso antiorario")

    gyro_sensor.reset_angle(0)
    ruotaSuAsse(-1)
    while abs(gyro_sensor.angle()) < 90:
        pass
    stop()

    print("Sono pronto a raggiungere il centro della stanza sul lato lungo")

    distance = getDistanceCmPort(4)
    dritto()
    while distance < 60 - halfRobot:
        distance = getDistanceCmPort(4)
    stop()

    print("HO RAGGIUNTO IL CENTRO")


def rightShort():
    print("Ho rilevato l'entrata a destra sul lato corto della stanza\n")

    gyro_sensor.reset_angle(0)
    ruotaSuAsse(-1)
    while abs(gyro_sensor.angle()) < 90:
        pass
    stop()

    print("Ho ruotato a sinistra perchè ho visto il muro a destra, raggiungo il centro del lato corto\n")

    distance = getDistanceCmPort(4)
    dritto()  
    while distance < (40 - halfRobot):
        distance = getDistanceCmPort(4)
    stop()

    print("Sono al centro del lato corto della stanza\n\nRuoto sull'asse in senso orario")

    gyro_sensor.reset_angle(0)
    ruotaSuAsse(1)
    while abs(gyro_sensor.angle()) < 90:
        pass
    stop()

    print("Sono pronto a raggiungere il centro della stanza sul lato lungo")

    distance = getDistanceCmPort(4)
    dritto()
    while distance < 60 - halfRobot:
        distance = getDistanceCmPort(4)
    stop()

    print("HO RAGGIUNTO IL CENTRO")


def leftLong():
    print("Ho rilevato l'entrata a sinistra sul lato lungo della stanza\n")

    gyro_sensor.reset_angle(0)
    ruotaSuAsse(1)
    while abs(gyro_sensor.angle()) < 90:
        pass
    stop()

    print("Ho ruotato a destra perchè ho visto il muro a sinistra, raggiungo il centro del lato lungo\n")

    distance = getDistanceCmPort(4)
    dritto()  
    while distance < (60 - halfRobot):
        distance = getDistanceCmPort(4)
    stop()

    print("Sono al centro del lato lungo della stanza\n\nRuoto sull'asse in senso antiorario")

    gyro_sensor.reset_angle(0)
    ruotaSuAsse(-1)
    while abs(gyro_sensor.angle()) < 90:
        pass
    stop()

    print("Sono pronto a raggiungere il centro della stanza sul lato corto")

    distance = getDistanceCmPort(4)
    dritto()
    while distance < 40 - halfRobot:
        distance = getDistanceCmPort(4)
    stop()

    print("HO RAGGIUNTO IL CENTRO")

def rightLong():
    print("Ho rilevato l'entrata a destra sul lato lungo della stanza\n")

    gyro_sensor.reset_angle(0)
    ruotaSuAsse(-1)
    while abs(gyro_sensor.angle()) < 90:
        pass
    stop()

    print("Ho ruotato a sinistra perchè ho visto il muro a destra, raggiungo il centro del lato lungo\n")

    distance = getDistanceCmPort(4)
    dritto()  
    while distance < (60 - halfRobot):
        distance = getDistanceCmPort(4)
    stop()

    print("Sono al centro del lato lungo della stanza\n\nRuoto sull'asse in senso orario")

    gyro_sensor.reset_angle(0)
    ruotaSuAsse(1)
    while abs(gyro_sensor.angle()) < 90:
        pass
    stop()

    print("Sono pronto a raggiungere il centro della stanza sul lato corto")

    distance = getDistanceCmPort(4)
    dritto()
    while distance < 40 - halfRobot:
        distance = getDistanceCmPort(4)
    stop()

    print("HO RAGGIUNTO IL CENTRO")
    



# Trova se si trova a sinistra o a destra della stanza. 
# Se, leggendo i sensori, la distanza di sinistra è minore della distanza di destra vuol dire che l'entrata è a sinistra(1). Altrimenti è a destra (2)
if sensorReadingLeft < sensorReadingRight:
    side = 1
else:
    side = 2

### CONTROLLO PALLINE
# controllo aggiuntivo per capire se ci sono palline:
# se le misure sono entrambe piccole, o comunque non sono come dovrebbero essere (120 * 90) riprova prima a farle sul posto
# se vede ancora misure piccole vuol dire che ha trovato la pallina per sbaglio, quindi si muove un attimo in avanti e fa di nuovo i controlli


# Legge poi il sensore davanti. Se la distanza è maggiore di 50 cm (metà stanza più la dimensione del robot, circa 20 cm, da sistemare per bene)
# vuol dire che è entrato dal lato corto della stanza (1) altrimenti è entrato dal lato lungo (2)
if sensorReadingFront > 50:
    longOrShort = 1
else:
    longOrShort = 2

if side == 1 and longOrShort == 1:
    # Si trova a sinistra nel lato corto della stanza
    leftShort()
elif side == 2 and longOrShort == 2:
    # Si trova a destra nel lato corto della stanza
    rightShort()
elif side == 1 and longOrShort == 2:
    # Si trova a sinistra nel lato lungo della stanza
    leftLong()
elif side == 2 and longOrShort == 2:
    # Si trova a destra nel lato lungo della stanza
    rightLong()


# Una volta raggiunto il centro non resettiamo più l'angolo, così teniamo sempre il "nord"
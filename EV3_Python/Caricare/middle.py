#!/usr/bin/env pybricks-micropython
from rescue_line_setup import *
from rescue_line_functions import *
from client_functions import *

robotFranco = 14
halfRobot = robotFranco/2


sensorReadingFront = getDistanceCm(DIST_FRONT)
sensorReadingLeft = getDistanceCm(DIST_LEFT)
sensorReadingRight = getDistanceCm(DIST_RIGHT)

side = 0
longOrShort = 0


def dritto():
    robot.drive(100, 0)

def ruotaSuAsse( verso ):
    robot.drive(0, (30 * verso))

def stop():
    robot.stop()


### FUNZIONI PER GUADAGNARE IL CENTRO

def stanzaFunc(destraSinistra, lungoCorto):
    rotazione2 = destraSinistra * -1

    firstMiddle = 40 if lungoCorto == 1 else 60
    secondMiddle = 60 if lungoCorto == 1 else 40

    gyro_sensor.reset_angle(0)
    ruotaSuAsse(destraSinistra)
    while abs(gyro_sensor.angle()) < 90:
        pass
    stop()

    distance = getDistanceCm(DIST_BACK)
    dritto()
    while distance < firstMiddle - halfRobot:
        print("Ho richiesto la distanza")
        distance = getDistanceCm(DIST_BACK)
    stop()

    gyro_sensor.reset_angle(0)
    ruotaSuAsse(rotazione2)
    while abs(gyro_sensor.angle()) < 90:
        pass
    stop()

    distance = getDistanceCm(DIST_BACK)
    dritto()
    while distance < secondMiddle - halfRobot:
        distance = getDistanceCm(DIST_BACK)
    stop()

    gyro_sensor.reset_angle(0)


# Trova se si trova a sinistra o a destra della stanza. 
# Se, leggendo i sensori, la distanza di sinistra è minore della distanza di destra vuol dire che l'entrata è a sinistra(1). Altrimenti è a destra (2)
if sensorReadingLeft < sensorReadingRight:
    side = 1
else:
    side = -1

### CONTROLLO PALLINE
# controllo aggiuntivo per capire se ci sono palline:
# se le misure sono entrambe piccole, o comunque non sono come dovrebbero essere (120 * 90) riprova prima a farle sul posto
# se vede ancora misure piccole vuol dire che ha trovato la pallina per sbaglio, quindi si muove un attimo in avanti e fa di nuovo i controlli


# Legge poi il sensore davanti. Se la distanza è maggiore di 50 cm (metà stanza più la dimensione del robot, circa 20 cm, da sistemare per bene)
# vuol dire che è entrato dal lato corto della stanza (1) altrimenti è entrato dal lato lungo (2)
if sensorReadingFront > 50:
    longOrShort = 1
else:
    longOrShort = -1


stanzaFunc(side, longOrShort)

# Una volta raggiunto il centro non resettiamo più l'angolo, così teniamo sempre il "nord"
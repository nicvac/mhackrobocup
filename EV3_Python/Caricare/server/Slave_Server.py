#!/usr/bin/env pybricks-micropython

# Messaging
# https://pybricks.com/ev3-micropython/messaging.html
# ATTENZIONE: USANDO IL MECCANISMO DI WAIT REQUEST DAL CLIENT, SI RISCHIA DI PERDERSI LA SINCRONIA 
#  FRA SERVERE E CLIENT, SERVER PERDE LA RICHIESTA DEL CLIENT E RIMANE INDEFINITIVAMENTE IN WAIT.
#  QUINDI LA WAIT LA FA SOLO IL SERVER E IL CLIENT LEGGE A RIPETIZIONE SENZA WAIT


from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor, InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.media.ev3dev import SoundFile, ImageFile
from pybricks.messaging import BluetoothMailboxServer, TextMailbox, NumericMailbox

from server_commands import *

import time

brick = EV3Brick()


# Before running this program, make sure the client and server EV3 bricks are
# paired using Bluetooth, but do NOT connect them. The program will take care
# of establishing the connection.

# The server must be started before the client!

#Suona N beep
def brick_speaker_beep( num ):
    for i in range( num ):
        brick.speaker.beep()
        if num > 0: 
            time.sleep(0.1)


ultrasonic_sensor_front = UltrasonicSensor(Port.S1)
ultrasonic_sensor_left = UltrasonicSensor(Port.S2)
ultrasonic_sensor_right = UltrasonicSensor(Port.S3)
ultrasonic_sensor_back = UltrasonicSensor(Port.S4)

server = BluetoothMailboxServer()


extDist = NumericMailbox('extDist', server)

# The server must be started before the client!
brick_speaker_beep(1)
print('waiting for connection...')
server.wait_for_connection()
print('connected!')

#count = 0

switchoff = True

while True:
    extDist.wait()
    req = extDist.read()
    if   req == DIST_FRONT:
        extDist.send(ultrasonic_sensor_front.distance())
    elif req == DIST_BACK:
        extDist.send(ultrasonic_sensor_back.distance())
    elif req == DIST_LEFT:
        extDist.send(ultrasonic_sensor_left.distance())
    elif req == DIST_RIGHT:
        extDist.send(ultrasonic_sensor_right.distance())

    elif req == DIST_FRONT_OFF:
        extDist.send(ultrasonic_sensor_front.distance(switchoff))
    elif req == DIST_BACK_OFF:
        extDist.send(ultrasonic_sensor_back.distance(switchoff))
    elif req == DIST_LEFT_OFF:
        extDist.send(ultrasonic_sensor_left.distance(switchoff))
    elif req == DIST_RIGHT_OFF:
        extDist.send(ultrasonic_sensor_right.distance(switchoff))

    #count += 1
    #print(count)
    
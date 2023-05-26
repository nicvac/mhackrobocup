#!/usr/bin/env pybricks-micropython

# Messaging
# https://pybricks.com/ev3-micropython/messaging.html
# ATTENZIONE: USANDO IL MECCANISMO DI WAIT REQUEST DAL CLIENT, SI RISCHIA DI PERDERSI LA SINCRONIA 
#  FRA SERVERE E CLIENT, SERVER PERDE LA RICHIESTA DEL CLIENT E RIMANE INDEFINITIVAMENTE IN WAIT.
#  QUINDI RACCOLGO I DATI DAL SENSORE E LI SPARO A RIPETIZIONE. SARA' SOLO IL CLIENT A FARE WAIT 
#  QUANDO GLI SERVE


from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor, InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.media.ev3dev import SoundFile, ImageFile
from pybricks.messaging import BluetoothMailboxServer, TextMailbox, NumericMailbox

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

extDistFront = NumericMailbox('extDistFront', server)
extDistBack  = NumericMailbox('extDistBack', server)
extDistLeft  = NumericMailbox('extDistLeft', server)
extDistRight  = NumericMailbox('extDistRight', server)

# The server must be started before the client!
brick_speaker_beep(1)
print('waiting for connection...')
server.wait_for_connection()
print('connected!')


while True:
    time.sleep(0.02)
    extDistFront.send(ultrasonic_sensor_front.distance())
    extDistBack.send(ultrasonic_sensor_back.distance())
    extDistLeft.send(ultrasonic_sensor_left.distance())
    extDistRight.send(ultrasonic_sensor_right.distance())


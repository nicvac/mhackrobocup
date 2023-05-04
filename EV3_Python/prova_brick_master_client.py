#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor, InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.media.ev3dev import SoundFile, ImageFile
from pybricks.messaging import BluetoothMailboxClient, TextMailbox, NumericMailbox


# This is the name of the remote EV3 or PC we are connecting to.
SERVER = 'ev3devext'

client = BluetoothMailboxClient()
mbox = TextMailbox('greeting', client)
extReq = NumericMailbox('extReq', client)
extDist = NumericMailbox('extDist', client)

print('establishing connection...')
client.connect(SERVER)
print('connected!')

# In this program, the client sends the first message and then waits for the
# server to reply.
mbox.send('hello!')
mbox.wait()
print(mbox.read())

color_sensor_front = ColorSensor(Port.S1)


while True:
    print(color_sensor_front.color())
    colore = color_sensor_front.color()
    if colore == Color.GREEN:
        extReq.send(1)
        extDist.wait()
        print(extDist.read())
       


    
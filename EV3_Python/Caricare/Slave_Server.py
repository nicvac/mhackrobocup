#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor, InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.media.ev3dev import SoundFile, ImageFile
# Before running this program, make sure the client and server EV3 bricks are
# paired using Bluetooth, but do NOT connect them. The program will take care
# of establishing the connection.

# The server must be started before the client!

from pybricks.messaging import BluetoothMailboxServer, TextMailbox, NumericMailbox

ultrasonic_sensor_front = UltrasonicSensor(Port.S1)
ultrasonic_sensor_left = UltrasonicSensor(Port.S2)
ultrasonic_sensor_right = UltrasonicSensor(Port.S3)
ultrasonic_sensor_back = UltrasonicSensor(Port.S4)

server = BluetoothMailboxServer()
#mbox = TextMailbox('greeting', server)

# The server must be started before the client!
print('waiting for connection...')
server.wait_for_connection()
print('connected!')

# In this program, the server waits for the client to send the first message
# and then sends a reply.
# mbox.wait()
# print(mbox.read())
# mbox.send('hello to you!')

while True:
    extDist = NumericMailbox('extDist', server)
    extDist.wait()
    req = extDist.read()
    if req == 1:
        extDist.send(ultrasonic_sensor_front.distance())
    elif req == 2:
        extDist.send(ultrasonic_sensor_left.distance())
    elif req == 3:
        extDist.send(ultrasonic_sensor_right.distance())
    else:
        extDist.send(ultrasonic_sensor_back.distance())


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
import time

sopra_motore_sinistra = Motor(Port.A)
sopra_motore_destra = Motor(Port.B)

ultrasonic_sensor_back = UltrasonicSensor(Port.S4)

sopra_motore_destra.hold()
sopra_motore_sinistra.hold()

while True:
    distanza = ultrasonic_sensor_back.distance()

    if distanza > 65 and distanza < 75:
        sopra_motore_sinistra.run_angle(300, -100)
        sopra_motore_destra.run_angle(300, -100)

        sopra_motore_destra.hold()
        sopra_motore_sinistra.hold()
        
        sopra_motore_sinistra.run_angle(300, 100)
        sopra_motore_destra.run_angle(300, 100)









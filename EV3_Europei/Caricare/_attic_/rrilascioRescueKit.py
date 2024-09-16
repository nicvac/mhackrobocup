#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor, InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.media.ev3dev import SoundFile, ImageFile
from pybricks.messaging import BluetoothMailboxServer, TextMailbox, NumericMailbox


rescueKit = Motor(Port.B)

rescueKit.run_angle(-140, 110)
rescueKit.run_until_stalled(140)
rescueKit.run_angle(-140, 110)
rescueKit.run_until_stalled(140)
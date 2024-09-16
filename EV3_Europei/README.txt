Per far funzionare il programma installare da terminale pybricks

pip install pybricks

comandi necessari

LIBRERIE

#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor, InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile


MOTORI:

gira 90 gradi

robot.settings(30, 100, 90)
primo argomento = potenza sul dritto
secondo argomento = accelerazione sul dritto
terzo argomento = potenza curva
quarto argomento = accelerazione curva


robot.turn(60)
argomento = angolo di curva

robot.stop()
per resettare le impostazioni e poterle cambiare


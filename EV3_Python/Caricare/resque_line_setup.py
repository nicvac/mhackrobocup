from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor, InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile

# Diametro ruota in mm
wheel = 32.5
wheel = 35

# Distanza dal centro delle ruote da sinistra a destra
axle = 205

# Lunghezza dei cingoli (i due sensori di colore devono essere allineati all'inizio dei cingoli)
lungCingoli = 140

# Motore grande destra
right_motor = Motor(Port.A)

# Motore grande sinistra
left_motor = Motor(Port.B)

# Sensore di colore destra
color_sensor_right = ColorSensor(Port.S2)

# Sensore di colore sinistra
color_sensor_left = ColorSensor(Port.S3)

# Giroscopio
gyro_sensor = GyroSensor(Port.S1)

# Sensore in luce riflessa fronte
light_sensor_front = ColorSensor(Port.S4)

#Sensore in colore trasformato fronte
#color_sensor_front = ColorSensor(Port.S4)

# Sensore ultrasuoni
# ultrasonic_sensor = UltrasonicSensor(Port.S1)

# Configurazione robot
#@@@ Correggere i valori di axle e wheel secondo la guida riportata qui:
# Measuring and validating the robot dimensions, https://pybricks.com/ev3-micropython/robotics.html#
robot = DriveBase(left_motor, right_motor, wheel_diameter=wheel, axle_track=axle)

# Motor max power deg/s
# Da specifica 1020. Da test arriva a 780 (forse a causa delle batterie scariche)
motor_max_spec_degs = 1020 
#Velocità massima di avanzamento
motor_max_degs = motor_max_spec_degs / 6 #Soglia ottimale di movimento. Non perde le curve a gomito
#mtr_side_black_degs = -motor_max_degs * 40/100
#mtr_side_white_degs =  motor_max_degs * 50/100
mtr_side_black_degs = -motor_max_degs * 50/100
mtr_side_white_degs =  motor_max_degs * 50/100

stampa = True

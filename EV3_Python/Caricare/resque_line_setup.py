from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor, InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile
import time

brick = EV3Brick()

# Diametro ruota in mm
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
###########################
### A T T E N Z I O N E ###
#@@@ Correggere i valori di axle e wheel secondo la guida riportata qui:
# Measuring and validating the robot dimensions, https://pybricks.com/ev3-micropython/robotics.html#
robot = DriveBase(left_motor, right_motor, wheel_diameter=wheel, axle_track=axle)

# Motor max power deg/s
# Da specifica 1020. Da test arriva a 780 (forse a causa delle batterie scariche)
motor_max_spec_degs = 1020 
#Velocità massima di avanzamento
#motor_max_degs = motor_max_spec_degs / 6 #Soglia ottimale di movimento. Non perde le curve a gomito
motor_max_degs = motor_max_spec_degs / 8 #Più lento, ma più stabile
#mtr_side_black_degs = -motor_max_degs * 40/100
#mtr_side_white_degs =  motor_max_degs * 50/100
mtr_side_black_degs = -motor_max_degs * 50/100
mtr_side_white_degs =  motor_max_degs * 50/100

stampa = True

print("### SETUP ###")
print("motor_max_degs: ",motor_max_degs)

#La uso per il calcolo dinamico delle soglie
# Diversi parametri soglia sono calibrati su motor_max_degs=200
# Al variare di motor_max_degs devono variare anche le soglie
def retta_da_due_punti(x1, y1, x2, y2):
    m = (y2 - y1) / (x2 - x1)
    c = y1 - m * x1
    return m, c

# Quante volte consecutive devo fare forward per resettare i contatori di correzione per il loop detection
x1=motor_max_spec_degs / 8 # Velocità a cui sono stati calibrati i vari y1
y1=3
m, c = retta_da_due_punti(x1, y1, x1/2, y1*2)
loop_detected_reset_soglia = round(motor_max_degs * m + c)
print("loop_detected_reset_soglia: ", loop_detected_reset_soglia)

#loop_detected_soglia = 70 # a 66 ha trovato 3 bianchi ed è ripartito il loop di detection
# Se fra correzioni a destra e a sinistra (senza andare mai avanti) arrivo a questa soglia in totale ==> loop detected
#y1=80
#y1=40
y1=50
m, c = retta_da_due_punti(x1, y1, x1/2, y1*2)
loop_detected_soglia = round(motor_max_degs * m + c)
print("loop_detected_soglia: ", loop_detected_soglia)

# Quante volte consecutive vedo bianco su tutti e tre i sensori per ritenermi perso
y1=140
m, c = retta_da_due_punti(x1, y1, x1/2, y1*2)
lost_soglia = round(motor_max_degs * m + c)
print("lost_soglia: ", lost_soglia)

# Soglia per detection curva a gomito Sx o Dx
y1=20
m, c = retta_da_due_punti(x1, y1, x1/2, y1*2)
gomito_soglia = round(motor_max_degs * m + c)
print("gomito_soglia: ", gomito_soglia)

# PARAMETRI DI SCAN
# Di quanto devo avanzare prima di cominciare uno scan
# Ad esempio dopo un loop potrei essere su una curva a gomito. Metto il vertice sotto i cingoli avanzando di un tot e poi parte lo scan
# Meno avanzo, meno sarà l'angolo di scan. Misurato con il goniometro il caso lungCingoli/4
scan_forward = lungCingoli/4
x1 = lungCingoli/2; y1 = 90+45 # Metto il vertice sull'asse, ma avanzare troppo non copre tutti gli scenari
x2 = lungCingoli/4; y2 = 90+35 #
m, c = retta_da_due_punti(x1, y1, x2, y2)
scan_degree = scan_forward * m + c
print("scan_forward: ", scan_forward, "; scan_degree: ",scan_degree)

print("### #### ###")

# [DEPRECATED]
#Dopo X correzioni, se vedo ancora linea sullo stesso sensore per X volte ==> è una curva a gomito
# Se usi un valore troppo alto, la correzione continua fino a non vedere più il nero e quindi viene considerato percorso smooth
# Se usi un valore troppo basso, alcune correzioni smooth vengono interrotte e fa una detect di una curva a gomito, 
#  quando invece doveva semplicemente continuare a correggere 
# Il valore di soglia dipende dalla velocità dei motori, perchè più veloce è il motore, meno campionamenti si fanno e quindi più bassa deve essere la soglia
# Abbiamo visto che  per motor_max_degs = motor_max_spec_degs / 6 = 1020 / 6 = 170 ==> un buon valore di soglia è 30. 
# Quindi per ottenere f(170)=30 e f(170*2)=30/2, ci serve una funzione lineare che passi dai punti (170,30) and (340,15):
# Query su www.wolframalpha.com: the equation of the linear function that passes through the points (170,30) and (340,15):
# f(x) = -(3/34)x + 45
# curvaGomitoSoglia = 30 # 30 va bene per motor_max_degs = motor_max_spec_degs / 6
# curvaGomitoSoglia =  -(3/34) * motor_max_degs + 45
# curvaGomitoSoglia = 40
# curvaGomitoSoglia = 10
# print(motor_max_degs, "  ", curvaGomitoSoglia)

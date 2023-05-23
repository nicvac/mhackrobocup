from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor, InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile
from pybricks.messaging import BluetoothMailboxClient, TextMailbox, NumericMailbox

import time


brick = EV3Brick()

#Il brick server (fornisce le distanze)
SERVER = 'ev3devExt'

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


# Motore grande sopra sinistra
upper_left_motor = Motor(Port.C)

# Motore grande sopra destra
upper_right_motor = Motor(Port.D)

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

# Motore medio
# medium_motor = Motor(Port.D)

# Configurazione robot
###########################
### A T T E N Z I O N E ###
#@@@ Correggere i valori di axle e wheel secondo la guida riportata qui:
# Measuring and validating the robot dimensions, https://pybricks.com/ev3-micropython/robotics.html#
robot = DriveBase(left_motor, right_motor, wheel_diameter=wheel, axle_track=axle)

# Motor max power deg/s
# Da specifica 1020. Da test arriva a 780 (forse a causa delle batterie scariche)
motor_max_spec_degs = 1020 
#Limite della velocità imposto da noi
motor_max_degs = motor_max_spec_degs / 8 
#Più lento, ma più stabile. Percorso a corna calibrato su questa velocità
motor_max_pwrperc = 63.75
mtr_side_black_pwrperc = -motor_max_pwrperc
mtr_side_white_pwrperc =  motor_max_pwrperc



ignoreDistanceSensorCounter = 0

correzionePerIncrocio = 0


#Velocità da usare per gli scan
motor_scan_degs = motor_max_degs * 0.5

stampa = True

print("### SETUP ###")
print("motor_max_degs: ",motor_max_degs)
print("motor_max_pwrperc: ",motor_max_pwrperc)
print("mtr_side_black_pwrperc: ",mtr_side_black_pwrperc)
print("mtr_side_white_pwrperc: ",mtr_side_white_pwrperc)

#La uso per il calcolo dinamico delle soglie
# Diversi parametri soglia sono calibrati su motor_max_pwrperc
# Al variare di motor_max_pwrperc devono variare anche le soglie
def retta_da_due_punti(x1, y1, x2, y2):
    m = (y2 - y1) / (x2 - x1)
    c = y1 - m * x1
    return m, c

# ATTENZIONE! LE SOGLIE DIPENDONO FORTEMENTE DAL VALORE DI motor_max_pwrperc!!!
# PIU' ALTO E' motor_max_pwrperc MINORI SARANNO I CAMPIONAMENTI E QUINDI LE SOGLIE CAMBIANO!
# QUESTE SOGLIE SONO STATE CALIBRATE SU motor_max_pwrperc = 63.75
# Tips: PUOI USARE retta_da_due_punti PER DETERMINARE IL VALORE DI UNA SOGLIA A PARTIRE DA motor_max_pwrperc, es.:
#   x1=motor_max_pwrperc # Velocità a cui sono stati calibrati i vari y1
#   y1=3
#   m, c = retta_da_due_punti(x1, y1, x1/2, y1*2) #Cioè al dimezzarsi di x raddoppia y
#   soglia = round(motor_max_pwrperc * m + c)


# Quante volte consecutive devo fare forward per resettare i contatori di correzione per il loop detection
loop_detected_reset_soglia = 3
print("loop_detected_reset_soglia: ", loop_detected_reset_soglia)

#loop_detected_soglia = 70 # a 66 ha trovato 3 bianchi ed è ripartito il loop di detection
# Se fra correzioni a destra e a sinistra (senza andare mai avanti) arrivo a questa soglia in totale ==> loop detected
#y1=80
#y1=40
loop_detected_soglia = 50
print("loop_detected_soglia: ", loop_detected_soglia)

# Quante volte consecutive vedo bianco su tutti e tre i sensori per ritenermi perso
lost_soglia = 140
print("lost_soglia: ", lost_soglia)

# Soglia per detection curva a gomito Sx o Dx
gomito_soglia = 20
print("gomito_soglia: ", gomito_soglia)

# PARAMETRI DI SCAN
# Di quanto devo avanzare prima di cominciare uno scan
# Ad esempio dopo un loop potrei essere su una curva a gomito. Metto il vertice sotto i cingoli avanzando di un tot e poi parte lo scan
# Meno avanzo, meno sarà l'angolo di scan. Misurato con il goniometro il caso lungCingoli/4
def scan_forward_2_scan_degree( scan_forward_mm ):
    x1 = lungCingoli/2; y1 = 90+45 # Metto il vertice sull'asse, ma avanzare troppo non copre tutti gli scenari
    x2 = lungCingoli/4; y2 = 90+35 #
    m, c = retta_da_due_punti(x1, y1, x2, y2)
    scan_degree = scan_forward_mm * m + c
    print("scan_forward: ", scan_forward_mm, "; scan_degree: ",scan_degree)
    return scan_degree

scan_forward_def = lungCingoli/4
print("scan_forward_def: ", scan_forward_def)





print("### #### ###")



print("OPERAZIONE DI CONNESSIONE AL SERVER AVVIATA, COMMENTARE SE NON SERVE")

SERVER = 'ev3devExt'

client = BluetoothMailboxClient()
mbox = TextMailbox('greeting', client)
extDist = NumericMailbox('extDist', client)

print('establishing connection...')
client.connect(SERVER)
print('connected!')

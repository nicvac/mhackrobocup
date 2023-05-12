#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor, InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile

import time

#Ritorna vero se linea
def isLine( color ):
    return (color == Color.BLACK or color == Color.BLUE or color == Color.BROWN)

#Ritorna vero se linea - Luce riflessa
def isLineF( light ):
    return (light <= 10)

#Scan
#Ruoto sul mio asse fino a degree angoli fino a centrare la linea fra i due sensori L e R
#Senso orario: degree positivo
#abs_ignora_degrees: angolo da ignorare dall'inizio dello scan (in valore assoluto)
def scan( degree , abs_ignora_degrees):

    print("Scan di max ", degree, "°")

    motor_scan_degs = motor_max_degs * 0.5 * ( -1 if degree < 0 else 1)
    
    #seleziono il sensore corretto a seconda della scansione oraria/antioraria
    color_sensor = color_sensor_right if degree > 0 else color_sensor_left

    lineLocked = False
    lineMet = False
    linePassed = False

    #Dovo aver scelto il sensore giusto, ruoto su asse fino a incontrare la linea e a sorpassarla
    gyro_sensor.reset_angle(0)
    robot.drive(0, motor_scan_degs)
    deg_abs = abs(degree)

    current_angle = abs(gyro_sensor.angle())
    while current_angle < deg_abs and not lineLocked:
        if current_angle <= abs_ignora_degrees:
            pass
        else:
            color = color_sensor.color()
            if not lineMet:
                lineMet = isLine(color)
            else:
                linePassed = not isLine(color)
            lineLocked = lineMet and linePassed

        current_angle = abs(gyro_sensor.angle())
        
    robot.drive(0, 0)

    #Se lo scan non ha trovato linee => Torno alla posizione di partenza
    if not lineLocked:
        robot.drive(0, -motor_scan_degs)
        if degree < 0:
            while ( gyro_sensor.angle() < 0 ) : pass
        else:
            while ( gyro_sensor.angle() > 0 ) : pass
        robot.drive(0, 0)

    print("Scan lock ", lineLocked)

    robot.stop()
    return lineLocked


#Scan in una direzione. Se non trova nulla scan nell'altra direzione
def scan_double( degree , abs_ignora_degrees):
    lineLocked = False    
    lineLocked = scan(degree , abs_ignora_degrees)
    if not lineLocked:
        #Non ho trovato la linea dove mi sarei aspettato. Provo dall'altra parte
        lineLocked = scan(-degree , abs_ignora_degrees)
    return lineLocked


def isGreen(color):
    return (color == Color.GREEN)


def verde360():
    robot.straight(lungCingoli / 2)

    gyro_sensor.reset_angle(0)

    robot.drive(0, 60)

    while gyro_sensor.angle() < 180: print(gyro_sensor.angle())

    robot.drive(0, 0)

    print("HO CORRETTO")

    robot.stop()


lc_counter = None

reset_counter = 0

reset_side_l = 1
reset_side_r = 2
reset_side = 0



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

###############
#DEBUG SENSORS
''' 
while True:  
    colorl = color_sensor_left.color()
    colorr = color_sensor_right.color()
    print (colorl, " ",colorr)
'''

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

curvaGomitoSoglia = 10 #rregolare non detected
#curvaGomitoSoglia = 20
print(motor_max_degs, "  ", curvaGomitoSoglia)

#Quante volte vedo CONSECUTIVAMENTE una linea, sul sensore sinistro e destro
lc_l = 0; lc_r = 0; lc_f = 0;
lc_l_max = 0; lc_r_max = 0;

bc_l = 0; bc_r = 0; bc_f = 0;

gyro_sensor.reset_angle(0)

isLine_l = False; isLine_r = False


while True:  

    gl = isGreen(color_sensor_left.color())
    gr = isGreen(color_sensor_right.color())

    # if gl and not gr:
    #     print("Ho vist verde a sinistra")
    #     robot.straight(lungCingoli / 3)
    #     scan(-100, 40)
    # elif gr and not gl:
    #     print("Ho vist verde a destra")
    #     robot.straight(lungCingoli / 3)
    #     scan(100, 40)
    # elif gr and gl:
    #     print("Ho vist verde da tutti e due i lati")
    #     verde360()

    
    color_l = color_sensor_left.color()
    color_r = color_sensor_right.color()
    light_f = light_sensor_front.reflection()
    
    isLine_l = isLine(color_l)
    isLine_r = isLine(color_r)
    isLine_f = isLineF(light_f)
    
    lc_l_prev = lc_l
    lc_r_prev = lc_r

    #Line counter: Incremento il contatore se è linea e lo era anche al giro precedente
    lc_l = lc_l + 1 if isLine_l else 0
    lc_r = lc_r + 1 if isLine_r else 0
    lc_f = lc_f + 1 if isLine_f else 0
    #Blank counte
    bc_l = bc_l + 1 if not isLine_l else 0
    bc_r = bc_r + 1 if not isLine_r else 0
    bc_f = bc_f + 1 if not isLine_f else 0

    if bc_l >= 50 and bc_r >= 50 and bc_f >= 50:
        lineFound = False
        left_motor.hold()
        right_motor.hold()
        robot.drive(-100, 0)
        while not lineFound:
            color_l = color_sensor_left.color()
            color_r = color_sensor_right.color()
            light_f = light_sensor_front.reflection()
            lineFound = isLine(color_l) or isLine(color_r) or isLineF(light_f)
            
        robot.stop()
        robot.straight(30)
        robot.stop()
        scan_double(60, 0)
        
        

    if bc_l >= 10 and bc_r >= 10: reset_counter = 0

    if lc_l_prev > 0 and lc_l == 0 and lc_r > 0 and lc_r_prev > 0 and lc_r_prev < lc_l_prev: 
        lc_r = 1
        print("Resettato r")
        lc_l_max = max(lc_l_max, lc_l_prev)
        if reset_counter == 0:
            reset_side = reset_side_r
            print("Ho finito correzione a sinista. E' la prima del loop.")
        # reset_counter += 1

        if reset_counter == 0 and lc_l_prev > curvaGomitoSoglia:
            reset_counter += 1
        elif reset_counter == 0 and lc_l_prev < curvaGomitoSoglia:
            reset_counter = 0
            print("Correzione nominale detected")
        else:
            reset_counter += 1
        # if lc_l_prev > curvaGomitoSoglia:
        #     reset_counter += 1
        # else: 
        #     reset_counter = 0
        #     print("Correzione nominale detected")

    if lc_r_prev > 0 and lc_r == 0 and lc_l > 0 and lc_l_prev > 0 and lc_l_prev < lc_r_prev:
        lc_l = 1
        print("Resettato l")
        lc_r_max = max(lc_r_max, lc_r_prev)
        if reset_counter == 0:
            reset_side = reset_side_l
            print("Ho finito correzione a destra. E' la prima del loop.")
        # reset_counter += 1

        if reset_counter == 0 and lc_r_prev > curvaGomitoSoglia:
            reset_counter += 1
        elif reset_counter == 0 and lc_r_prev < curvaGomitoSoglia:
            reset_counter = 0
            print("Correzione nominale detected")
        else: 
            reset_counter += 1

        # if lc_r_prev > curvaGomitoSoglia:
        #     reset_counter += 1
        # else: 
        #     reset_counter = 0
        #     print("Correzione nominale detected")

    


    if stampa == True:
        #print(right_motor.speed())
        #print("L: ", colorl, "; Line: ", isLine(colorl))
        #print("R: ", colorr, "; Line: ", isLine(colorr))
        dl = 1 if isLine_l else 0
        dr = 1 if isLine_r else 0
        df = 1 if isLine_f else 0
        print ( dl, "-", df, "-", dr, "   ", lc_l, "-", lc_f, "-", lc_r, "       ", reset_counter)

    #Finchè riesce a correggersi in poche iterazioni, considero la posizione stabile => sono ad angolo 0.
    if max(lc_l, lc_r) <= 4:
        gyro_sensor.reset_angle(0)

    #Nessuno dei due sensori è sulla linea => vado dritto
    if not isLine_l and not isLine_r :
        left_motor.dc(mtr_side_white_degs)
        right_motor.dc(mtr_side_white_degs)
    
    else:
        #Almeno uno dei due sensori è sulla linea
        correctLeft = False; correctRight = False
        #Se entrambi sono sulla linea, continuo con la stessa correzione con cui ho cominciato
        if isLine_l and isLine_r:
            if lc_l >= lc_r:
                correctLeft = True;  correctRight = False
            else:
                correctLeft = False; correctRight = True
        #Se solo uno dei due è sulla linea, applico la correzione opportuna
        else:
            correctLeft  = isLine_l
            correctRight = isLine_r 

        if correctLeft: 
            left_motor.dc ( mtr_side_black_degs )
            right_motor.dc( mtr_side_white_degs )
        if correctRight:
            right_motor.dc( mtr_side_black_degs )
            left_motor.dc ( mtr_side_white_degs )

    #Detection curva a gomito: sono sulla linea da diverse iterazioni: nonostante la correzione continuo a leggere linea.
    # tipico di una curva a gomito
    # gomitoSx = lc_l > curvaGomitoSoglia
    # gomitoDx = lc_r > curvaGomitoSoglia

    gomitoSx = reset_counter >= 3 and reset_side == reset_side_r
    gomitoDx = reset_counter >= 3 and reset_side == reset_side_l

    # gomitoSx = reset_counter >= 3 and lc_l_max >= lc_r_max
    # gomitoDx = reset_counter >= 3 and lc_r_max >= lc_l_max


    if gomitoSx or gomitoDx:
        reset_counter = 0

        print("Contatori in fase loop: ",lc_l_max, " ", lc_r_max)
        print("Curva a gomito a sinitra.") if gomitoSx else print("Curva a gomito a destra")
        # Mi Fermo
        right_motor.hold()
        left_motor.hold()

        #quit()

        #Ripristino la posizione allo stesso angolo di quando ero stabile (prima della curva a gomito)
        angle = gyro_sensor.angle()
        print("Angolo da ripristinare: ", angle)
        
        if abs(angle) >= 5:
            if gomitoSx:
                right_motor.dc( mtr_side_black_degs )
                left_motor.dc( mtr_side_white_degs )
            else: # if gomitoDx:
                left_motor.dc( mtr_side_black_degs )
                right_motor.dc( mtr_side_white_degs )

            current_angle = gyro_sensor.angle()
            if current_angle < 0:
                while gyro_sensor.angle() < 0: pass
            else:
                while gyro_sensor.angle() > 0: pass


        print("Angolo ripristinato")
        #while abs(gyro_sensor.angle()) >= 2 : pass
        right_motor.hold()
        left_motor.hold()

        #Avanzo di mezzo robot, posizionando la curva a gomito sotto il robot, al centro
        #robot.straight( lungCingoli/4 )
        robot.straight( 30 ) #Test su curve a corna
        print("Avanzo di un quarto di cinglo")

        #Avendo il vertice della curva a gomito sotto il mio asse perpendicolare, eseguo uno scan
        lineLocked = False

        #ruota in senso orario o antiorario (a seconda della curva a gomito) fino a ritrovare la linea
        scanDegree = 100 * (-1 if gomitoSx else 1)
        
        lineLocked = scan_double(scanDegree, 0)

        if lineLocked :
            #Qui ho ritrovato la linea
            lc_l = 0; lc_r = 0
            gyro_sensor.reset_angle(0)
        else:
            print("MI SONO PERSO DOPO LA CURVA A GOMITO.")
            lineLocked = scan_double(180, 0)
            #@@@ GESTIRE QUESTO CASO.
            quit()



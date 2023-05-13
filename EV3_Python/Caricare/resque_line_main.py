#!/usr/bin/env pybricks-micropython

import time

from resque_line_functions import *
from resque_line_setup import *

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
loop_detected_soglia = 70

#Line counter: Quante volte vedo CONSECUTIVAMENTE una linea, su tutti i sensori
lc_l = 0; lc_r = 0; lc_f = 0;
#Blank counter: Quante volte vedo CONSECUTIVAMENTE bianco, su tutti i sensori
bc_l = 0; bc_r = 0; bc_f = 0;

def resetCountersLine_lc_bc():
    lc_l = 0; lc_r = 0; lc_f = 0;
    bc_l = 0; bc_r = 0; bc_f = 0;

#Detection di un loop su asse (sx-dx-sx-dx ecc...)
corrc_fwd = 0; corrc_left = 0; corrc_right = 0
corrc_list_l = []; corrc_list_r = []; 

def resetCountersCorrection_corrc():
    corrc_fwd = 0; corrc_left = 0; corrc_right = 0
    corrc_list_l = []; corrc_list_r = []; 

gyro_sensor.reset_angle(0)

isLine_l = False; isLine_r = False


while True:  

    #Lettura di tutti i sensori nel loop corrente
    color_l = color_sensor_left.color()
    color_r = color_sensor_right.color()
    light_f = light_sensor_front.reflection()

    ### VERDI
    '''
    gl = isGreen( color_l )
    gr = isGreen( color_r )

    if gl and not gr:
        print("Ho vist verde a sinistra")
        robot.straight(lungCingoli / 3)
        scan(-100, 40)
    elif gr and not gl:
        print("Ho vist verde a destra")
        robot.straight(lungCingoli / 3)
        scan(100, 40)
    elif gr and gl:
        print("Ho vist verde da tutti e due i lati")
        verde360()
    
    if gl or gr: 
        continue
    '''
    
    isLine_l = isLine(color_l)
    isLine_r = isLine(color_r)
    isLine_f = isLineF(light_f)
    
    #Line counter: Incremento il contatore se è linea e lo era anche al giro precedente
    lc_l = lc_l + 1 if isLine_l else 0
    lc_r = lc_r + 1 if isLine_r else 0
    lc_f = lc_f + 1 if isLine_f else 0
    #Blank counter
    bc_l = bc_l + 1 if not isLine_l else 0
    bc_r = bc_r + 1 if not isLine_r else 0
    bc_f = bc_f + 1 if not isLine_f else 0

    corrc_list_l.append(lc_l)
    corrc_list_r.append(lc_r)
    if stampa == True:
        #print(right_motor.speed())
        dl = 1 if isLine_l else 0
        dr = 1 if isLine_r else 0
        df = 1 if isLine_f else 0
        print ( dl, "-", df, "-", dr, "   ", lc_l, "-", lc_f, "-", lc_r)

    '''
    #Ho perso la strada. Torno indietro
    if bc_l >= 50 and bc_r >= 50 and bc_f >= 50:
        left_motor.hold()
        right_motor.hold()
        robot.drive(-100, 0)
        lineFound = False
        while not lineFound:
            color_l = color_sensor_left.color()
            color_r = color_sensor_right.color()
            light_f = light_sensor_front.reflection()
            lineFound = isLine(color_l) or isLine(color_r) or isLineF(light_f)
            
        robot.stop()
        robot.straight(30)
        robot.stop()
        lineLock = scan_double(60, 0)
        continue
    '''

    #Nessuno dei due sensori è sulla linea => vado dritto
    if not isLine_l and not isLine_r :
        left_motor.dc(mtr_side_white_degs)
        right_motor.dc(mtr_side_white_degs)
        corrc_fwd += 1
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

        #@@@ TBC: abbassare mtr_side_*_degs all'aumentare di corrc_*
        #         per essere più precisi nelle curve a gomito strettissime

        if correctLeft: 
            left_motor.dc ( mtr_side_black_degs )
            right_motor.dc( mtr_side_white_degs )
            corrc_left += 1

        if correctRight:
            right_motor.dc( mtr_side_black_degs )
            left_motor.dc ( mtr_side_white_degs )
            corrc_right += 1

    #Finchè riesce a correggersi in poche iterazioni, considero la posizione stabile => sono ad angolo 0.
    if corrc_fwd >= 2:
        resetCountersCorrection_corrc()
        gyro_sensor.reset_angle(0)

    # LOOP DETECTION: sono fermo sull'asse a correggere a destra-sinistra continuamente, senza avanzare mai.
    # Sono sulla linea da diverse iterazioni: nonostante la correzione continuo a leggere linea.
    # Tipico di una curva a gomito
    loop_detected = corrc_left >= loop_detected_soglia and corrc_right >= loop_detected_soglia
    
    if not loop_detected: 
        continue

    #Qui sono in loop di correzioni dx-sx. 
    # Procedo con uno scan. Determino se iniziare con uno scan a destra o a sinistra
    # Mi Fermo
    right_motor.hold()
    left_motor.hold()

    gomitoSx = isGomitoSx(corrc_list_l, corrc_list_r)
    gomitoDx = not gomitoSx

    print("Curva a gomito a sinitra.") if gomitoSx else print("Curva a gomito a destra")

    #Ripristino la posizione allo stesso angolo di quando ero stabile (prima della curva a gomito)
    angle = gyro_sensor.angle()
    print("Angolo da ripristinare: ", angle)
    
    current_angle = gyro_sensor.angle()

    if gomitoSx:
        right_motor.dc( mtr_side_black_degs * 1/4 )
        left_motor.dc( mtr_side_white_degs  * 1/4)
    else: # if gomitoDx:
        left_motor.dc( mtr_side_black_degs * 1/4)
        right_motor.dc( mtr_side_white_degs * 1/4 )

    if current_angle < 0:
        while gyro_sensor.angle() < 0: pass
    else:
        while gyro_sensor.angle() > 0: pass

    print("Angolo ripristinato")
    right_motor.hold()
    left_motor.hold()

    #Avanzo di mezzo robot, posizionando la curva a gomito sotto il robot, al centro
    robot.straight( lungCingoli/4 )
    print("Avanzo di un quarto di cinglo")

    #Avendo il vertice della curva a gomito sotto il mio asse perpendicolare, eseguo uno scan
    lineLocked = False

    #Ruota in senso orario o antiorario (a seconda della curva a gomito) fino a ritrovare la linea
    scanDegree = 100 * (-1 if gomitoSx else 1)
    
    lineLocked = scan_double(scanDegree, 0)

    if not lineLocked:
        print("DOUBLE SCAN FALLITO. ESEGUO DEGLI SCAN RIPETUTI FINO A TROVARE LA STRADA")
    while not lineLocked:
        robot.straight(50) #5 cm
        robot.stop()
        lineLocked = scan_double(scanDegree, 0)

    #Qui ho ritrovato la linea
    resetCountersLine_lc_bc()
    resetCountersCorrection_corrc()
    gyro_sensor.reset_angle(0)



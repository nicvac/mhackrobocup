#!/usr/bin/env pybricks-micropython

import time

from rescue_line_functions import *
from rescue_line_setup import *

#Line counter: Quante volte vedo CONSECUTIVAMENTE una linea, su tutti i sensori
lc_l = 0; lc_r = 0; lc_f = 0
#Blank counter: Quante volte vedo CONSECUTIVAMENTE bianco, su tutti i sensori
bc_l = 0; bc_r = 0; bc_f = 0

def resetCountersLine_lc_bc():
    global lc_l, lc_r, lc_f
    global bc_l, bc_r, bc_f
    lc_l = 0; lc_r = 0; lc_f = 0
    bc_l = 0; bc_r = 0; bc_f = 0

#Detection di un loop su asse (sx-dx-sx-dx ecc...)
corrc_fwd = 0; corrc_left = 0; corrc_right = 0
corrc_list_l = list()
corrc_list_r = list()

def resetCountersCorrection_corrc():
    global corrc_fwd, corrc_left, corrc_right
    corrc_fwd = 0; corrc_left = 0; corrc_right = 0
    corrc_list_l.clear()
    corrc_list_r.clear() 
    #print("Correction counters corrc clear", "\t\t Corr: ", corrc_fwd," ", corrc_left, " ", corrc_right)

gyro_sensor.reset_angle(0)

isLine_l = False; isLine_r = False


while True:  
    
    # isObstacle = checkIfObstacle()
    # if isObstacle: aggiraOstacolo()
    

    #Lettura di tutti i sensori nel loop corrente
    color_l = color_sensor_left.color()
    color_r = color_sensor_right.color()
    light_f = light_sensor_front.reflection()

    ### VERDI
    isGreen_l = isGreen( color_l )
    isGreen_r = isGreen( color_r )

    # if isGreen_l and not isGreen_r:
    #     print("Ho visto verde a sinistra")
    #     scan_deg = scan_forward_2_scan_degree(lungCingoli / 3)
    #     robot.straight(lungCingoli / 3)
    #     scan(-scan_deg, 40, False)
    # elif isGreen_r and not isGreen_l:
    #     print("Ho visto verde a destra")
    #     scan_deg = scan_forward_2_scan_degree(lungCingoli / 3)
    #     robot.straight(lungCingoli / 3)
    #     scan(scan_deg, 40, False)
    # elif isGreen_r and isGreen_l:
    #     print("Ho visto verde da tutti e due i lati")
    #     verde360()
    
    if isGreen_l or isGreen_r: 
        continue
    
    ### SEGUI LINEA
    isLine_l = isLine(color_l)
    isLine_r = isLine(color_r)
    isLine_f = isLineF(light_f)

    ### GAP
    #Da testare, se i sensori laterali vedono bianco e il frontale vede nero, e poi il fontale vede bianco => vai avanti e controlla i sensori laterali
    # flag_gap = False
    # if not isLine_l and not isLine_r and isLine_f:
    #     flag_gap = True
    # else:
    #     flag_gap = False
    # if flag_gap:
    #     left_motor.dc(80)
    #     right_motor.dc(80)



    # Da testare, se tutti e tre i sensori vedono nero fa uno skip in avanti
    # Problemi possibili:
    # Nelle corna tutti e tre i sensori possono vedere nero, quindi può fare lo skip in una direzione sbagliata e perdersi
    if isLine_l and isLine_r and isLine_f and correzionePerIncrocio >= 50:
        skip()
        correzionePerIncrocio = 0
        print("Skip incrocio nero nero nero")
    elif isLine_l and not isLine_r and isLine_f and correzionePerIncrocio >= 50:
        skip()
        correzionePerIncrocio = 0
        print("Skip incrocio nero sinistra nero avanti bianco destra")
    if isLine_r and not isLine_l and isLine_f and correzionePerIncrocio >= 50:
        skip()
        correzionePerIncrocio = 0
        print("Skip incrocio nero destra nero avanti bianco sinistra")
    

    #Line counter: Incremento il contatore se è linea e lo era anche al giro precedente
    lc_l = lc_l + 1 if isLine_l else 0
    lc_r = lc_r + 1 if isLine_r else 0
    lc_f = lc_f + 1 if isLine_f else 0
    
    #Blank counter: Incremento il contatore se non è linea e non lo era anche al giro precedente
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
        print( ". ",dl,"-",dr,"\t",lc_l,"-",lc_r,"\t\t F: ",df," ",lc_f, "\t\t Corr:(", corrc_fwd,") ", corrc_left, " ", corrc_right, "\t Incrocio: ", correzionePerIncrocio)

    #Ho perso la strada. Torno indietro e recupero il percorso Triplo bianco
    #@@@ QUI BISOGNA DISTINGUERE IL CASO GAP
    # if bc_l >= lost_soglia and bc_r >= lost_soglia and bc_f >= lost_soglia:
    #     print("I TRE SENSORI VEDONO BIANCO DA ", lost_soglia, " ITERAZIONI")
    #     left_motor.hold()
    #     right_motor.hold()
    #     brick_speaker_beep(3)

    #     robot.drive(-100, 0)
    #     lineFound = False
    #     while not lineFound:
    #         color_l = color_sensor_left.color()
    #         color_r = color_sensor_right.color()
    #         light_f = light_sensor_front.reflection()
    #         lineFound = isLine(color_l) or isLine(color_r) or isLineF(light_f)
            
    #     robot.stop()
    #     robot.straight(30)
    #     robot.stop()
    #     lineLock = scan_double(60, 0, True)
    #     continue

    


    #Nessuno dei due sensori è sulla linea => vado dritto
    if not isLine_l and not isLine_r :
        left_motor.dc(mtr_side_white_pwrperc)
        right_motor.dc(mtr_side_white_pwrperc)
        corrc_fwd += 1
        correzionePerIncrocio += 1
        
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
            left_motor.dc ( mtr_side_black_pwrperc )
            right_motor.dc( mtr_side_white_pwrperc )
            corrc_left += 1; corrc_fwd = 0; correzionePerIncrocio = 0

        if correctRight:
            right_motor.dc( mtr_side_black_pwrperc )
            left_motor.dc ( mtr_side_white_pwrperc )
            corrc_right += 1; corrc_fwd = 0; correzionePerIncrocio = 0

    #Finchè riesce a correggersi in poche iterazioni, considero la posizione stabile => sono ad angolo 0.
    if corrc_fwd >= loop_detected_reset_soglia:
        resetCountersCorrection_corrc()
        gyro_sensor.reset_angle(0)

    # LOOP DETECTION: sono fermo sull'asse a correggere a destra-sinistra continuamente, senza avanzare mai.
    # Sono sulla linea da diverse iterazioni: nonostante la correzione continuo a leggere linea.
    # Tipico di una curva a gomito
    loop_detected = corrc_left >= loop_detected_soglia and corrc_right >= loop_detected_soglia
    
    if not loop_detected: 
        continue

    print("LOOP DETECTED!")
    #Qui sono in loop di correzioni dx-sx. 
    # Procedo con uno scan. Determino se iniziare con uno scan a destra o a sinistra
    # Mi Fermo
    right_motor.hold()
    left_motor.hold()

    gomitoSx = isGomitoSx(corrc_list_l, corrc_list_r)
    gomitoDx = not gomitoSx

    print("Curva a gomito a sinitra.") if gomitoSx else print("Curva a gomito a destra")

    #Ripristino la posizione allo stesso angolo di quando ero stabile (prima della curva a gomito)
    angle_to_restore = -1 * gyro_sensor.angle()
    print("Angolo da ripristinare: ", angle_to_restore)

    if angle_to_restore > 0:
        right_motor.dc( mtr_side_black_pwrperc * 0.9 )
        left_motor.dc( mtr_side_white_pwrperc * 0.9)
    else: # if gomitoDx:
        left_motor.dc( mtr_side_black_pwrperc * 0.9)
        right_motor.dc( mtr_side_white_pwrperc * 0.9)

    if angle_to_restore > 0:
        while gyro_sensor.angle() < 0: pass
    else:
        while gyro_sensor.angle() > 0: pass

    print("Angolo ripristinato")
    right_motor.hold()
    left_motor.hold()


    # caso per gestire la cuva a T. Se ripristina l'angolo e vede nero con il sensore di fronte non fa partire la scansione
    # il sensore davanti passa un attimo in modalità colore per essere sicuri di non sbagliare con la lettura della luce
    new_color_f = light_sensor_front.color()
    
    new_is_line_f = isLine(new_color_f)
    # se, dopo aver resettato l'angolo, il sensore vede la linea fa uno skip in avanti e supera l'incrocio
    # da provare con tutti i casi in cui potrebbe partire la scansione.
    # va messo prima dell "avanzo per tenere il vertice sotto" perchè se ci troviamo in curve strette rischiamo di vedere la linea avanti.
    # testato con l'incrocio a T a sinistra e a destra e funziona.
    if new_is_line_f:
        robot.straight(30)
        robot.stop()
        print("Ho trovato un incrocio a T, non serve eseguire la scansione")
        resetCountersCorrection_corrc()
        continue

    #Mi posiziono in un punto ottimale per far partire lo scan
    #Avanzo, posizionando la curva a gomito sotto il robot
    print("Avanzo per tenere il vertice sotto")
    robot.straight( scan_forward_def )

    #Avendo il vertice della curva a gomito sotto il mio asse perpendicolare, eseguo uno scan
    lineLocked = False

    #Ruota in senso orario o antiorario (a seconda della curva a gomito) fino a ritrovare la linea
    scan_degree = scan_forward_2_scan_degree(scan_forward_def)
    curr_scan_degree = ( scan_degree ) * (-1 if gomitoSx else 1)
    
    lineLocked = scan_double(curr_scan_degree, 0, True)

    if not lineLocked:
        print("DOUBLE SCAN FALLITO. ESEGUO DEGLI SCAN RIPETUTI FINO A TROVARE LA STRADA")
    while not lineLocked:
        robot.straight(50) #5 cm
        robot.stop()
        lineLocked = scan_double(curr_scan_degree, 0, True)

    #Qui ho ritrovato la linea
    resetCountersLine_lc_bc()
    resetCountersCorrection_corrc()
    gyro_sensor.reset_angle(0)



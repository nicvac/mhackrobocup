#!/usr/bin/env pybricks-micropython
from rescue_line_functions import *
from rescue_line_setup import *
from stanza_main import *
#from guadagna_centro import *



# sensorOff(DIST_BACK_OFF)
# time.sleep(0.2)
# sensorOff(DIST_LEFT_OFF)
# time.sleep(0.2)
# sensorOff(DIST_RIGHT_OFF)
# time.sleep(0.2)

# getDistanceCm(DIST_FRONT)
# getDistanceCm(DIST_FRONT)

#Line counter: Quante volte vedo CONSECUTIVAMENTE una linea, su tutti i sensori
lc_l = 0; lc_r = 0; lc_f = 0
#Blank counter: Quante volte vedo CONSECUTIVAMENTE bianco, su tutti i sensori
bc_l = 0; bc_r = 0; bc_f = 0
#Blank counter gap: Vedo bianco però si resetta quando uno dei sensori vede nero
fullGapCounter = 0
start=time.time()

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

imposta_carrello_rescueline()
gyro_sensor.reset_angle(0)

isLine_l = False; isLine_r = False

countVerdi = 0
while True:  
    
    #SE PREMO UN PULSANTE (TRANNE STOP!!!) RIAVVIA IL SERVER ED ESCE DAL PROGRAMMA (Questo alla fine ignorato malamente?)
    check_quit_and_restart_server()

    ## OSTACOLO
    ############################
    ### URGENTISSIMO TESTARE ###
    ############################
    # Funzione aggira ostacolo. Da sistemare con tutti gli aggiornamenti fatti al client-server durante il percorso.
    # Potrebbe dare problemi con le troppe letture durante il percorso, bisogna impostargli uno sleep.
    if time.time()-start>=1:
        isObstacle = checkIfObstacle()
        if isObstacle: aggiraOstacolo()
        start=time.time()
    

    ### STAGNOLA
    lightFront = light_sensor_front.reflection()
    stagnola = isStagnola(lightFront)
    if stagnola:
        print("Ho visto la luminosità maggiore del 90%")
        robot.drive(0,0) 
        robot.stop()
        stanzaTrovata = stagnolaTrovata()
        if stanzaTrovata:
            stanza_main()
        else:
            print("Non ho trovato la stanza, continuo il seguilinea")
            # far andare un attimo in avanti ed eseguire lo scan se tutti e tre vedono bianco
            ####################
            ### URGENTISSIMO ###
            ####################
            robot.drive(0,0)
            robot.stop()

            # Se quando non vede la stagnola non ritrova la linea legge un attimo tutti i sensori
            lineLee = isLine(color_sensor_left.color())
            lineRii = isLine(color_sensor_right.color())
            lineFrr = isLineF(light_sensor_front.reflection())
            # Se uno dei tre sensori vede la linea riprende normalmente il seguilinea
            if lineLee or lineRii or lineFrr:
                continue
            # Se non ritrova la linea va un attimo avanti e avvia la scansione. Se la linea sta avanti la ritroverà mai? Non lo scopriremo mai :)
            else:
                # Non so se funziona
                scan_deg = scan_forward_2_scan_degree(lungCingoli / 2)
                robot.straight(lungCingoli / 2)
                scan(scan_deg, 0, False)

    else:
        pass

    


    #Lettura di tutti i sensori nel loop corrente
    color_l = color_sensor_left.color()
    color_r = color_sensor_right.color()
    light_f = light_sensor_front.reflection()

    ### VERDI
    isGreen_l = isGreen( color_l )
    isGreen_r = isGreen( color_r )

    countVerdi = countVerdi + 1 if isGreen_l or isGreen_r else 0

    attivaVerde = True

    if attivaVerde and (isGreen_l or isGreen_r and countVerdi >= 3):
        robot.stop()
        brick_speaker_beep(3)

        # risolvere errore verde a caso nel percorso oppure non vede il doppio verde
        # quando vede un verde con uno dei due sensori resetta l'ultimo angolo stabile e fa un passetto in avanti per essere
        # sicuri di essere al centro del quadratino verde
        oldAngle = gyro_sensor.angle()
        resetAngleGreen()
        robot.straight(5)
        # qui fa il controllo normalmente. Se non vede nessun verde nella posizione stabile non esegue nessuna correzione
        if isGreen_l and not isGreen_r:
            print("Ho visto verde a sinistra")
            countVerdi = 0
            scan_deg = scan_forward_2_scan_degree(lungCingoli / 2)
            robot.straight(lungCingoli / 2)
            scan(-scan_deg, 40, False)

        elif isGreen_r and not isGreen_l:
            print("Ho visto verde a destra")
            countVerdi = 0
            scan_deg = scan_forward_2_scan_degree(lungCingoli / 2)
            robot.straight(lungCingoli / 2)
            scan(scan_deg, 40, False)
        elif isGreen_r and isGreen_l:
            print("Ho visto verde da tutti e due i lati")
            countVerdi = 0
            verde360()
        else:
            # forse è il caso di fargli riprendere l'angolo prima che ha visto il verde. Se lo vede durante una curva
            # stretta è probabile che ristabilisca l'anglo stabile lontano dalla linea, quindi non vede niente e si perde
            # bisogna fare comunque un po' di tentavi
            resetBackAngleAfterNoGreen(oldAngle)
            continue
    
    # if isGreen_l or isGreen_r: 
    #     continue
    
    ### SEGUI LINEA
    isLine_l = isLine(color_l)
    isLine_r = isLine(color_r)
    isLine_f = isLineF(light_f)



    ### INCROCI
    # Da testare, se tutti e tre i sensori vedono nero fa uno skip in avanti
    # Problemi possibili:
    # Nelle corna tutti e tre i sensori possono vedere nero, quindi può fare lo skip in una direzione sbagliata e perdersi
    if isLine_l and isLine_r and isLine_f:
        skip()
        correzionePerIncrocio = 0
        print("Skip incrocio nero nero nero")
    # elif isLine_l and not isLine_r and isLine_f and correzionePerIncrocio >= 50:
    #     skip()
    #     correzionePerIncrocio = 0
    #     print("Skip incrocio nero sinistra nero avanti bianco destra")
    # if isLine_r and not isLine_l and isLine_f and correzionePerIncrocio >= 50:
    #     skip()
    #     correzionePerIncrocio = 0
    #     print("Skip incrocio nero destra nero avanti bianco sinistra")
    


    #Line counter: Incremento il contatore se è linea e lo era anche al giro precedente
    lc_l = lc_l + 1 if isLine_l else 0
    lc_r = lc_r + 1 if isLine_r else 0
    lc_f = lc_f + 1 if isLine_f else 0
    
    #Blank counter: Incremento il contatore se non è linea e non lo era anche al giro precedente
    bc_l = bc_l + 1 if not isLine_l else 0
    bc_r = bc_r + 1 if not isLine_r else 0
    bc_f = bc_f + 1 if not isLine_f else 0

    fullGapCounter = fullGapCounter + 1 if not isLine_l and not isLine_r and not isLine_f else 0
    

    corrc_list_l.append(lc_l)
    corrc_list_r.append(lc_r)

    if stampa == True:
        #print(right_motor.speed())
        dl = 1 if isLine_l else 0
        dr = 1 if isLine_r else 0
        df = 1 if isLine_f else 0
        print( ". ",dl,"-",dr,"\t",lc_l,"-",lc_r,"\t\t F: ",df," ",lc_f, "\t\t Corr:(", corrc_fwd,") ", corrc_left, " ", corrc_right, "\t Incrocio: ", correzionePerIncrocio, "\t Contatori Bianco Completo: ", fullGapCounter, "   counterVerdi", countVerdi)


    ### GAP
    if fullGapCounter >= lost_soglia:
        print("I sensori hanno visto 3 volte bianco per tanto tempo")
        robot.stop()
        left_motor.hold()
        right_motor.hold()

        print("Inizio ad andare indietro finchè uno dei miei sensori vede la linea")
        robot.drive(-100, 0)

        while True:

            #SE PREMO UN PULSANTE (TRANNE STOP!!!) RIAVVIA IL SERVER ED ESCE DAL PROGRAMMA
            check_quit_and_restart_server()

            lineLeft = isLine(color_sensor_left.color())
            lineRight = isLine(color_sensor_right.color())
            lineFront = isLineF(light_sensor_front.reflection())

            if lineLeft or lineRight or lineFront:
                if lineLeft: print("Ho trovato la linea a sinistra")
                if lineRight: print("Ho trovato la linea a destra")
                if lineFront: print("Ho trovato la linea davanti")
                break
        robot.stop()

        front = True if lineFront else False
        side = 1 if lineLeft and not lineRight else -1


        if front:
            print("Ho ritrovato la linea con il sensore al centro")
            gyro_sensor.reset_angle(0)
            ruotaSuAsse(1)
            while abs(gyro_sensor.angle() < 20):
                pass
            stop()
            robot.straight(-50)
            stop()
            fullGapCounter = -100
            continue

        # side = 1 vuol dire che il sensore di sinistra ha visto per primo la linea
        if side == 1:
            print("Sono entrato in side 1")
            gyro_sensor.reset_angle(0)
            # gira sull'asse finchè il sensore non vede più nero oppure fino a quando l'angolo è minore di 45, sennò gira troppo (modificare a seconda dei casi, fare delle prove)
            ruotaSuAsse(side)
            while isLine(color_sensor_left.color()) and abs(gyro_sensor.angle()) < 45:
                pass
            robot.stop()
            robot.straight(100)
            robot.stop()
            fullGapCounter = -100
            continue
        # side = -1 il destroo ha visto per primo la linea
        elif side == -1:
            print("Sono entrato in side -1")
            gyro_sensor.reset_angle(0)
            ruotaSuAsse(side)
            while isLine(color_sensor_right.color()) and abs(gyro_sensor.angle()) < 45:
                pass
            robot.stop()
            robot.straight(100)
            robot.stop()
            fullGapCounter = -100
            continue



            
    
    ### BIANCO BIANCO BIANCO
    ### GAP CHE NON FUNZIONA
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

# # caso per gestire la cuva a T. Se ripristina l'angolo e vede nero con il sensore di fronte non fa partire la scansione
    # incrocio = rilevaIncrocio()



    # Seconda prova per l'incrocio a T.
    # Se trova il loop fa partire una scansione di 10° per lato con il sensore davanti
    # Se trova la linea vuol dire che siamo sull'incrocio a T
    # Controllare se basta l'angolo di 10 gradi anche nel caso peggiore.
    # Controllare se anche le corna 
    
    # Fa partire lo scan con il sensore avanti per vedere se si trova all'incrocio 
    lineFoundBack = scanBeforeIntersection()

    if lineFoundBack == 3:
        print("Ho visto verde a sinistra con il controllo incrocio")
        scan_deg = scan_forward_2_scan_degree(lungCingoli / 2)
        robot.straight(lungCingoli / 2)
        scan(-scan_deg, 40, False)
    elif lineFoundBack == 4:
        print("Ho visto verde a destra con il controllo incrocio")
        scan_deg = scan_forward_2_scan_degree(lungCingoli / 2)
        robot.straight(lungCingoli / 2)
        scan(scan_deg, 40, False)
    elif lineFoundBack == 1:
        # Se ha trovato la linea fa uno skip in avanti e supera l'incrocio, resettando tutti i counter
        print("Ho trovato l'incrocio a T, salto lo scan.")
        robot.straight(30)
        stop()
        resetCountersCorrection_corrc()
        continue
    elif lineFoundBack == 0:
        # Se non ha trovato la linea va avanti con la scansione
        pass

    # se ha trovato l'incrocio resetta tutti i contatoiri. 
    # È fondamentale perchè se trova l'incrocio e lo supera, ma i contatori non si sono resettati, fa partire la scansione
    # perchè si ricorda dell'incrocio di prima
    # if incrocio:
    #     resetCountersCorrection_corrc()
    #     continue
    # else:
    #     pass

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



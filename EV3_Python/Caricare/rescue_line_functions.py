from rescue_line_setup import *
from client_functions import *



#Confronto a meno di un errore
def simile( a, b, errore = 1.0 ):
  return ( abs(a - b) <= errore )


#Suona N beep
def brick_speaker_beep( num ):
    #brick.speaker.say("Yes")
    for i in range( num ):
        brick.speaker.beep()
        if num > 0: 
            time.sleep(0.1)

# ABBASSA IL CARRELLO E LO ALZA ALLA POSIZIONE DI START
def imposta_carrello_stanza():
    upper_right_motor.stop()
    upper_left_motor.run_until_stalled(-50)
    time.sleep(1)

    upper_left_motor.reset_angle(0)
    while upper_left_motor.angle() < 70: #80 120
        upper_left_motor.dc(50)
        upper_right_motor.dc(50)

    upper_left_motor.hold()
    upper_right_motor.hold()

def imposta_carrello_rescueline():
    upper_right_motor.stop()
    upper_left_motor.run_until_stalled(50)
    upper_left_motor.hold()
    upper_right_motor.hold()

#Legge il colore avanzando di dist_cm. Ritorna il colore più frequente
def color_scan(sensor_color, dist_cm, speed_cms=1):
    #Output
    max_color = None
    max_samples = -1

    #Scan 
    count_color=dict()
    robot.drive(speed_cms*10, 0)
    start_mm = robot.distance()
    while robot.distance() - start_mm < dist_cm*10:
        color = sensor_color.color()
        if color != None:
            count_color.setdefault(color, list())
            count_color[color].append(1)
    robot.stop()
    
    #Colore più frequente
    for color in count_color:
        samples = count_color[color]
        if len(samples) > max_samples:
            max_color = color
            max_samples = len(samples)

    return max_color, max_samples


#Ritorna vero se linea
#@@@ CALIBRARE I COLORI!!! A SECONDA DELL'AMBIENTE
def isLine( color ):
    #return (color == Color.BLACK or color == Color.BLUE or color == Color.BROWN)
    #return (color == Color.BLACK or color == Color.BROWN)
    return (color == Color.BLACK)

#Ritorna vero se linea - Luce riflessa
def isLineF( light ):
    return (light <= 10)

#Rotazioni con giroscopio
#preserva_angolo: vero => dopo la rotazione viene fatto il reset dell'angolo di start.
def robot_gyro_turn( degree, preserva_angolo = False ):
    if degree == 0: return
    speed_degs = motor_scan_degs * 0.5
    startdeg = gyro_sensor.angle()
    stopdeg = startdeg + degree
    robot.drive(0, speed_degs * (1 if degree > 0 else -1))
    if degree > 0:
        while gyro_sensor.angle() < stopdeg : pass
    else:    
        while gyro_sensor.angle() > stopdeg : pass
    robot.drive(0, 0)
    robot.stop()
    if preserva_angolo:
        gyro_sensor.reset_angle(startdeg)

def dritto():
    robot.drive(100, 0)

def ruotaSuAsse( verso ):
    robot.drive(0, (30 * verso))

def stop():
    robot.stop()

#Scan
#Ruoto sul mio asse fino a degree angoli fino a centrare la linea fra i due sensori L e R
#Senso orario: degree positivo
# abs_ignora_degrees: angolo da ignorare dall'inizio dello scan (in valore assoluto)
# lock_front_also: anche il sensore frontale deve vedere linea
# lock_front_also conviene usarlo per uno scan a valle di una curva a gomito. 
#    perchè se la detection della curva a gomito sbaglia, il frontale non vede (quasi) mai linea
#    e quindi faccio partire lo scan dall'altra parte (la direzione giusta)
#    Invece non serve attivarlo dopo la detection del verde perchè il verde mi dà già 
#    la direzione corretta, non si può sbagliare.
def scan( degree , abs_ignora_degrees, lock_front_also):

    #Salvo l'angolo di partenza
    angle_save = gyro_sensor.angle()

    print("Scan di max ", degree, "°. Ignoro primi ", abs_ignora_degrees, "°; lock_front_also",lock_front_also)

    #Tieni una velocità bassa. Altrimenti i cingoli slittano sfalsando tutto (un po' per volta può tornare indietro)
    motor_scan_degs = motor_max_degs * 0.5 * ( -1 if degree < 0 else 1)
    
    #seleziono il sensore corretto a seconda della scansione oraria/antioraria
    color_sensor = color_sensor_right if degree > 0 else color_sensor_left

    lineLocked = False
    lineMet = False #Trovo una linea
    linePassed = False #La sorpasso

    lineMetFront = False #Trovo una linea con il sensore frontale

    #Dovo aver scelto il sensore giusto, ruoto su asse fino a incontrare la linea e a sorpassarla
    gyro_sensor.reset_angle(0)
    robot.drive(0, motor_scan_degs)
    deg_abs = abs(degree)

    current_angle = abs(gyro_sensor.angle())
    while current_angle < deg_abs and not lineLocked:
        #SE PREMO UN PULSANTE (TRANNE STOP!!!) RIAVVIA IL SERVER ED ESCE DAL PROGRAMMA
        check_quit_and_restart_server()

        if current_angle <= abs_ignora_degrees:
            pass
        else:
            color = color_sensor.color()
            lineMet = lineMet or isLine(color)
            linePassed = lineMet and (linePassed or not isLine(color))

            if not lineMetFront:
                refl = light_sensor_front.reflection()
                lineMetFront = isLineF(refl)

            if lock_front_also:
                lineLocked = lineMet and linePassed and lineMetFront
            else:
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

    print("Scan: lineMet: ",lineMet,"; linePassed: ",linePassed, "; lineMetFront: ", lineMetFront)
    print("Scan lock ", lineLocked)

    robot.stop()

    #Ripristino l'angolo prima della chiamata
    angle_save = gyro_sensor.reset_angle( angle_save )

    return lineLocked


#Scan in una direzione. Se non trova nulla scan nell'altra direzione
def scan_double( degree , abs_ignora_degrees, lock_front_also):
    lineLocked = scan(degree , abs_ignora_degrees, lock_front_also)
    if not lineLocked:
        #Non ho trovato la linea dove mi sarei aspettato. Provo dall'altra parte
        lineLocked = scan(-degree , abs_ignora_degrees, lock_front_also)
    return lineLocked


def isGreen(color):
    return (color == Color.GREEN)


def verde360():
    robot.straight(lungCingoli / 2)

    gyro_sensor.reset_angle(0)

    robot.drive(0, 60)

    while gyro_sensor.angle() < 180: print(gyro_sensor.angle())

    robot.drive(0, 0)

    print("verde360: HO CORRETTO")

    robot.stop()

#Detect curva a gomito
def isGomitoSx(l, r):
    print("####### DETECT Gomito ########")
    for i in range(len(l)):
        print("... [",i,"]\t\t",l[i],"-",r[i])
    print("####### DETECT Gomito END ########")

    isGomSx = False

    delta = 3
    i = 0; found = False; found2 = False
    while i < len(l) and not found:
        if l[i] > gomito_soglia and r[i] > gomito_soglia:
            found = True
            print("... First step Found ",l[i],"-",r[i], " at i=",i)
            found2 = False
            while i < len(l) and not found2:
                if l[i] >= r[i]+delta:
                    found2 = True
                    isGomSx = True
                if r[i] >= l[i]+delta:
                    found2 = True
                    isGomSx = False
                if found2 : print("... Second step Found ",l[i],"-",r[i], " at i=",i)
                i += 1
        i += 1
        
    print("... isGomitoSx. Found: ", found2, "; isGomSx: ", isGomSx)
    if found2:
        brick_speaker_beep(1)
    else:
        brick_speaker_beep(2)
        isGomSx = isGomitoSx_optII(l,r)

    return isGomSx


#Guarda analisi su https://docs.google.com/spreadsheets/d/1zzRqJC8Go7ISH45u8RZzTldJTufcHLqrFenuDwdnGmc/edit?usp=sharing
def isGomitoSx_optII(l, r):
    print("... isGomitoSx_optII")
    distanza = 0
    for i in range(len(l)):
        distanza += (l[i] - r[i])
    
    media = distanza / len(l)
    isGomSx = media > 0    
    print("... isGomitoSx. Media distanze: ", media, "; GomitoSx: ", isGomSx)

    return isGomSx



def checkIfObstacle():
    distanceCm = getDistanceCm(DIST_FRONT)
    # print("Distanza rilevata: ", distanceCm)
    if distanceCm <= 9:
        return True
    else:
        return False


def aggiraOstacolo():

    robot.straight(-100)
    robot.stop()

    gyro_sensor.reset_angle(0)

    getDistanceCm(DIST_LEFT)
    getDistanceCm(DIST_RIGHT)

    # salva la distanza del sensore di sinistra ( porta 2 - sensore sinistra )
    distanceLeft = getDistanceCm(DIST_LEFT)


    # salva la distanza del sensore di destra ( porta 3 - sensore destra )
    distanceRight = getDistanceCm(DIST_RIGHT)

    verso = 1 if distanceLeft < distanceRight else -1


    if verso == 1: print("Ho visto l'ostacolo e la strada libera sembra a destra")
    if verso == -1: print("Ho visto l'ostacolo e la strada libera sembra a sinistra")

    gyro_sensor.reset_angle(0)
    
    # gira sull'asse di 50 gradi
    ruotaSuAsse(verso)
    while abs(gyro_sensor.angle()) < 50:
        print(gyro_sensor.angle())
        
    stop()

    # si allontana dalla linea di 5 centimetri per avviare la scansione con i sensori che vedono bianco bianco bianco
    robot.straight(50)
    robot.stop()

    # inizia a muoversi circumnavigando l'ostacolo
    left_motor.dc(80 if verso == -1 else 30)
    right_motor.dc(30 if verso == -1 else 80)
        

    while True:
        colorl = color_sensor_left.color()
        colorr = color_sensor_right.color()
        lightf = light_sensor_front.color()

        isLineLeft = isLine(colorl)
        isLineRight = isLine(colorr)
        isLineFront = isLine(lightf)

        # se vede con uno dei tre sensori la linea nera interrompe la funzione aggira ostacolo e torna al seguilinea
        if isLineLeft or isLineRight or isLineFront:
            left_motor.hold()
            right_motor.hold()
            sensorOff(DIST_BACK_OFF)
            time.sleep(0.2)
            sensorOff(DIST_LEFT_OFF)
            time.sleep(0.2)
            sensorOff(DIST_RIGHT_OFF)
            time.sleep(0.2)
            return




def skip():
    robot.straight(50)
    robot.stop()


# def rilevaIncrocio():
#     # il sensore davanti passa un attimo in modalità colore per essere sicuri di non sbagliare con la lettura della luce
#     new_color_f = light_sensor_front.color()
    
#     new_is_line_f = isLine(new_color_f)
#     # se, dopo aver resettato l'angolo, il sensore vede la linea fa uno skip in avanti e supera l'incrocio
#     # da provare con tutti i casi in cui potrebbe partire la scansione.
#     # va messo prima dell "avanzo per tenere il vertice sotto" perchè se ci troviamo in curve strette rischiamo di vedere la linea avanti.
#     # testato con l'incrocio a T a sinistra e a destra e funziona.
#     if new_is_line_f:
#         robot.straight(30)
#         robot.stop()
#         print("Ho trovato un incrocio a T, non serve eseguire la scansione")
#         return True
#     else:
#         return False
    


def resetAngleGreen():
    restoreAngle = -1 * gyro_sensor.angle()
    
    if restoreAngle > 0:
        right_motor.dc( mtr_side_black_pwrperc * 0.9 )
        left_motor.dc( mtr_side_white_pwrperc * 0.9)
    else: # if gomitoDx:
        left_motor.dc( mtr_side_black_pwrperc * 0.9)
        right_motor.dc( mtr_side_white_pwrperc * 0.9)

    if restoreAngle > 0:
        while gyro_sensor.angle() < 0: pass
    else:
        while gyro_sensor.angle() > 0: pass

    print("Ripristinato angolo stabile prima di trovare il verde")
    left_motor.hold()
    right_motor.hold()


def resetBackAngleAfterNoGreen(angle):
    currAngle = gyro_sensor.angle()
    if currAngle < angle:
        right_motor.dc( mtr_side_black_pwrperc * 0.9 )
        left_motor.dc( mtr_side_white_pwrperc * 0.9)
    else: # if gomitoDx:
        left_motor.dc( mtr_side_black_pwrperc * 0.9)
        right_motor.dc( mtr_side_white_pwrperc * 0.9)

    if currAngle < angle:
        while gyro_sensor.angle() < 0: pass
    else:
        while gyro_sensor.angle() > 0: pass

    print("Ripristinato angolo di quando ho visto il verde, ignoro i verdi per qualche istante")
    left_motor.hold()
    right_motor.hold()


def scanBeforeIntersection():

    # print("Torno indietro di 2 cm per controllare se c'è un verde")
    # robot.straight(-20)
    # stop()

    # #Ruota a destra di 10 gradi
    # gyro_sensor.reset_angle(0)
    # ruotaSuAsse(1)
    # # finchè l'angolo è minore di 10
    # while abs(gyro_sensor.angle()) < 20:
    #     colorL = color_sensor_left.color()
    #     colorR = color_sensor_right.color()

    #     lineL = isLine(colorL)
    #     lineR = isLine(colorR)

    #     if lineL:
    #         break

    #     greenL = isGreen(colorL)
    #     greenR = isGreen(colorR)

    #     if greenL:
    #         return 3
    #     elif greenR:
    #         return 4
    #     else:
    #         pass
    
    # print("Controllato a destra, niente verde. Resetto l'angolo iniziale.")
    # stop()
    # ruotaSuAsse(-1)

    # curr_angle = gyro_sensor.angle()
    # if curr_angle > 0:
    #     while gyro_sensor.angle() > 0: pass
    # elif curr_angle < 0:
    #     while gyro_sensor.angle() < 0: pass

    # stop()
    # print("Resettato l'angolo iniziale, controllo a sinistra")

    # gyro_sensor.reset_angle(0)
    # ruotaSuAsse(-1)
    # while abs(gyro_sensor.angle()) < 20:
    #     colorL = color_sensor_left.color()
    #     colorR = color_sensor_right.color()

    #     lineL = isLine(colorL)
    #     lineR = isLine(colorR)

    #     if lineR:
    #         break

    #     greenL = isGreen(colorL)
    #     greenR = isGreen(colorR)

    #     if greenL:
    #         return 3
    #     elif greenR:
    #         return 4
    #     else:
    #         pass

    # print("Controllato a sinistra, niente verde. Ripristino l'angolo iniziale")
    # stop()
    # ruotaSuAsse(1)

    # curr_angle = gyro_sensor.angle()
    # if curr_angle > 0:
    #     while gyro_sensor.angle() > 0: pass
    # elif curr_angle < 0:
    #     while gyro_sensor.angle() < 0: pass

    # stop()
    # print("Ripristnato l'angolo iniziale")

    # print("Non ho trovato nessun verde nello scan iniziale")
    # robot.straight(20)


    print("Scan di 10 gradi con il sensore davanti, vedo se tovo la linea per l'incrocio")
    # Resetta l'angolo alla partenza
    gyro_sensor.reset_angle(0)
    
    # Ruota prima a desta di 10 gradi
    ruotaSuAsse(1)
    while abs(gyro_sensor.angle()) < 10:
        colorFront = light_sensor_front.color()
        lineScanIntersection = isLine(colorFront)

        if lineScanIntersection:
            # Se, mentre ruota, trova la linea esce dalla funzione
            stop()
            return 1
        else:
            pass
    
    stop()
    gyro_sensor.reset_angle(0)
    # riprende la posizione iniziale se non ha trovato la linea prima di iniziare un altro scan di 10 gradi verso sinistra
    ruotaSuAsse(-1)
    while abs(gyro_sensor.angle()) < 10:
        pass
    stop()

    # inizia la rotazione di 10 gradi verso sinistra
    gyro_sensor.reset_angle(0)
    ruotaSuAsse(-1)
    while abs(gyro_sensor.angle()) < 10:
        colorFront = light_sensor_front.color()
        lineScanIntersection = isLine(colorFront)

        if lineScanIntersection:
            # se trova la linea nello scan di 10 gradi verso sinistra interrompe la funzione.
            stop()
            return 1
        else:
            pass

    # se ne a destra ne ha sinistra ha trovato niente riprende la posizione di partenza e va avanti nel programma
    stop()
    gyro_sensor.reset_angle(0)
    ruotaSuAsse(1)
    while abs(gyro_sensor.angle()) < 10:
        pass
    stop()

    return 0



def isStagnola(reading):
    return True if reading == 100 else False


def stanza():
    pass

def resetAngle():
    angle = gyro_sensor.angle()

    if angle > 0:
        ruotaSuAsse(-1)
    else:
        ruotaSuAsse(1)

    if angle > 0:
        while gyro_sensor.angle() > 0: pass
        stop()
    else:
        while gyro_sensor.angle() < 0: pass
        stop()


def resetAngleBack(firstAngle):
    if gyro_sensor.angle() > firstAngle:
        ruotaSuAsse(-1)
        while gyro_sensor.angle() > firstAngle: pass
        stop()
    else:
        ruotaSuAsse(1)
        while gyro_sensor.angle() < firstAngle: pass
        stop()


def stagnolaTrovata():
    angleStagnola = gyro_sensor.angle()
    resetAngle()    
    # far andare dritto il robot finchè anche i sensori di dietro vedono la stagnola, prendere bene le misure
    robot.straight(40)
    stop()
    time.sleep(1)
    lightL = color_sensor_left.reflection()
    lightR = color_sensor_right.reflection()
    stagnolaL = isStagnola(lightL)
    stagnolaR = isStagnola(lightR)

    print("Luminosità sinistra: ", lightL, " Luminosità destra: ", lightR)
    if stagnolaL and stagnolaR:
        print("Ho trovato la stanza mader fader ")
        return True
    else:
        # non c'è la stanza. Riprendo l'angolo a prima che ho trovato la stagnola e vado avanti, sperando che non mi incastro nelle rampe mannaggia
        print("Non ho trovato la stanza azzo ")
        robot.straight(-40)
        stop()
        resetAngleBack(angleStagnola)
        return False
        # Ignorare la lettura del sensore davanti per qualche secondo. sennò torna indietro e siamo punto e a capo



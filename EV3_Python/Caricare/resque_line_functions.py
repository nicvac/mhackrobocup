from resque_line_setup import *

#Ritorna vero se linea
#@@@ CALIBRARE I COLORI!!! A SECONDA DELL'AMBIENTE
def isLine( color ):
    #return (color == Color.BLACK or color == Color.BLUE or color == Color.BROWN)
    #return (color == Color.BLACK or color == Color.BROWN)
    return (color == Color.BLACK)

#Ritorna vero se linea - Luce riflessa
def isLineF( light ):
    return (light <= 10)

#Scan
#Ruoto sul mio asse fino a degree angoli fino a centrare la linea fra i due sensori L e R
#Senso orario: degree positivo
#abs_ignora_degrees: angolo da ignorare dall'inizio dello scan (in valore assoluto)
def scan( degree , abs_ignora_degrees):

    #Salvo l'angolo di partenza
    angle_save = gyro_sensor.angle()

    print("Scan di max ", degree, "°. Ignoro primi ", abs_ignora_degrees, "°")

    #Tieni una velocità bassa. Altrimenti i cingoli slittano sfalsando tutto (un po' per volta può tornare indietro)
    motor_scan_degs = motor_max_degs * 0.5 * ( -1 if degree < 0 else 1)
    #motor_scan_degs = motor_max_degs * 1.0 * ( -1 if degree < 0 else 1)
    
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

    #Ripristino l'angolo prima della chiamata
    angle_save = gyro_sensor.reset_angle( angle_save )

    return lineLocked


#Scan in una direzione. Se non trova nulla scan nell'altra direzione
def scan_double( degree , abs_ignora_degrees):
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

    print("verde360: HO CORRETTO")

    robot.stop()


def isGomitoSx(l, r):
    print("####### DETECT Gomito ########")
    for i in range(len(l)):
        print("... [",i,"]\t\t",l[i],"-",r[i])
    print("####### DETECT Gomito END ########")

    isGomSx = False

    i = 0; found = False; found2 = False
    while i < len(l) and not found:
        if l[i] > gomito_soglia and r[i] > gomito_soglia:
            found = True
            print("... First step Found ",l[i],"-",r[i], " at i=",i)
            found2 = False
            while i < len(l) and not found2:
                if l[i] >= r[i]+3:
                    found2 = True
                    isGomSx = True
                if r[i] >= l[i]+3:
                    found2 = True
                    isGomSx = False
                if found2 : print("... Second step Found ",l[i],"-",r[i], " at i=",i)
                i += 1
        i += 1
        
    print("... isGomitoSx. Found: ", found2, "; isGomSx: ", isGomSx)
    return isGomSx

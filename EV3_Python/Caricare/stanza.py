from rescue_line_setup import *


def oggDistCm():
    pass

def evacIndividuaSpike( franco ):
    pass


def evacTrovaERaggiungiPalla( EV_TYPE & evacuationType ):

    isPallina = False
    
    while not isPallina:
        print("evacIndividuaSpike begin")
        oggDistCm(0)
        trovato = evacIndividuaSpike(oggDistCm)

        print("evacIndividuaSpike end. oggDistCm: ", oggDistCm, "; trovato: ", trovato)

        if not trovato:
            evacuationType = EV_USCITA
        
        
        print("evacRaggiungiOggetto begin")
        dirScanDetected = False
        SGVERSO dirScan
        evacRaggiungiOggetto(oggDistCm, dirScan, dirScanDetected)

        if dirScanDetected:
            print("evacCentratiRispettoAlloggetto begin. dirScan: ", dirScan)
            evacCentratiRispettoAlloggetto( dirScan )
            print("evacCentratiRispettoAlloggetto end.")

        isPallina = evacIsPallina( evacuationType )
    
    robot.turn(180) #da modificare con il giroscopio

    evacCatturaPallina()

    print("fine")


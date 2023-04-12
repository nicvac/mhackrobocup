#include "definizioni.h"

//Contatore di distanza stabile
const int distStableCount = 3;

//Velocità durante lo scan
const int scanVel = sgPotenzaGiro / 3;
const bool ruotaSuAsse = true;

//Velocità di avanzamento
const int evacMoveVel = maxspeed / 3;

//Dimensione della pallina
const double sizePallinaCm = 4.5;

//La distanza finale fra robot e oggetto da raggiungere 
const double distFinaleCm = 2;

//Dimensioni della stanza
const double dimRoom1 = 90;
const double dimRoom2 = 120;
const double dimDiag = sqrt( dimRoom1*dimRoom1 + dimRoom2*dimRoom2);

//Dimensione robot
const double dimRobLarg = 15;
const double dimRobAltz = 20;

//Confronto a meno di un errore
inline bool simile( const double & a, const double & b, const double errore = 0.5 ) {
  return ( abs(a - b) <= errore );
}

//Ritorna la dimensione calcolata dai due sensori laterali.
inline double evacGetRoomSize() {
  double currLCm = getDistanceCm(SDLEFT, distStableCount);
  double currRCm = getDistanceCm(SDRIGHT, distStableCount);
  double totCm = currLCm + currRCm + dimRobLarg;
  return totCm;
}

//Avanza di cm (sfrutta il sensore di distanza)
inline void avanzaCm( double cm ) {
  double distStartCm = getDistanceCm(SDFRONT, distStableCount);
  double currDistCm = distStartCm;
  avanza(evacMoveVel);
  while (  distStartCm - currDistCm <= cm ) {
    currDistCm = getDistanceCm(SDFRONT, distStableCount);
  }
  motoriFerma();
}


//Posizionati perpendicolarmente alla stanza.
//In questa posizione i sensori laterali misurano una delle due dimensioni della stanza.
//Dopo questa funzione il robot non punta verso le uscite, nè lateralmente, nè frontalmente.
void evacPosizionatiVerticalmente() {
  //Misuro la dimensione della stanza accross track
  double currRoomSizeAccrossCm = evacGetRoomSize();

  //Faccio un giro di più di 360 gradi finchè non sono perpendicolare alla stanza
  bool sonoInPosizione=false;
  while ( not(sonoInPosizione) ) {

    bool done = false;
    double angle = 0;
    while ( (abs( angle ) <= 370) and (not( simile( currRoomSizeAccrossCm, dimRoom1) or simile( currRoomSizeAccrossCm, dimRoom2) ) ) ) {
      if ( not(done) ) {
        mpu6050.update();
        gira(SGANTIOR, scanVel, ruotaSuAsse);
        done = true;
      }
      angle = mpu6050.getAngleZ();

      currRoomSizeAccrossCm = evacGetRoomSize();
    }
    motoriFerma();

    //Ho trovato una delle dimensioni accross track?
    bool sonoPerpendicolareLateralmente = simile( currRoomSizeAccrossCm, dimRoom1) or simile( currRoomSizeAccrossCm, dimRoom2);
    bool sonoPerpendicolareFrontalmente = false;
    if ( sonoPerpendicolareLateralmente ) {
      //Misuro la dimensione della stanza along track
      ruotaAsse(  90, true );
      double currRoomSizeAlongCm = evacGetRoomSize();
      ruotaAsse( -90, true );
      
      double dimExpectedAlongCm = simile( currRoomSizeAccrossCm, dimRoom1) ? dimRoom2 : dimRoom1;
      sonoPerpendicolareFrontalmente = simile( currRoomSizeAlongCm, dimExpectedAlongCm);

    }
    
    sonoInPosizione = sonoPerpendicolareLateralmente and sonoPerpendicolareFrontalmente;
    if ( sonoInPosizione ) break;

    //Non ho trovato la posizione ottimale.
    //Mi sposto di 10 centimetri lungo la direzione con più spazio e ripeto la ricerca.
    double distFront = getDistanceCm(SDFRONT, distStableCount);
    double distLeft  = getDistanceCm(SDLEFT , distStableCount);
    double distRight = getDistanceCm(SDRIGHT, distStableCount);
    double distCm=0;
    if ( distFront >= distLeft and distFront >= distRight ) {
      //avanza frontalmente
      distCm = distFront;
    } else if ( distLeft >= distFront and distLeft >= distRight ) {
      //girati a destra e avanza
      ruotaAsse( 90, true );
      distCm = distLeft;
    } else {
      //girati a sinistra a avanza
      ruotaAsse( -90, true );
      distCm = distRight;
    }
    //Limito la distanza nel caso sia stato puntato un oggetto fuori dalla stanza
    distCm = min(distCm, dimRoom1);
    //Sono nella direzione di avanzamento. Avanzo di qualche cm nella direzione con più spazio.
    avanzaCm( distCm / 3.0 );

  }

}

//Raggiunge un angolo
void evacRaggiungiAngolo() {

  //Posizionati verticalmente nella stanza
  //Qui non punto alle uscite, nè lateralmente, nè frontalmente.
  evacPosizionatiVerticalmente();

  //Calcola le distanze dalla posizione ottimale
  double distLeft  = getDistanceCm(SDLEFT , distStableCount);
  double distRight = getDistanceCm(SDRIGHT, distStableCount);
  ruotaAsse( 90, true );
  double distNordA  = getDistanceCm(SDLEFT , distStableCount);
  double distSudA  = getDistanceCm(SDRIGHT, distStableCount);
  ruotaAsse( -90, true );

  //Mi avvicino al muro
  double ang90 = (distLeft < distRight ) ? -90 : 90;
  bool orario = ang90 > 0;
  ruotaAsse( ang90, true );

  double distFront = getDistanceCm(SDFRONT, distStableCount);
  bool done = false;
  while (distFront <= 3) {
    if ( not(done) ) {
      avanza(evacMoveVel);
      done = true;
    } 
    distFront = getDistanceCm(SDFRONT, distStableCount);
  }
  motoriFerma();
  //Qui sono a meno di 3 cm da un muro, frontalmente

  //Ricalcolo le distanze laterali
  double distNordB = getDistanceCm( orario? SDLEFT : SDRIGHT, distStableCount);
  double distSudB  = getDistanceCm( orario? SDRIGHT: SDLEFT , distStableCount);

  //@@@ CONTINUA DA QUI
  if ( simile(distNordA, distNordB, 15) ) {

  }


}

//Raggiunge l'angolo rosso
void evacRaggiungiAngoloVerde() {
  //@@@ DA SCRIVERE
}

//Raggiunge l'angolo rosso
void evacRaggiungiAngoloRosso() {
  //@@@ DA SCRIVERE
}


//L'oggetto raggiunto è una pallina
//Restituisce vero se abbiamo raggiunto una pallina
//Restituisce evacuationType: il colore della evacuation zone in cui portare la pallina
bool evacIsPallina( EV_TYPE & evacuationType ) {
  //@@@ Restituire false se qualche sensore dell'infrarosso vede l'entrata o l'uscita dell'evacuation zone, questo nel caso
  //@@@ la spike detection trova un angolo dell'entrata o uscita.
  //@@@ DA SCRIVERE
}

//Cattura la pallina
void evacCatturaPallina() {
  //@@@ DA SCRIVERE
}

//Trova una palla nella stanza e la raggiunge
//Restituisce evacuationType: il colore della evacuation zone in cui portare la pallina
bool dirScanDetected = false;
void evacTrovaERaggiungiPalla( EV_TYPE & evacuationType ) {

  bool isPallina = false;
  while ( not(isPallina) ) {
    //Radar, ruota fino a individuare un oggetto da raggiungere
    Serial.print("evacIndividuaSpike begin");
    double oggDistCm(0); //la distanza dall'oggetto che mi ha determinato lo spike (che ho agganciato)
    evacIndividuaSpike(oggDistCm); 
    Serial.println(String("evacIndividuaSpike end. oggDistCm: ") + oggDistCm);

    //Tieni agganciato l'oggetto ed avvicinati
    Serial.print("evacRaggiungiOggetto begin");
    dirScanDetected = false;
    SGVERSO dirScan;
    evacRaggiungiOggetto(oggDistCm, dirScan, dirScanDetected);
    Serial.println(String("evacRaggiungiOggetto end. oggDistCm: ")+ oggDistCm + "; dirScan: "+ dirScan + "; dirScanDetected: "+ dirScanDetected); 

    //Raggiunto l'oggetto ad una distanza di distFinaleCm
    //Ruoto il robot per centrare meglio l'oggetto
    if ( dirScanDetected ) {
      Serial.println(String("")+"evacCentratiRispettoAlloggetto begin. dirScan: "+dirScan); 
      evacCentratiRispettoAlloggetto( dirScan );
      Serial.println(String("evacCentratiRispettoAlloggetto end.")); 
    }

    //Controlliamo se l'oggetto raggiunto è una pallina
    isPallina = evacIsPallina( evacuationType );

  }

  //Ruoto su me stesso in modo da posizionare la gabbia per catturare la pallina
  ruotaAsse( 180, true );

  //Cattura pallina
  evacCatturaPallina();

}

//Raggiunto l'oggetto, ruoto il robot per centrare al meglio l'oggetto.
// Ruoto finchè non raggiungo la distanza minima.
void evacCentratiRispettoAlloggetto(SGVERSO dirScan ) {

    double currCm = getDistanceCm(SDFRONT, distStableCount);
    double scanMinCm = currCm;

    gira(dirScan, scanVel, ruotaSuAsse);

    bool minimoMigliorato = true;
    while ( minimoMigliorato ) {
      currCm = getDistanceCm(SDFRONT, distStableCount);
      minimoMigliorato = ( currCm <= scanMinCm );
    }
    motoriFerma();

}

//Gira in senso antioratio, come un radar, per individuare uno spike nella distanza
//Continua a ruotare finche le misurazioni successive sono "smooth", cioè finchè osservi un muro
//Fermati quando hai individuato uno spike: potenzialmente un oggetto da prendere.
//Note:
// - se si parte osservando già l'oggetto, la scansione prenderà il prossimo oggetto o lo stesso dopo una rotazione di 360 gradi.
// - a volte aggancia gli spigoli delle entrate. Pazienza... si arriverà allo spigolo e si controllerà che non è una pallina (con il sensore di colore frontale).
void evacIndividuaSpike( double & distCm ) {
  
  //Ruota come un radar, in senso antiorario
  gira(SGANTIOR, scanVel, ruotaSuAsse);

  //Individua lo spike
  bool isScanInteresting = false;
  double currCm(0);
  while ( not(isScanInteresting) ) {
    double prevCm = currCm;
    currCm = getDistanceCm(SDFRONT, distStableCount);
    double diffCm = abs(prevCm - currCm);

    bool daLontanoAVicino = prevCm > currCm + 1.0;
    bool isSpike = (diffCm >= sizePallinaCm);
    bool nellaStanza = (currCm < dimDiag);
    isScanInteresting = (isSpike and daLontanoAVicino and nellaStanza); 
  }

  motoriFerma();

  //Ritorna l'ultima distanza
  distCm = currCm;

}

//Sto puntando l'oggetto. Lo raggiungo.
void evacRaggiungiOggetto( double oggDistCm, SGVERSO & dirScan, bool & dirScanDetected ) {
  
  //Il verso di rotazione deve essere determinato solo una volta in questa funzione.
  dirScanDetected = false;
  dirScan = SGANTIOR;

  double scanDistCurrCm = oggDistCm;
  double scanMinCm = oggDistCm;

  bool isAgganciato = true;
  
  while ( scanDistCurrCm >= distFinaleCm ) {

    //Avanza finchè la distanza si riduce
    avanza(evacMoveVel);
    while ( isAgganciato and (scanDistCurrCm > distFinaleCm) ) {
      scanDistCurrCm = getDistanceCm(SDFRONT, distStableCount);

      if ( scanDistCurrCm <= scanMinCm + 0.5 ) {
        scanMinCm = min( scanMinCm, scanDistCurrCm );
      } else {
        isAgganciato = false;
      }
    }
    motoriFerma();

    //Qui sono sganciato oppure ho raggiunto l'oggetto
    //Se ho rggiunto l'oggetto esco dal ciclo principale
    if ( scanDistCurrCm <= distFinaleCm ) {
      break;
    }

    //Qui sono sganciato dall'oggetto. Lo riaggancio, scansionando un'area di pochi gradi a destra e a sinistra.
    
    //Devo determinare il verso di rotazione da usare per riagganciare l'oggetto.
    //Il verso di rotazione va determinato solo una volta e si userà sempre lo stesso per riagganciare l'oggetto corrente
    if (not(dirScanDetected)) {
      dirScan = evacDetectScanDirection(scanMinCm);
      dirScanDetected = true;
    }

    //Gira nella direzione individuata, finchè non riaggancio l'oggetto
    gira(dirScan, scanVel, ruotaSuAsse);
    while ( not(isAgganciato) ) {
      scanDistCurrCm = getDistanceCm(SDFRONT, distStableCount);
      isAgganciato = (scanDistCurrCm <= scanMinCm + 0.5 );
    }
    motoriFerma();

    //Una volta riagganciato, giro di ulteriori 5 gradi per centrare meglio l'oggetto
    double angolo = ( dirScan == SGANTIOR ) ? -5 : 5;
    ruotaAsse( angolo, true );

  }
}

//Determina il verso di rotazione da usare per riagganciare l'oggetto.
//Il verso di rotazione va determinato solo una volta e si userà sempre lo stesso per riagganciare l'oggetto
SGVERSO evacDetectScanDirection( double scanMinCm ) {

  SGVERSO dirScan;

  mpu6050.update();

  //Ruota come un radar, in senso antiorario per 10 gradi
  const double angleLimit = 10.0;
  gira(SGANTIOR, scanVel, ruotaSuAsse);
  double cTurnAngle = mpu6050.getAngleZ();
  bool trovato = false;
  while ( not(trovato) and abs( cTurnAngle ) <= angleLimit ) {
    cTurnAngle = mpu6050.getAngleZ();
    double tempDist = getDistanceCm(SDFRONT, distStableCount);
    if ( tempDist <= scanMinCm + 0.5 ) {
      trovato = true;
    }      
  }

  motoriFerma(); 

  //Rimettiti in posizione, prima di questa scansione
  //Ruota In senso orario di N gradi per compensare la rotazione antioraria usata durante la scansione per riagganciare l'oggetto
  ruotaAsse( abs(cTurnAngle), true );

  dirScan = trovato ? SGANTIOR : SGORARIO ;

  return dirScan;

}


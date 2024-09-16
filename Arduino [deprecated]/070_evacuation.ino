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
const double dimRoomDiag = sqrt( dimRoom1*dimRoom1 + dimRoom2*dimRoom2);


//Dimensioni Evacuation points
const double dimEvacPoint = 30;
const double dimEvacPointAltezza = sqrt( dimEvacPoint*dimEvacPoint + dimEvacPoint*dimEvacPoint) / 2.0;

//Dimensione robot
const double dimRobDistLat = 7; //Distanza dal centro al sensore laterale
const double dimRobDistFront = 10; //Distanza dal centro al sensore frontale
const double dimRobDistDelta = dimRobDistFront - dimRobDistLat; //Delta da aggiungere alla distanza laterale per ottenere la frontale, dopo la rotazione

//Confronto a meno di un errore
inline bool simile( const double & a, const double & b, const double errore = 0.5 ) {
  return ( abs(a - b) <= errore );
}

//Ritorna la dimensione calcolata dai due sensori laterali.
inline double evacGetRoomSize() {
  double currLCm = getDistanceCm(SDLEFT, distStableCount);
  double currRCm = getDistanceCm(SDRIGHT, distStableCount);
  double totCm = currLCm + currRCm + dimRobDistLat*2;
  return totCm;
}


//Scegli automaticamente se posso usare avanzaFronteCm oppure devo ricorrere a avanzaRetroCm
inline void avanzaAutoCm(double cm) {
  Serial.println(String("") + __func__ );
  Serial.println(String("") + "cm: " + cm );

  double currCm = getDistanceCm(SDFRONT, distStableCount);
  if ( cm <= currCm ) {
    avanzaFronteCm(cm);
  } else {
    avanzaRetromCm(cm);
  }

  Serial.println(String("") + __func__ + " END ");
}

//Avanza di cm (sfrutta il sensore di distanza)
//Avanzo procedendo frontalmente, per sfruttare in avvicinamento il sensore frontale
//Attenzione! Se cm > distanza dall'oggetto più vicino al frontale ==> usa avanzaRetroCm
inline void avanzaFronteCm( double cm ) {
  Serial.println(String("") + __func__ );
  Serial.println(String("") + "cm: " + cm );

  double distStartCm = getDistanceCm(SDFRONT, distStableCount);
  double currDistCm = distStartCm;
  avanza(evacMoveVel);
  while (  distStartCm - currDistCm <= cm ) {
    currDistCm = getDistanceCm(SDFRONT, distStableCount);
  }
  motoriFerma();

  Serial.println(String("") + __func__ + " END ");
}

//Avanza in retromarcia di cm (sfrutta il sensore di distanza)
//Avanzo procedendo in retromarcia, per sfruttare in allontanamento il sensore frontale
//Mi serve quando cm > distanza dall'oggetto più vicino al frontale.
inline void avanzaRetromCm(double cm ) {
  Serial.println(String("") + __func__ );
  Serial.println(String("") + "cm: " + cm );

  ruotaAsse(180, true);
  double distStartCm = getDistanceCm(SDFRONT, distStableCount);
  double currDistCm = distStartCm;
  avanza(-evacMoveVel);
  while ( currDistCm - distStartCm <= cm ) {
    currDistCm = getDistanceCm(SDFRONT, distStableCount);
  }
  motoriFerma();
  ruotaAsse(-180, true);

  Serial.println(String("") + __func__ + " END ");
}


//FUNZIONE PRINCIPALE
void evacuation() {

  Serial.println(String("") + __func__ );

  //Sono appena entrato nella stanza
  //Solo per la prima volta, Avanza nella stanza, eventualmente spingendo le palline
  avanzaAutoCm(dimRoom1 / 2.0);

  bool ciSonoPalline = true;
  while ( ciSonoPalline ) {
    //Raggiungo il centro della stanza
    evacRaggiungiCentroStanza();

    //Dal centro stanza raggiungi la pallina.
    EV_TYPE evacuationType;
    evacTrovaERaggiungiPalla(evacuationType);

    if ( evacuationType != EV_USCITA ) {
      evacCatturaPallina();
      //Dal centro della stanza ruoto, fino a puntare gli angoli (la cui distanza è nota dal centro stanza)
      if ( evacuationType == EV_ROSSA ) {
        evacRaggiungiAngoloRosso();
      } else {
        evacRaggiungiAngoloVerde();
      }
      //Rilascio la pallina dopo aver raggiunto l'angolo
      evacRilasciaPallina();

    }

    ciSonoPalline = (evacuationType != EV_USCITA);
  }

  //Raggiungo di nuovo il centro della stanza
  evacRaggiungiCentroStanza();

  //Raggiungi l'uscita
  evacRaggiungiUscita();

  Serial.println(String("") + __func__ + " END ");

}

//Posizionati perpendicolarmente alla stanza.
//In questa posizione i sensori laterali misurano una delle due dimensioni della stanza.
//Dopo questa funzione il robot non punta verso le uscite, nè lateralmente, nè frontalmente.
void evacPosizionatiVerticalmente() {

  Serial.println(__func__);

  //Misuro la dimensione della stanza accross track
  double currRoomSizeAccrossCm = evacGetRoomSize();

  Serial.println(String("")+"currRoomSizeAccrossCm: "+currRoomSizeAccrossCm);

  //Faccio un giro di più di 360 gradi finchè non sono perpendicolare alla stanza
  bool sonoInPosizione=false;
  while ( not(sonoInPosizione) ) {
  
    Serial.println(String("")+"Faccio un giro di più di 360 gradi finchè non sono perpendicolare alla stanza");

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
    Serial.println(String("")+"sonoPerpendicolareLateralmente: " + sonoPerpendicolareLateralmente);
    Serial.println(String("")+"sonoPerpendicolareFrontalmente: " + sonoPerpendicolareFrontalmente);
    Serial.println(String("")+"sonoInPosizione: " + sonoInPosizione);
    if ( sonoInPosizione ) break;

    //Non ho trovato la posizione ottimale.
    //Mi sposto di 10 centimetri lungo la direzione con più spazio e ripeto la ricerca.
    Serial.println(String("")+"Non ho trovato la posizione ottimale. Mi sposto di 10 centimetri lungo la direzione con più spazio e ripeto la ricerca.");
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
    avanzaAutoCm( distCm / 3.0 );

  }

  Serial.println(String("") + "Sono perpendicolare alla stanza");
  Serial.println(String("") + __func__ + " END ");

}

//Raggiunge il centro della stanza
// L'asse Nord-Sud sarà allineato con la dimensione corta.
// L'asse Laterale sarà allineato con la dimensione lunga.
void evacRaggiungiCentroStanza() {

  Serial.println(String("") + __func__ );

  //Posizionati verticalmente nella stanza
  //Qui sono allineato sugli assi rispetto alla stanza E non punto alle uscite, nè lateralmente, nè frontalmente.
  evacPosizionatiVerticalmente();

  double err=2.0;

  //Mi posiziono in modo da avere l'asse nord-sud allineato al lato più corto
  double roomSizeAccrossCm = evacGetRoomSize();
  if ( simile(roomSizeAccrossCm, dimRoom1, err) ) {
    ruotaAsse( 90, true );  
  }

  Serial.println(String("") + "L'asse nord-sud è allineato al lato più corto");

  //Calcola le distanze dal centro del robot ai muri
  double distLeftCm  = getDistanceCm(SDLEFT , distStableCount) + dimRobDistLat;
  double distRightCm = getDistanceCm(SDRIGHT, distStableCount) + dimRobDistLat;
  ruotaAsse( 90, true );
  double distNordCm = getDistanceCm(SDLEFT , distStableCount) + dimRobDistDelta;
  double distSudCm  = getDistanceCm(SDRIGHT, distStableCount) + dimRobDistDelta;
  ruotaAsse( -90, true );

  Serial.println(String("") + "Compenso le distanze per raggiungere il centro");
  Serial.println(String("") + "distLeftCm: " + distLeftCm);
  Serial.println(String("") + "distRightCm: " + distRightCm);
  Serial.println(String("") + "distNordCm: " + distNordCm);
  Serial.println(String("") + "distSudCm: " + distSudCm);

  //Mi accentro lateralmente. Left-Right è allineato con la dimensione della stanza più lunga
  Serial.println(String("") + "Mi accentro lateralmente. Left-Right è allineato con la dimensione della stanza più lunga");
  if ( not(simile(distLeftCm, distRightCm, err)) ) {
    //Calcolo la distanza dal centro
    if ( distLeftCm > distRightCm ) {
      //Devo andare verso sinistra
      double gapCm = distLeftCm - (dimRoom2 / 2.0);
      ruotaAsse( -90, true ); 
      //Avanza, spingi pure le palline
      avanzaAutoCm(gapCm);
      //Mi riposiziono per riallineare left-right con la dimensione più lunga
      ruotaAsse(  90, true );
    } else {
      //Devo andare verso destra
      double gapCm = distRightCm - (dimRoom2 / 2.0);
      ruotaAsse(  90, true ); 
      avanzaAutoCm(gapCm);
      ruotaAsse( -90, true );
    }
  }

  //Mi accentro frontalmente. Nord-Sud è allineato con la dimensione della stanza più corta
  Serial.println(String("") + "Mi accentro frontalmente. Nord-Sud è allineato con la dimensione della stanza più corta");
  if ( not(simile(distNordCm, distSudCm, err)) ) {
    //Calcolo la distanza dal centro
    if ( distNordCm > distSudCm ) {
      //Devo andare verso nord
      double gapCm = distNordCm - (dimRoom2 / 2.0);
      avanzaAutoCm(gapCm); 
    } else {
      //Devo andare verso sud
      double gapCm = distSudCm - (dimRoom2 / 2.0);
      ruotaAsse(  180, true ); 
      avanzaAutoCm(gapCm);
      ruotaAsse( -180, true );
    }
  }
  motoriFerma();

  Serial.println(String("") + "Sono al centro della stanza. Nord-sud allineato su dim corta. Asse laterale allineato su dim lunga.");
  Serial.println(String("") + __func__ + " END ");

}

//Dal centro della stanza raggiungi l'uscita.
//Qui dovrei avere tutte le palline delle evacuation zone
void evacRaggiungiUscita() {
  Serial.println(String("") + __func__ );
  //@@@ DA SCRIVERE
  Serial.println(String("") + __func__ + " END ");
}

//Dal centro della stanza ruoto, fino a puntare un angolo (la cui distanza è nota dal centro stanza)
//e lo raggiungo
void evacRaggiungiAngolo() {
  Serial.println(String("") + __func__ );
  //@@@ DA SCRIVERE
  Serial.println(String("") + __func__ + " END ");
}

//Raggiunge l'angolo verde
void evacRaggiungiAngoloVerde() {
  Serial.println(String("") + __func__ );

  evacRaggiungiAngolo();
  //@@@ DA SCRIVERE
  Serial.println(String("") + __func__ + " END ");
}

//Raggiunge l'angolo rosso
void evacRaggiungiAngoloRosso() {
  Serial.println(String("") + __func__ );

  evacRaggiungiAngolo();
  //@@@ DA SCRIVERE
  Serial.println(String("") + __func__ + " END ");
}


//L'oggetto raggiunto è una pallina
//Restituisce vero se abbiamo raggiunto una pallina
//Restituisce evacuationType: il colore della evacuation zone in cui portare la pallina
bool evacIsPallina( EV_TYPE & evacuationType ) {
  Serial.println(String("") + __func__ );
  //@@@ DA SCRIVERE
  //RESTITUISCI FALSE SE LEGGI UNA LINEA DI ENTRATA O USCITA
  Serial.println(String("") + __func__ + " END ");
  return true;
}

//Cattura la pallina
void evacCatturaPallina() {
  Serial.println(String("") + __func__ );
  //@@@ DA SCRIVERE
  Serial.println(String("") + __func__ + " END ");
}

//Rilascia la pallina
void evacRilasciaPallina() {
  Serial.println(String("") + __func__ );
  //@@@ DA SCRIVERE
  Serial.println(String("") + __func__ + " END ");
}

//Questa funzione va chiamata dal centro stanza!
//Trova una palla nella stanza e la raggiunge
//Restituisce evacuationType: il colore della evacuation zone in cui portare la pallina oppure uscita (non ci sono palline)
bool dirScanDetected = false;
void evacTrovaERaggiungiPalla( EV_TYPE & evacuationType ) {

  Serial.println(String("") + __func__ );

  bool isPallina = false;
  while ( not(isPallina) ) {
    //Radar, ruota fino a individuare un oggetto da raggiungere
    Serial.print("evacIndividuaSpike begin");
    double oggDistCm(0); //la distanza dall'oggetto che mi ha determinato lo spike (che ho agganciato)
    bool trovato = evacIndividuaSpike(oggDistCm);

    Serial.println(String("evacIndividuaSpike end. oggDistCm: ") + oggDistCm + "; trovato: "+trovato);

    if ( not(trovato) ) {
      evacuationType = EV_USCITA;
      return;
    }

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

  Serial.println(String("") + __func__ + " END ");

}

//Raggiunto l'oggetto, ruoto il robot per centrare al meglio l'oggetto.
// Ruoto finchè non raggiungo la distanza minima.
void evacCentratiRispettoAlloggetto(SGVERSO dirScan ) {

  Serial.println(String("") + __func__ );

    double currCm = getDistanceCm(SDFRONT, distStableCount);
    double scanMinCm = currCm;

    gira(dirScan, scanVel, ruotaSuAsse);

    bool minimoMigliorato = true;
    while ( minimoMigliorato ) {
      currCm = getDistanceCm(SDFRONT, distStableCount);
      minimoMigliorato = ( currCm <= scanMinCm );
    }
    motoriFerma();

  Serial.println(String("") + __func__ + " END ");

}

//Gira in senso antioratio, come un radar, per individuare uno spike nella distanza
//Continua a ruotare finche le misurazioni successive sono "smooth", cioè finchè osservi un muro
//Fermati quando hai individuato uno spike: potenzialmente un oggetto da prendere.
//Note:
// - se si parte osservando già l'oggetto, la scansione prenderà il prossimo oggetto o lo stesso dopo una rotazione di 360 gradi.
// - LA SCANSIONE DEVE ESSERE FATTA PARTENDO DAL CENTRO STANZA, PER TROVARE SOLO PALLINE E NON GLI SPIGOLI DELLE ENTRATE / USCITE!
// - SE ENTRATA E USCITA NON SONO NEGLI ANGOLI, POTREBBE PRENDERE COME SPIKE L'ANGOLO DEL MURO DI UNA ENTRATA O UNA USCITA
bool evacIndividuaSpike( double & distCm ) {
  
  Serial.println(String("") + __func__ );

  //Ruota come un radar, in senso antiorario
  gira(SGANTIOR, scanVel, ruotaSuAsse);

  //Individua lo spike. Fa due giri su se stesso. Se non trova nulla restituisce false.
  mpu6050.update();
  double cTurnAngle = 0.0;

  bool isScanInteresting = false;
  double currCm(0);
  while ( not(isScanInteresting) and abs( cTurnAngle ) <= 360.0*2 ) {
    double prevCm = currCm;
    currCm = getDistanceCm(SDFRONT, distStableCount);
    double diffCm = abs(prevCm - currCm);

    cTurnAngle = mpu6050.getAngleZ();

    bool daLontanoAVicino = prevCm > currCm + 1.0;
    bool isSpike = (diffCm >= sizePallinaCm);
    bool nellaStanza = (currCm < (dimRoomDiag/2.0 - dimEvacPointAltezza) );
    isScanInteresting = (isSpike and daLontanoAVicino and nellaStanza); 
  }

  motoriFerma();

  //Ritorna l'ultima distanza
  distCm = currCm;

  Serial.println(String("") + __func__ + " END ");

  return isScanInteresting;
}

//Sto puntando l'oggetto. Lo raggiungo.
void evacRaggiungiOggetto( double oggDistCm, SGVERSO & dirScan, bool & dirScanDetected ) {
  
  Serial.println(String("") + __func__ );

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

  Serial.println(String("") + __func__ + " END ");
}

//Determina il verso di rotazione da usare per riagganciare l'oggetto.
//Il verso di rotazione va determinato solo una volta e si userà sempre lo stesso per riagganciare l'oggetto
SGVERSO evacDetectScanDirection( double scanMinCm ) {

  Serial.println(String("") + __func__ );

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

  Serial.println(String("") + __func__ + " END ");

  return dirScan;

}


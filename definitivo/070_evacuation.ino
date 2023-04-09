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


//Trova una palla nella stanza e la raggiunge
void trovaERaggiungiPalla() {

  //Radar, ruota fino a individuare un oggetto da raggiungere
  double oggDistCm(0); //la distanza dall'oggetto che mi ha determinato lo spike (che ho agganciato)
  evacIndividuaSpike(oggDistCm);

  //Tieni agganciato l'oggetto ed avvicinati
  bool dirScanDetected = false;
  SGVERSO dirScan;
  evacRaggiungiOggetto(oggDistCm, dirScan, dirScanDetected);

  //Raggiunto l'oggetto ad una distanza di distFinaleCm
  //Ruoto il robot per centrare meglio l'oggetto
  if ( dirScanDetected ) {
    centratiRispettoAlloggetto( dirScan );
  }

  //@@@ QUI BISOGNA LEGGERE IL COLORE DELLA PALLINA USANDO IL SENSORE DI COLORE FRONTALE
  bool isPallina = true;

  //Ruoto su me stesso in modo da posizionare la gabbia per catturare la pallina
  if (isPallina) {
    ruotaAsse( 180, true );
  }

}

//Raggiunto l'oggetto, ruoto il robot per centrare al meglio l'oggetto
void centratiRispettoAlloggetto(SGVERSO dirScan ) {
    
    gira(dirScan, scanVel, ruotaSuAsse);

    double currCm = getDistanceCm(SDFRONT, distStableCount);
    double scanMinCm = currCm;
    bool isAgganciato = false;
    while ( not isAgganciato ) {
      currCm = getDistanceCm(SDFRONT, distStableCount);
      if ( scanMinCm > scanMinCm ) {
        isAgganciato = true;
      } else {
        scanMinCm = currCm;        
      }
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

    bool daLontanoAVicino = prevCm > currCm;
    bool isSpike = (diffCm >= sizePallinaCm);
    isScanInteresting = (isSpike and daLontanoAVicino); 
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
    while ( isAgganciato and (scanDistCurrCm >= distFinaleCm) ) {
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
    if ( scanDistCurrCm >= distFinaleCm ) {
      break;
    }

    //Qui sono sganciato dall'oggetto. Lo riaggancio, scansionando un'area di pochi gradi a destra e a sinistra.
    
    //Devo determinare il verso di rotazione da usare per riagganciare l'oggetto.
    //Il verso di rotazione va determinato solo una volta e si userà sempre lo stesso per riagganciare l'oggetto
    if (not(dirScanDetected)) {
      dirScan = detectScanDirection(scanMinCm);
      dirScanDetected = true;
    }

    //Gira nella direzione individuata, finchè non riaggancio l'oggetto
    gira(dirScan, scanVel, ruotaSuAsse);
    while ( not(isAgganciato) ) {
      scanDistCurrCm = getDistanceCm(SDFRONT, distStableCount);
      isAgganciato = (scanDistCurrCm <= scanMinCm + 0.5 );
    }

    //Una volta riagganciato, giro di ulteriori 5 gradi per centrare meglio l'oggetto
    double angolo = ( dirScan == SGANTIOR ) ? -5 : 5;
    ruotaAsse( angolo, true );

    motoriFerma();

  }
}

//Determina il verso di rotazione da usare per riagganciare l'oggetto.
//Il verso di rotazione va determinato solo una volta e si userà sempre lo stesso per riagganciare l'oggetto
SGVERSO detectScanDirection( double scanMinCm ) {

  SGVERSO dirScan;

  mpu6050.update();

  //Ruota come un radar, in senso antiorario
  gira(SGANTIOR, scanVel, ruotaSuAsse);
  double cTurnAngle = mpu6050.getAngleZ();
  bool trovato = false;
  while ( not(trovato) and abs( cTurnAngle ) <= 10 ) {
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


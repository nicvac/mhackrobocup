
#include "definizioni.h"
//@@@ MODIFICARE IL CODICE PRINCIPALE PER USARE QUESTA FUNZIONE SEMPLICE

//Ritorna un valore quando viene letto consecutivamente per stableCount volte. 
// error: errore permesso fra le letture
inline double getDistanceCm( SDTYPE sdtype, int stableCount = 1, double error = 0.5 ) {
  int count = 0;
  double distCurr0);
  double distPrev(0);

  do {
    distPrev = distCurr;
    distCurr = getUltrasonicDistanceCm( sdtype );

    if ( abs( distPrev - distCurr ) <= error ) {
      ++count;
    } else {
      count = 0;
    }
  } while ( count < stableCount );

  return distCurr;
}

//Lettura della distanza
inline double getUltrasonicDistanceCm( SDTYPE sdtype ) {

  //SDFRONT
  int triggerPort = triggerPort1;
  int echoPort    = echoPort1;
  
  //LEFT OR RIGHT
  if        ( sdtype == SDRIGHT ) { triggerPort = triggerPort2; echoPort = echoPort2;
  } else if ( sdtype == SDLEFT  ) { triggerPort = triggerPort3; echoPort = echoPort3;
  }

  return getUltrasonicDistanceCm(triggerPort, echoPort);
}

inline double getUltrasonicDistanceCm(int trigger, int echo)
{
  digitalWrite(trigger, LOW);
  delay(5);
  digitalWrite(trigger, HIGH);
  delay(10);
  digitalWrite(trigger, LOW);
  double distanza = pulseIn(echo, HIGH) * 0.03432 / 2.0;
  return distanza;
}


//@@@ Restituisce int - da eliminare quando definitivo.ino userà la funzione semplice
inline int _getUltrasonicDistance(int trigger, int echo)
{
  double distanza = getUltrasonicDistanceCm(trigger, echo);
  return distanza; //ritorna intero
}

inline void aggira_ostacolo() {
  int direzione = -1;
  if ( _getUltrasonicDistance(triggerPort2, echoPort2) > _getUltrasonicDistance(triggerPort3, echoPort3)) {
    direzione = 1;
  }
  ruotaAsse(direzione * 90);
  float dist_min = avanza_superando_ostacolo(direzione); //qui
  circum(dist_min, -direzione);
  /*
    ruotaAsse(direzione * 90 * -1);
    avanza_superando_ostacolo_con_controllo(direzione);
    if (controllo()) {
    ruotaAsse_con_controllo(direzione * 90 * -1);
    if (controllo()) avanza_superando_ostacolo_con_controllo(direzione);
    }*/
}

inline bool isAgganciato(float d_min, int triggerPort, int echoPort ) {
    const float distDelta = 6;
    auto distLat = _getUltrasonicDistance(triggerPort, echoPort);
    bool agganciato = d_min - distDelta <= distLat && distLat <= d_min + distDelta;
    return agganciato;  
}

void circum(float d_min, int direzione) {
  //@@@ Migliorare il codice - fare una funzione che restituisce echo e trigger corretti a seconda di direzione.
  int echoPort = (direzione != 1) ? echoPort3 : echoPort2 ;
  int triggerPort = ( echoPort == echoPort2 ) ? triggerPort2 : triggerPort3 ;
  while (true) {

    //@@@ if (controllo() != 0) return;

    bool agganciato = isAgganciato( d_min, triggerPort, echoPort );
    if ( agganciato ) {
      avanza(speed_circum);       
    } else {
      const float gradi = direzione * 1;
      ruotaAsse(gradi , false);
    }
  }
}

inline float avanza_superando_ostacolo( int direzione ) {

  int echoPort = (direzione == 1) ? echoPort3 : echoPort2 ;
  int triggerPort = ( echoPort == echoPort2 ) ? triggerPort2 : triggerPort3 ;

  int distanza_min = 0;

  do {
    distanza_min = _getUltrasonicDistance(triggerPort, echoPort);
  } while (distanza_min < 2);

  avanza(speed_circum);
  bool superato = false;
  int distanza_corr = 0;
  do {
    do {
      distanza_corr = _getUltrasonicDistance(triggerPort, echoPort);
    } while (distanza_corr < 2);

    distanza_min = min(distanza_min, distanza_corr );
    superato = (distanza_min <= 10) && distanza_corr > distanza_min + 10;
  } while (!superato);
  motoriFerma();
  return distanza_min;
}
/*
inline void avanza_superando_ostacolo_con_controllo ( int direzione ) {

  int echoPort = (direzione == 1) ? echoPort3 : echoPort2 ;
  int triggerPort = ( echoPort == echoPort2 ) ? triggerPort2 : triggerPort3 ;

  int distanza_min = _getUltrasonicDistance(triggerPort, echoPort);
  do {
    if (!controllo()) break;
    int distanza_corr = _getUltrasonicDistance(triggerPort, echoPort);
    distanza_min = min(distanza_min, distanza_corr );
    avanza(200);
    superato = (distanza_min <= 10) && distanza_corr > distanza_min + 10;
  } while (!superato);
  stop();
}
*/


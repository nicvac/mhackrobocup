#include <MPU6050_tockn.h>
#include <Wire.h>
#include <QTRSensors.h>

unsigned long r, g, b;
unsigned long r2, g2, b2;
unsigned long int t1, t2 = 0;
unsigned long int inv1, inv2 = 0;
int16_t ultimoErrore = 0;

const uint8_t maxspeed = 240;
const uint8_t speed_circum = maxspeed * 0.7;
const uint8_t speedturn    = maxspeed * 1.0;

float PID;

const float KP = 0.083, KD = 2;  //0.083 2

int16_t lSpeed, rSpeed;

const int STBY = 4;


const int PWMA = 3;
const int AIN1 = 9;
const int AIN2 = 8;


const int PWMB = 5;
const int BIN1 = 7;
const int BIN2 = 6;


const int out = 28;
const int s0 = 29;
const int s1 = 30;
const int s2 = 31;
const int s3 = 32;

//Sensor 2 Left
const int out_2 = 33;
const int s0_2 = 34;
const int s1_2 = 35;
const int s2_2 = 36;
const int s3_2 = 37;


QTRSensors qtr;

const uint8_t SensorCount = 8;
uint16_t sensorValues[SensorCount];

MPU6050 mpu6050(Wire);

float x, y, z;

const int triggerPort1 = 38;
const int echoPort1 = 39;
const int alimUltra1 = 40;

const int alimGiroscopio = 41;

const int triggerPort2 = 42;
const int echoPort2 = 43;
const int alimUltra2 = 44;

const int triggerPort3 = 45;
const int echoPort3 = 46;
const int alimUltra3 = 47;

unsigned long cont_dist_stabile = 0;

int _getUltrasonicDistance(int trigger, int echo)
{
  digitalWrite(trigger, LOW);
  delay(5);
  digitalWrite(trigger, HIGH);
  delay(10);
  digitalWrite(trigger, LOW);
  double distanza = pulseIn(echo, HIGH) * 0.03432 / 2.0;
  //Serial.println(distanza);
  return distanza;
}

long long int t_start;

void setup() {
  Serial.begin(115200);
  qtr.setTypeRC();
  qtr.setSensorPins((const uint8_t[]) {
    11, 12, 27, 22, 23, 24, 25, 26
  }, SensorCount);
  qtr.setEmitterPin(2);

  for (int i = 0; i < 250; i++)  // make the calibration take about 5 seconds
  {
    qtr.calibrate();
    delay(20);
  }

  qtr.setTimeout(2000);

  pinMode(STBY, OUTPUT);

  pinMode(PWMA, OUTPUT);
  pinMode(AIN1, OUTPUT);
  pinMode(AIN2, OUTPUT);

  pinMode(PWMB, OUTPUT);
  pinMode(BIN1, OUTPUT);
  pinMode(BIN2, OUTPUT);

  pinMode(s0, OUTPUT);
  pinMode(s1, OUTPUT);
  pinMode(s2, OUTPUT);
  pinMode(s3, OUTPUT);
  pinMode(s0_2, OUTPUT);
  pinMode(s1_2, OUTPUT);
  pinMode(s2_2, OUTPUT);
  pinMode(s3_2, OUTPUT);
  pinMode(out, INPUT);
  pinMode(out_2, INPUT);

  digitalWrite(s0, HIGH);
  digitalWrite(s1, HIGH);
  digitalWrite(s0_2, HIGH);
  digitalWrite(s1_2, HIGH);

  Wire.begin();
  pinMode(alimGiroscopio, OUTPUT);
  digitalWrite(alimGiroscopio, HIGH);
  mpu6050.begin();
  mpu6050.calcGyroOffsets(true);

  pinMode(triggerPort1, OUTPUT);
  pinMode(echoPort1, INPUT);
  pinMode(alimUltra1, OUTPUT);

  pinMode(triggerPort2, OUTPUT);
  pinMode(echoPort2, INPUT);
  pinMode(alimUltra2, OUTPUT);

  pinMode(triggerPort3, OUTPUT);
  pinMode(echoPort3, INPUT);
  pinMode(alimUltra3, OUTPUT);


  t_start=millis();
  digitalWrite(alimUltra1, HIGH);
  digitalWrite(alimUltra2, HIGH);
  digitalWrite(alimUltra3, HIGH);
}

void loop() {
  t1 = millis();

  //if(millis()-t_start<100)avanza(maxspeed*0.8);
  
  uint16_t posizione = qtr.readLineBlack(sensorValues);

  if (posizione > 6700) {
    move(1, speedturn, 0);
    move(2, speedturn, 1);
    return;
  }
  if (posizione < 300) {
    move(1, speedturn, 1);
    move(2, speedturn, 0);
    return;
  }

  int16_t errore = posizione - 3500;

  PID = (errore * KP) + ((errore - ultimoErrore) * KD);
  ultimoErrore = errore;

  lSpeed = maxspeed + PID;
  rSpeed = maxspeed - PID;

  if (lSpeed > maxspeed) {
    lSpeed = maxspeed;
  }
  if (lSpeed < 0) {
    lSpeed = 0;
  }
  if (rSpeed > maxspeed) {
    rSpeed = maxspeed;
  }
  if (rSpeed < 0) {
    rSpeed = 0;
  }
/*
  if (controllo()) {
    stop();
    //avanza(180);
    //delay(70);
    //stop();
    delay(2000);
    digitalWrite(s2, LOW);
    digitalWrite(s3, LOW);
    r = pulseIn(out, LOW);
    //Red 2
    digitalWrite(s2_2, LOW);
    digitalWrite(s3_2, LOW);
    r2 = pulseIn(out_2, LOW);
    //Blue 1
    digitalWrite(s2, LOW);
    digitalWrite(s3, HIGH);
    b = pulseIn(out, LOW);
    //Blue 2
    digitalWrite(s2_2, LOW);
    digitalWrite(s3_2, HIGH);
    b2 = pulseIn(out_2, LOW);

    //Green 1
    digitalWrite(s2, HIGH);
    digitalWrite(s3, HIGH);
    g = pulseIn(out, LOW);

    //Green 2
    digitalWrite(s2_2, HIGH);
    digitalWrite(s3_2, HIGH);
    g2 = pulseIn(out_2, LOW);

    if (r >= 9 && g >= 9 && b >= 9 && r2 >= 9 && g2 >= 9 && b2 >= 9) {
      avanza(230);
      delay(200);
      ruotaAsse(180);
    } else if (r >= 9 && g >= 9 && b >= 9) {
      avanza(230);
      delay(200);
      ruotaAsse(-90);
    } else if (r2 >= 9 && g2 >= 9 && b2 >= 9) {
      avanza(230);
      delay(200);
      ruotaAsse(90);
    }
  }*/

  //Il PID ha bisogno di tempo per stabilizzarsi.
  //Ignora il risultato del PID per i primi X ms.
  if(millis()-t_start<100) {
    lSpeed=maxspeed;
    rSpeed=maxspeed;
  }

  move(1, lSpeed, 0);
  move(2, rSpeed, 0);

  int distanza = _getUltrasonicDistance(triggerPort1, echoPort1);

  if (  3 <= distanza && distanza <= 7  ) {
    ++cont_dist_stabile;
  } else {
    cont_dist_stabile = 0;
  }
  
  if (cont_dist_stabile >= 3 ) {
    aggira_ostacolo(); //prima lettura 0 (percui maggioe 3)
  }
}

const int potenzaGiraOrario = 230;

inline void giraOrario(bool su_asse=true) {
  int potenzaM2 = potenzaGiraOrario;
  int potenzaM1 = su_asse? potenzaM2 : 0;

  move(1, potenzaM1, 1);
  move(2, potenzaM2, 0);
}

inline void giraAntiorario(bool su_asse=true) {
  int potenzaM1 = potenzaGiraOrario;
  int potenzaM2 = su_asse? potenzaM1 : 0;

  move(1, potenzaM1, 0);
  move(2, potenzaM2, 1);  
}


void ruotaAsse(float gradi, bool su_asse=true ) {

  if (gradi == 0) return;
  float gradiEn = gradi2Eng(abs(gradi));
  mpu6050.update();
  float valIniziale = mpu6050.getAngleZ();
  do {
    mpu6050.update();
    if (gradi > 0) {
      giraOrario(su_asse);
    } else {
      giraAntiorario(su_asse);
    }
    //Serial.println(abs(valIniziale - mpu6050.getAngleZ()));

  } while (abs(valIniziale - mpu6050.getAngleZ()) < gradiEn);

  move(1, 0, 0);
  move(2, 0, 1);
}

/*
void ruotaAsse_con_controllo(float gradi) {

  if (gradi == 0) {
    return ;
  }
  float gradiEn = gradi2Eng(abs(gradi));
  mpu6050.update();
  float valIniziale = mpu6050.getAngleZ();
  do {
    if (!controllo()) break;
    mpu6050.update();
    if (gradi > 0) {
      giraOrario();
    } else {
      giraAntiorario();
    }
    //Serial.println(abs(valIniziale - mpu6050.getAngleZ()));

  } while (abs(valIniziale - mpu6050.getAngleZ()) < gradiEn);

  move(1, 0, 0);
  move(2, 0, 1);
}
*/

inline void aggira_ostacolo() {
  int direzione = -1;
  if ( _getUltrasonicDistance(triggerPort2, echoPort2) > _getUltrasonicDistance(triggerPort3, echoPort3)) {
    direzione = 1;
  }
  ruotaAsse(direzione * 90);
  float dist_min = avanza_superando_ostacolo(direzione); //qui
  circum_(dist_min, -direzione);
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

void circum_(float d_min, int direzione) {
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
inline void avanza(int v) {
  move(1, v, 0);
  move(2, v, 0);
}

inline void motoriFerma() {
  move(1, 0, 0);
  move(2, 0, 0);
}



inline float gradi2Eng(float gradiCent) {
  return gradiCent * 160.0 / 90.0;
}

inline float Eng2Gradi(float gradiEng) {
  return gradiEng * 90.0 / 160.0;
}


inline bool controllo() {
  for (int i = 0; i < SensorCount; i++) {
    if (sensorValues[i] < 500) return false;
  }
  return true;
}

void move(int motor, int speed, int direction) {

  digitalWrite(STBY, HIGH);

  boolean inPin1 = LOW;
  boolean inPin2 = HIGH;

  if (direction == 1) {
    inPin1 = HIGH;
    inPin2 = LOW;
  }

  if (motor == 1) {
    digitalWrite(AIN1, inPin1);
    digitalWrite(AIN2, inPin2);
    analogWrite(PWMA, speed);
  } else {
    digitalWrite(BIN1, inPin1);
    digitalWrite(BIN2, inPin2);
    analogWrite(PWMB, speed);
  }
}

void stop() {

  digitalWrite(STBY, LOW);
}

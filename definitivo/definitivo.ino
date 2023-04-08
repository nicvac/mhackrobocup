#include <MPU6050_tockn.h>
#include <Wire.h>
#include <QTRSensors.h>

#include "definizioni.h"

unsigned long r, g, b;
unsigned long r2, g2, b2;
unsigned long int t1, t2 = 0;
unsigned long int inv1, inv2 = 0;
int16_t ultimoErrore = 0;

float PID;

int16_t lSpeed, rSpeed;

QTRSensors qtr;

const uint8_t SensorCount = 8;
uint16_t sensorValues[SensorCount];

MPU6050 mpu6050(Wire);

float x, y, z;

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

inline bool controllo() {
  for (int i = 0; i < SensorCount; i++) {
    if (sensorValues[i] < 500) return false;
  }
  return true;
}

void calibra(){

  mpu6050.update();
  float valIniziale = mpu6050.getAngleZ();
  
  bool sinistra = false;
  bool destra = true;
  int gradi = gradi2Eng(40);

  for(int i = 0; i < 7; i+=0){

      mpu6050.update();

      if(abs(valIniziale - mpu6050.getAngleZ()) > gradi){
        valIniziale = mpu6050.getAngleZ();
        sinistra = !sinistra;
        destra = !destra;
        gradi = gradi2Eng(80);
        i++;
      }

      if(i == 6) gradi = gradi2Eng(40);

      move(1, 240, sinistra);
      move(2, 240, destra);

      qtr.calibrate();
      delay(20);
  }
  
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

  //calibra();

  t_start=millis();
  digitalWrite(alimUltra1, HIGH);
  digitalWrite(alimUltra2, HIGH);
  digitalWrite(alimUltra3, HIGH);
}

void loop() {
  t1 = millis();
  
  uint16_t posizione = qtr.readLineBlack(sensorValues);

  if (posizione > 6200) {
    move(1, speedturn, 0);
    move(2, speedturn, 1);
    return;
  }
  if (posizione < 800) {
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

  //Controllo della distanza su valori stabili. Ci sono degli spike che in questo modo ignoriamo
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


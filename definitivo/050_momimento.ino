//Giroscopio Engineering - gradi
inline float gradi2Eng(float gradiCent) {
  return gradiCent * 160.0 / 90.0;
}

inline float Eng2Gradi(float gradiEng) {
  return gradiEng * 90.0 / 160.0;
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


//Motori
inline void avanza(int v) {
  move(1, v, 0);
  move(2, v, 0);
}

inline void motoriFerma() {
  move(1, 0, 0);
  move(2, 0, 0);
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

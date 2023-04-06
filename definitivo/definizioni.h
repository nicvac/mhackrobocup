#pragma once

const uint8_t maxspeed = 240;
const uint8_t speed_circum = maxspeed * 0.7;
const uint8_t speedturn    = maxspeed * 1.0;

//PID
const float KP = 0.083, KD = 2;  //0.083 2

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

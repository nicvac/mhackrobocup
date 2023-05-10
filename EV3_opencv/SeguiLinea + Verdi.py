from collections import deque
import numpy as np
import cv2
import imutils
import time

posizione = 300
Pd = 0
ultimoErrore = 0

MAXSPEED = 1023

KP = 3.41
KD = 6

#Maschera verde
greenLower = (50, 200, 53) 
greenUpper = (100, 255, 255)

#Maschera nero
blackLower = (0, 0, 0)
blackUpper = (180, 255, 80)

vs = cv2.VideoCapture(1)
time.sleep(2.0)

while True:

    frame = vs.read()

    if frame[0] is None:
        break
    frame = frame[1]

    
    frame = imutils.resize(frame, width=600)
    linea = frame[220:240, 0:600]
    blurred = cv2.GaussianBlur(linea, (11, 11), 0)
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
    
    mask = cv2.inRange(hsv, blackLower, blackUpper)
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)
    
    mask2 = cv2.inRange(hsv, greenLower, greenUpper)
    mask2 = cv2.erode(mask2, None, iterations=2)
    mask2 = cv2.dilate(mask2, None, iterations=2)

    cv2.rectangle(frame,(0,220),(600,240),(0,255,0),3)

    cntsNero = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE)
    cntsNero = imutils.grab_contours(cntsNero)
    centerNero = None

    cntsVerde = cv2.findContours(mask2.copy(), cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE)
    cntsVerde = imutils.grab_contours(cntsVerde)
    centerVerde = None

    if len(cntsNero) > 0:

        c = max(cntsNero, key=cv2.contourArea)
        #((x, y), radius) = cv2.minEnclosingCircle(c)
        M = cv2.moments(c)
        centerNero = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"] + 221))
        
        cv2.circle(frame, centerNero, 5, (0, 0, 255), -1)

    if centerNero != None:
        posizione = centerNero[0]
        errore = posizione - 300
        
        Pd = (errore * KP) + ((errore - ultimoErrore) * KD)
        ultimoErrore = errore

        lSpeed = MAXSPEED + Pd
        rSpeed = MAXSPEED - Pd

        if (lSpeed > MAXSPEED):
            lSpeed = MAXSPEED
        
        if (lSpeed < 0):
            lSpeed = 0
        
        if (rSpeed > MAXSPEED): 
            rSpeed = MAXSPEED
        
        if (rSpeed < 0):
            rSpeed = 0
        
        S1 = "Errore: " + str(errore)
        S2 = "lSpeed: " + str(lSpeed)
        S3 = "rSpeed: " + str(rSpeed)

        cv2.putText(frame, S1, (5, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1, cv2.LINE_AA)
        cv2.putText(frame, S2, (5, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1, cv2.LINE_AA)
        cv2.putText(frame, S3, (5, 75), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1, cv2.LINE_AA)

    if len(cntsVerde) > 0:
        c = max(cntsVerde, key=cv2.contourArea)
        #((x, y), radius) = cv2.minEnclosingCircle(c)
        M = cv2.moments(c)
        centerVerde = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"] + 221))
        
        cv2.circle(frame, centerVerde, 5, (255, 0, 0), -1)

        if(centerVerde[0] > centerNero[0]):
            cv2.putText(frame, "Gira a destra", (5, 100), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1, cv2.LINE_AA)
        else:
            cv2.putText(frame, "Gira a sinistra", (5, 100), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1, cv2.LINE_AA)



    cv2.imshow("Mask Nero", mask)
    cv2.imshow("Mask Verde", mask2)
    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1) & 0xFF

    if key == ord("q"):
        break

vs.release()

cv2.destroyAllWindows()
from collections import deque
import numpy as np
import cv2
import imutils
import time
import serial
import threading

pacchetto = ""
pacchettoPrec = ""

def seriale():
    global pacchetto
    global pacchettoPrec
    while True:
        print(pacchetto)
        if pacchetto > 280 and pacchetto < 320:
            pass
        else:
            if(pacchetto != pacchettoPrec):
                arduino.write(pacchetto)
                pacchettoPrec = pacchetto
                time.sleep(0.1)
        
buffer = 64

send = threading.Thread(target = seriale, daemon=True)

#Maschere verde
#greenLower = (29, 86, 6)
#greenUpper = (64, 255, 255)

#Maschera giallo
#greenLower = (15, 150, 20)
#greenUpper = (35, 255, 255)

#Maschera blu
#greenLower = (100, 130, 20)
#greenUpper = (140, 255, 255)

#Maschera argento
greenLower = (190, 190, 190, 255)
greenUpper = (220, 220, 220, 255)

#Maschera nero
#greenLower = (100, 130, 20) 
#greenUpper = (140, 255, 255)

#Maschera rosso
#greenLower = (100, 130, 20)
#greenUpper = (140, 255, 255)



pts = deque(maxlen=buffer)

arduino = serial.Serial('COM8', 115200)

vs = cv2.VideoCapture(0)
time.sleep(2.0)
send.start()
while True:

    frame = vs.read()

    if frame[0] is None:
        break
    frame = frame[1]

    frame = imutils.resize(frame, width=600)
    blurred = cv2.GaussianBlur(frame, (11, 11), 0)
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
    rgba = cv2.cvtColor(blurred, cv2.COLOR_BGR2RGBA)

    mask = cv2.inRange(rgba, greenLower, greenUpper)
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)
    

    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    center = None

    if len(cnts) > 0:

        c = max(cnts, key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(c)
        M = cv2.moments(c)
        center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

        if radius > 10:
            
            cv2.circle(frame, (int(x), int(y)), int(radius),
                (0, 255, 255), 2)
            cv2.circle(frame, center, 5, (0, 0, 255), -1)
            distanza = 2237.6 * ((radius ** 2) * 3.141592653589793)**-0.603
            pacchetto = str(center[0]) + ',' + str(center[1]) +  "\n"
            pacchetto = pacchetto.encode("utf-8")
            S = "Dist: " + str(distanza)
            cv2.putText(frame, S, (5, 50), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 2, cv2.LINE_AA)



    pts.appendleft(center)

    

    for i in range(1, len(pts)):

        if pts[i - 1] is None or pts[i] is None:
            continue

        thickness = int(np.sqrt(buffer / float(i + 1)) * 2.5)
        cv2.line(frame, pts[i - 1], pts[i], (0, 0, 255), thickness)

    cv2.imshow("Mask", mask)
    cv2.imshow("rgba", rgba)
    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1) & 0xFF

    if key == ord("q"):
        break

vs.release()

cv2.destroyAllWindows()
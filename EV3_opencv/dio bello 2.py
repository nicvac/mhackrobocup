from collections import deque
import numpy as np
import cv2
import imutils
import time

pacchetto = ""
pacchettoPrec = ""

        



#Maschera verde
#greenLower = (76, 210, 160) 
#greenUpper = (100, 255, 255)

#Maschera nero
greenLower = (0, 0, 0
) 
greenUpper = (180, 255, 130)

vs = cv2.VideoCapture(0)
time.sleep(2.0)

while True:

    frame = vs.read()

    if frame[0] is None:
        break
    frame = frame[1]

    frame = imutils.resize(frame, width=600)
    blurred = cv2.GaussianBlur(frame, (11, 11), 0)
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
    rgba = cv2.cvtColor(blurred, cv2.COLOR_BGR2RGBA)

    mask = cv2.inRange(hsv, greenLower, greenUpper)
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)
    

    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    center = None

    if len(cnts) > 0:

        c = max(cnts, key=cv2.contourArea)
        #((x, y), radius) = cv2.minEnclosingCircle(c)
        M = cv2.moments(c)
        center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
        cv2.circle(frame, center, 5, (0, 0, 255), -1)
        '''
        if radius > 10:
            
            cv2.circle(frame, (int(x), int(y)), int(radius),
                (0, 255, 255), 2)
            cv2.circle(frame, center, 5, (0, 0, 255), -1)
            distanza = 2237.6 * ((radius ** 2) * 3.141592653589793)**-0.603
            pacchetto = str(center[0]) + ',' + str(center[1]) +  "\n"
            pacchetto = pacchetto.encode("utf-8")
            S = "Dist: " + str(distanza)
            cv2.putText(frame, S, (5, 50), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 2, cv2.LINE_AA)
        '''

    cv2.imshow("Mask", mask)

    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1) & 0xFF

    if key == ord("q"):
        break

vs.release()

cv2.destroyAllWindows()
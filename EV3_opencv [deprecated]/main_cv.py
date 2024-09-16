import cv2 as cv
from time import sleep

video = cv.VideoCapture(0)
sleep(2.0)

blackLowest = (95, 20, 15)
blackHighest = (143, 134, 130)

greenLower = (76, 210, 160) 
greenUpper = (100, 255, 255)

while True:
    frame = video.read()
    
    if frame[0] is None:
        break
    frame = frame[1]
    
    hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
    
    mask = cv.inRange(hsv, greenLower, greenUpper)
    mask = cv.erode(mask, None, iterations=2)
    mask = cv.dilate(mask, None, iterations=2)

    cv.imshow("Fanculo", mask)

    if cv.waitKey(1) == ord('q'):
        break


video.release()
cv.destroyAllWindows()
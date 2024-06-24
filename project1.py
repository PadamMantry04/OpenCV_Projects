import cv2
import numpy as np

frameWidth = 1024
frameHeight = 768
cap = cv2.VideoCapture(0)
cap.set(3, frameWidth)
cap.set(4, frameHeight)
cap.set(10, 150)

myColors = [[0, 100, 0, 16, 153, 255],
            [109, 20, 0, 117, 255, 255],
            [87, 36, 0, 99, 255, 255],
            [127,0,104,160,30,139]]
myColorVals = [[31, 95, 255],
               [255, 212, 128],
               [0,128,0],
               [0,0,0]]
def getContours(img):
    contours,hierarchy = cv2.findContours(img, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    x,y,w,h=0,0,0,0
    for cnt in contours:
        area = cv2.contourArea(cnt)
        # cv2.drawContours(imgContours,cnt,-1,(255,0,0),3)
        if area > 1000:
            cv2.drawContours(imgResult,cnt,-1,(0,0,255),2)
            peri = cv2.arcLength(cnt,True)
            approx = cv2.approxPolyDP(cnt,0.02*peri,True)
            x, y, w, h = cv2.boundingRect(cnt)
    return x+w//2,y

myPoints =  [] #x,y,colorId
def findColor(img, myColors,myColorVals):
    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    count=0
    newPoints=[]
    for i, color in enumerate(myColors):
        lower = np.array(color[0:3])
        upper = np.array(color[3:6])
        mask = cv2.inRange(imgHSV, lower, upper)
        x,y = getContours(mask)
        cv2.circle(imgResult, (x, y), 15, myColorVals[count], cv2.FILLED)
        if x != 0 and y != 0:
            newPoints.append([x, y, count])
        count += 1
        # cv2.imshow(str(color[0]),mask)
    return newPoints

def drawOnCanvas(myPoints,myColorVals):
    for point in myPoints:
        cv2.circle(imgResult, (point[0], point[1]), 10, myColorVals[point[2]], cv2.FILLED)


while True:
    success, img = cap.read()
    imgResult = img.copy()
    if not success:
        break
    newPoints = findColor(img, myColors, myColorVals)
    if len(newPoints) != 0:
        for newP in newPoints:
            myPoints.append(newP)
    if len(myPoints) != 0:
        drawOnCanvas(myPoints, myColorVals)
    cv2.imshow("Result", imgResult)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break



import cv2
import numpy as np
framewidth = 600
frameheight = 480
cap = cv2.VideoCapture(0)
cap.set(3, framewidth)
cap.set(4, frameheight)
cap.set(10, 150)

mycolor = [[0,163,154,50,255,255],
           [52,168,52,120,255,255],
           [93,64,21,174,142,115]]
mycolor_value = [[2, 101, 250], #BGR
                 [209, 136, 0],
                 [207, 0, 176]]

mypoints = [] # x, y, colorID

def find_Color(img, myColor, mycolor_values):
    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    count = 0
    new_points = []
    for color in myColor:
        lower = np.array(color[0:3])
        upper = np.array(color[3:6])
        mask = cv2.inRange(imgHSV, lower, upper)
        x, y = getContours(mask)
        cv2.circle(imgResult, (x, y), 5, mycolor_values[count], cv2.FILLED)
        if x!=0 and y!=0:
            new_points.append([x,y,count])
        count = count + 1
        #cv2.imshow(str(color[0]),mask)
    return new_points

def getContours(img):
    contours, hierarchy = cv2.findContours(img,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    x, y, w, h = 0, 0, 0, 0
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > 500:
            #cv2.drawContours(imgResult, cnt, -1, (255, 0, 0), 3)
            peri = cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, 0.02*peri, True)
            x, y, w, h = cv2.boundingRect(approx)
    return x+w//2, y

def drawonCanvas(mypoints, mycolor_values):

    for point in mypoints:
        cv2.circle(imgResult, (point[0], point[1]), 5, mycolor_values[point[2]], cv2.FILLED)


while True:
    success, img = cap.read()
    imgResult = img.copy()
    newpoints = find_Color(img, mycolor, mycolor_value)
    if len(newpoints)!=0:
        for point in newpoints:
            mypoints.append(point)
    if len(mypoints)!=0:
        drawonCanvas(mypoints,mycolor_value)

    cv2.imshow("video", imgResult)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
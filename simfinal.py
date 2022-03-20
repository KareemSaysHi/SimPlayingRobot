import numpy as np
import cv2
import imutils
from random import *
import time
import serial
import math

boardRead = []
cap = cv2.VideoCapture(0)
player = 1
ai = 2
thinkingPower = 3

lines = [[-1, 0, 0, 0, 0, 0],
         [-1, -1, 0, 0, 0, 0],
         [-1, -1, -1, 0, 0, 0],
         [-1, -1, -1, -1, 0, 0],
         [-1, -1, -1, -1, -1, 0],
         [-1, -1, -1, -1, -1, - 1]]

#CV stuff

def initPoints(cap, warped, pts):
    hsv = cv2.cvtColor(warped, cv2.COLOR_BGR2HSV).astype("float32")

    hsv[:,:,2] = hsv[:,:,2]*2
    hsv[:,:,2] = np.clip(hsv[:,:,2], 0, 255)
    
    frame = cv2.cvtColor(hsv.astype('uint8'), cv2.COLOR_HSV2BGR)
    
    height, width = frame.shape[:2]

    cv2.imshow('frame', frame)
    
    
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    thresh = cv2.threshold(blurred, 50, 255, cv2.THRESH_BINARY_INV)[1]
    cv2.imshow('thresh', thresh)
    cnts = cv2.findContours(thresh, cv2.RETR_EXTERNAL,
    cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    
    number = 0
    for c in cnts:
        M = cv2.moments(c)
        
        if M["m00"] > 10 and M["m00"] < 1000:
            cx = int(M["m10"] / M["m00"])
            cy = int(M["m01"] / M["m00"])
            cv2.drawContours(frame, [c], -1, (0, 255, 255), 2)
            cv2.circle(frame, (cx, cy), 7, (255, 255, 255), 2)
            cv2.putText(frame, str(number), (cx, cy), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,0),2)
            pts.append([cx, cy])
            number += 1
    print(pts)
    cv2.imshow('points', frame)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    return frame, pts

def checkIfRed(points, image, pos1, pos2):
    
    imageCopy = image
    
    cv2.imshow('image', image)
    
    mask = np.zeros(image.shape[:2], dtype='uint8')
    
    if len(points) > 1:
        cv2.line(mask, (points[pos1][0], points[pos1][1]), (points[pos2][0], points[pos2][1]), (255, 255, 255), 15) 

    masked = cv2.bitwise_and(imageCopy, imageCopy, mask=mask)
    
    lower_red = np.array([0, 50, 0])
    upper_red = np.array([100, 255, 100])
    
    redMask = cv2.inRange(masked, lower_red, upper_red)
    redMaskApplied = cv2.bitwise_and(masked, masked, mask=redMask)
    
    redMaskApplied = cv2.GaussianBlur(redMaskApplied, (5, 5), 0)

    threshMask = cv2.cvtColor(redMaskApplied, cv2.COLOR_BGR2GRAY)
    final = cv2.threshold(threshMask, 1, 255, cv2.THRESH_BINARY)[1]
    
    cntsMask = cv2.findContours(final, cv2.RETR_EXTERNAL,
    cv2.CHAIN_APPROX_SIMPLE)
    cntsMask = imutils.grab_contours(cntsMask)
    if len(cntsMask) != 0:
        areaSum = 0
        for c in cntsMask:
            MMask = cv2.moments(c)
            areaSum += MMask["m00"]
            cv2.drawContours(final, [c], -1, (0, 255, 255), 2)
        if areaSum > 700:
            return 1
        else:
            return 0
    else:
        return 0
    
def checkIfSame(old, new):
    diff = cv2.subtract(new, old)
    grayDiff = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
    grayDiffThresh = cv2.threshold(grayDiff, 30, 255, cv2.THRESH_BINARY)[1]

    if cv2.countNonZero(grayDiffThresh) == 0:
        print("nodiff")
        return True
    else:
        print("diff") 
        return False    
    
def checkPlayerMove(frame, points, boardRead):
        for i in range (0, 6):
            for j in range (0, 6):
                if i >= j:
                    boardRead.append(-1)
                else:
                    boardRead.append(checkIfRed(points, frame, i, j))
        return boardRead
    
    
#AI TO CV CONVERSION FUNCTION
    
def cv2ai(aiList, cvList):
    for i in range (0, 6):
        for j in range (0,6):
            cvPos = 6*i + j
            if cvList[cvPos] == 1:
                aiList[i][j] = 1
    print (aiList)
    return aiList
                     
#A FEW MORE CV FUNCTIONS
         
def order_points(pts):
    
    rect = np.zeros((4, 2), dtype="float32")
    
    s = np.sum(pts, axis=1)
    rect[0] = pts[np.argmin(s)]
    rect[2] = pts[np.argmax(s)]
    
    d = np.diff(pts, axis=1)
    print(d)
    rect[1] = pts[np.argmin(d)]
    rect[3] = pts[np.argmax(d)]
    
    return rect
 
def four_point_transform(img, pts):
    rect = order_points(pts)
    (tl, tr, br, bl) = rect
    
    heightA = np.sqrt(((tr[0]-br[0]) ** 2) + ((tr[1]-br[1]) ** 2))
    heightB = np.sqrt(((tl[0]-bl[0]) ** 2) + ((tl[1]-bl[1]) ** 2))
    maxHeight = max(int(heightA), int(heightB))
    
    widthA = np.sqrt(((tr[0]-tl[0]) ** 2) + ((tr[1]-tl[1]) ** 2))
    widthB = np.sqrt(((br[0]-bl[0]) ** 2) + ((br[1]-bl[1]) ** 2))
    maxWidth = max(int(widthA), int(widthB))
    
    dst = np.array([[0, 0], [maxWidth-1, 0], [maxWidth-1, maxHeight-1], [0, maxHeight-1]], dtype = "float32")
    
    M  = cv2.getPerspectiveTransform(rect, dst)
    warped = cv2.warpPerspective(img, M, (maxWidth, maxHeight))
    
    return warped

def findRedPoints(image):
    points = []
    imageCopy = image
    
    #print (image[:,:,2])
    for thing in image[:,:,2]:
        for otherThing in thing:
            if otherThing < 100:
                otherThing = 0
            else:
                otherThing = 255
        
    cv2.imshow("sss", image)
    
    hsv = cv2.cvtColor(imageCopy, cv2.COLOR_BGR2HSV).astype("float32")

    hsv[:,:,2] = hsv[:,:,2]*2
    hsv[:,:,2] = np.clip(hsv[:,:,2], 0, 255)
    
    imageCopy = cv2.cvtColor(hsv.astype('uint8'), cv2.COLOR_HSV2BGR)

    lower_red = np.array([0, 0, 50])
    upper_red = np.array([100,100,255])
    
    redMask = cv2.inRange(imageCopy, lower_red, upper_red)
    
    redMaskApplied = cv2.GaussianBlur(redMask, (5, 5), 0)
    
    cv2.imshow("redMask", redMaskApplied)

    final = cv2.threshold(redMaskApplied, 1, 255, cv2.THRESH_BINARY)[1]
    
    cv2.imshow("final", final)
    
    cntsMask = cv2.findContours(final, cv2.RETR_EXTERNAL,
    cv2.CHAIN_APPROX_SIMPLE)
    cntsMask = imutils.grab_contours(cntsMask)
    
    if len(cntsMask) != 0:
        for c in cntsMask:
            M = cv2.moments(c)
            print (M["m00"])
            if M["m00"] > 500 and M["m00"] < 3000: 
                cx = int(M["m10"] / M["m00"])
                cy = int(M["m01"] / M["m00"])
                cv2.drawContours(image, [c], -1, (0, 255, 255), 2)
                cv2.circle(image, (cx, cy), 7, (255, 255, 255), 2)
                points.append([cx, cy])
    else:
        pass
    cv2.circle(image, (410, 448), 7, (255, 255, 255), -1)

    cv2.imshow("image", image)

    return points

#CV TO AI FUNCTIONS

def cvToMove(tMatrix, x, y):
    xyMatrix = np.array([[x], [y], [1]])
    moveMatrix = tMatrix@xyMatrix
    print(moveMatrix)
    xMove = moveMatrix[0][0]
    yMove = moveMatrix[1][0]
    movePos = "X" + str(int(xMove)) + ",Y" + str(int(yMove)) + "\n"
    print(movePos)
    movePosb = bytes(movePos, 'utf-8')
    ser.write(movePosb)
    
def drawLine(tMatrix, x1, y1, x2, y2, ppl): #points per line
    cvToMove(tMatrix, x1, y1)
    time.sleep(2)
    ser.write(b'D\n')
    time.sleep(.2)
    
    xNew = float(x1)
    yNew = float(y1)
    
    for i in range(0, ppl):
        xNew = xNew + float(x2-x1)/ppl
        yNew = yNew + float(y2-y1)/ppl
        cvToMove(tMatrix, xNew, yNew)
        print([xNew, yNew, i])

        time.sleep(.05)
    time.sleep(1)
    ser.write(b'U\n')

    
#AI FUNCTIONS
  
def checkForWin(lastMove, position):
    for i in range(0, 6):
        if i != lastMove[0] and i != lastMove[1]:
            if i < lastMove[0] and i < lastMove[1]:
                least = i
                middle = lastMove[0]
                biggest = lastMove[1]
            elif i > lastMove[0] and i < lastMove[1]:
                least = lastMove[0]
                middle = i
                biggest = lastMove[1]
            else:
                least = lastMove[0]
                middle = lastMove[1]
                biggest = i
            if position[least][middle] == position[middle][biggest] and position[least][middle] == position[least][biggest] and position[least][middle] != 0:
                return True
    return False

def checkForWinMark(lastMove, position, mark):
    for i in range(0, 6):
        if i != lastMove[0] and i != lastMove[1]:
            if i < lastMove[0] and i < lastMove[1]:
                least = i
                middle = lastMove[0]
                biggest = lastMove[1]
            elif i > lastMove[0] and i < lastMove[1]:
                least = lastMove[0]
                middle = i
                biggest = lastMove[1]
            else:
                least = lastMove[0]
                middle = lastMove[1]
                biggest = i
            if position[least][middle] == position[middle][biggest] and position[least][middle] == position[least][biggest] and position[least][middle] == mark:
                return True
    return False

def trianglePoints(position, one, two, three): #one, two, thre need to be in ascending order, not a problem tho
    playerCount = 0
    aiCount = 0

    if (position[one][two] == 0 and position[two][three] != 0 and position[one][three] != 0) or (position[one][two] != 0 and position[two][three] == 0 and position[one][three] != 0) or (position[one][two] != 0 and position[two][three] != 0 and position[one][three] == 0):  #is one of them open:

        if position[one][two] != 0:
            if position[one][two] == player:
                playerCount += 1
            else:
                aiCount += 1
        elif position[one][three] != 0:
            if position[one][three] == player:
                playerCount += 1
            else:
                aiCount += 1
        elif position[two][three] != 0:
            if position[two][three] == player:
                playerCount += 1
            else:
                aiCount += 1
        return playerCount - aiCount
    else:
        return 0

        


def playerMove(position, mark, image, points):
    boardReadOld = checkPlayerMove(image, points, [])
    #boardRead = checkPlayerMove(image, points, [])
    loop = True
    while loop:
        old = cap.read()[1]
        old = four_point_transform(old, warpPoints)

        for i in range (0, 6):
            new = cap.read()[1]
            cv2.waitKey(50)
        new = four_point_transform(new, warpPoints)
        
        if checkIfSame(old, new): 
            boardRead = checkPlayerMove(new, points, [])
            for i in range (0, 36):
                if boardReadOld[i] != boardRead[i]:
                    loop = False
                    
    print("check")
    print(boardReadOld)
    print(boardRead)
                
    position = cv2ai(lines, boardRead)

def aiMove(position, mark):
    bestMove = [0, 0]
    bestScore = -10000

    for i in range (0, 6):
        for j in range (0, 6):
            if position[i][j] == 0 and i != j:
                position[i][j] = mark
                move = [i, j]
                score = minimax(position, [i, j], thinkingPower, False, -10000, 10000)
                position[i][j] = 0
                if score > bestScore:
                    bestScore = score
                    bestMove = move
    print (bestMove)
    print (bestScore)
    ser.write(b'X179.65,Y0\n') #up
    time.sleep(2)
    ser.write(b'R\n')
    time.sleep(2) 
    drawLine(transformationMatrix, pts[bestMove[0]][0], pts[bestMove[0]][1], pts[bestMove[1]][0], pts[bestMove[1]][1], 30)
    ser.write(b'X0,Y-179.65\n') #out of da wai
    time.sleep(2)
    lines[bestMove[0]][bestMove[1]] = ai

                

def minimax(position, lastMove, depth, maximizing, alpha, beta):
    if checkForWin(lastMove, position):

        if checkForWinMark(lastMove, position, ai):
            return -10000
        else:
            return 10000

    if depth == 0:
        score = evaluatePosition(position)
        return score
    
    if maximizing:
        bestScore = -10000
        for i in range (0, 6):
            for j in range (0, 6):
                if position[i][j] == 0 and i != j:
                    position[i][j] = ai
                    score = minimax(position, [i, j], depth-1, False, alpha, beta)
                    position[i][j] = 0
                    if score > bestScore:
                        bestScore = score
                    alpha = max(alpha, score)
                    if beta <= alpha:
                        break
        return bestScore

    else:   
        bestScore = 10000
        for i in range (0, 6):
            for j in range (0, 6):
                if position[i][j] == 0 and i != j:
                    position[i][j] = player
                    score = minimax(position, [i, j], depth-1, True, alpha, beta)
                    position[i][j] = 0
                    if score < bestScore:
                        bestScore = score
                    beta = min(beta, score)
                    if beta <= alpha:
                        break
        return bestScore




def evaluatePosition(position):
    count = 0

    count += trianglePoints(position, 0, 1, 2)
    count += trianglePoints(position, 0, 1, 3)
    count += trianglePoints(position, 0, 1, 4)
    count += trianglePoints(position, 0, 1, 5)
    count += trianglePoints(position, 0, 2, 3)
    count += trianglePoints(position, 0, 2, 4)
    count += trianglePoints(position, 0, 2, 5)
    count += trianglePoints(position, 0, 3, 4)
    count += trianglePoints(position, 0, 3, 5)
    count += trianglePoints(position, 0, 4, 5)
    count += trianglePoints(position, 1, 2, 3)
    count += trianglePoints(position, 1, 2, 4)
    count += trianglePoints(position, 1, 2, 5)
    count += trianglePoints(position, 1, 3, 4)
    count += trianglePoints(position, 1, 3, 5)
    count += trianglePoints(position, 1, 4, 5)
    count += trianglePoints(position, 2, 3, 4)
    count += trianglePoints(position, 2, 3, 5)
    count += trianglePoints(position, 2, 4, 5)
    count += trianglePoints(position, 3, 4, 5) # 6 choose 3 = 20

    return count







#image, pts = initPoints(cap)

points = [] #points are the ones that are for the cv calibration (red)
cap = cv2.VideoCapture(0);
cap.release()
cap = cv2.VideoCapture(0)
time.sleep(.2)
ret, frame = cap.read()
warpPoints = [[493, 437], [101, 414], [590, 133], [23, 107]] #corners
    
warped = four_point_transform(frame, warpPoints)

cv2.imshow("frame", frame)
cv2.imshow("warped", warped)
cv2.waitKey(0)
cv2.destroyAllWindows()



calX1 = 135
calY1 = 0
calX2 = 90
calY2 = 80
calX3 = 150
calY3 = 70


ser = serial.Serial('/dev/ttyACM0', 9600, timeout=5) 
time.sleep(2);
ser.write(b'K\n'); #restart arduino
time.sleep(2);
#calibration time

calPos1 = "X135,Y-20\n"
calPos1b = bytes(calPos1, 'utf-8')

calPos2 = "X" + str(calX2) + ",Y" + str(calY2) + "\n"
calPos2b = bytes(calPos2, 'utf-8')

calPos3 = "X" + str(calX3) + ",Y" + str(calY3) + "\n"
calPos3b = bytes(calPos3, 'utf-8')

ser.write(b'R\n'); #get ready
time.sleep(.05)
ser.write(b'S-10\n');
time.sleep(.5)
ser.write(b'S10\n');
time.sleep(.5)
ser.write(b'R\n'); #get ready
time.sleep(.05)

ser.write(calPos1b) #move
time.sleep(2)

ser.write(b'D\n'); #draw first point
time.sleep(.5)

for i in range (0, 2):
    ser.write(b'S5\n');
    time.sleep(.2)
    ser.write(b'S-10\n');
    time.sleep(.2)
    ser.write(b'S5\n');
    time.sleep(.2)
    
ser.write(b'U\n');
time.sleep(.5)

ser.write(calPos2b) #move to second point
time.sleep(2)

ser.write(b'D\n'); #draw second point 
time.sleep(.5)

for i in range (0, 2):
    ser.write(b'S5\n');
    time.sleep(.2)
    ser.write(b'S-10\n');
    time.sleep(.2)
    ser.write(b'S5\n');
    time.sleep(.2)
    
ser.write(b'U\n');
time.sleep(.5)

ser.write(calPos3b) #move to third point
time.sleep(2)

ser.write(b'D\n'); #draw third point
time.sleep(.5)

for i in range (0, 2):
    ser.write(b'S5\n');
    time.sleep(.2)
    ser.write(b'T-1\n');
    ser.write(b'S-10\n');
    time.sleep(.2)
    ser.write(b'T1\n');
    ser.write(b'S5\n');
    time.sleep(.2)
    
ser.write(b'U\n');
time.sleep(.5)


ser.write(b'X0,Y-179.65\n') #move out of the way
time.sleep(2)

for i in range(0, 6):
    ret, frame = cap.read();
warped = four_point_transform(frame, warpPoints)
points = findRedPoints(warped)
cv2.waitKey(0)

cv2.destroyAllWindows();

cvp1 = points[0]
cvp2 = points[1]
cvp3 = points[2]
    
print(points)

#gotta match points
if min([points[0][0], points[1][0], points[2][0]]) == points[0][0]: #find min x val
    cvp1 = points[0]
    if min([points[1][1], points[2][1]]) == points[1][1]: #find y min val
        cvp2 = points[1]
        cvp3 = points[2]
    else:
        cvp2 = points[2]
        cvp3 = points[1]
        
elif min([points[0][0], points[1][0], points[2][0]]) == points[1][0]: #find min x val
    cvp1 = points[1]
    if min([points[0][1], points[2][1]]) == points[0][1]: #find y min val
        cvp2 = points[0]
        cvp3 = points[2]
    else:
        cvp2 = points[2]
        cvp3 = points[0]
        
else:
    cvp1 = points[2]
    if min([points[0][1], points[1][1]]) == points[0][1]: #find y min val
        cvp2 = points[0]
        cvp3 = points[1]
    else:
        cvp2 = points[1]
        cvp3 = points[0]
        
m1 = [calX1, calY1]
m2 = [calX2, calY2]
m3 = [calX3, calY3]

 

#cvp points are x-y coordinates of red dots from CV (raspberry pi) perspective
#m points are x-y coordinates of the red dots from the machine (arduino) perspective
A = np.array([[cvp1[0], cvp1[1], 1], [cvp2[0], cvp2[1], 1], [cvp3[0], cvp3[1], 1]])
B = np.array([[m1[0], m1[1], 1], [m2[0], m2[1], 1], [m3[0], m3[1], 1]])

A = A.astype(np.float64)
B = B.astype(np.float64)


X = np.array(np.linalg.solve(A, B))

transformationMatrix = X.transpose()

pts = initPoints(cap, warped, [])[1]




while cap.isOpened():
    for i in range(0, 6):
        ret, frame = cap.read();
    warped = four_point_transform(frame, warpPoints)
    
    hsv = cv2.cvtColor(warped, cv2.COLOR_BGR2HSV).astype("float32")

    hsv[:,:,2] = hsv[:,:,2]*2
    hsv[:,:,2] = np.clip(hsv[:,:,2], 0, 255)
    
    image = cv2.cvtColor(hsv.astype('uint8'), cv2.COLOR_HSV2BGR)     
    
    playerMove(lines, player, warped, pts)
    
    
    #print(lines)
    aiMove(lines, ai)
    print(lines) 
    

cv2.destroyAllWindows()
cap.release()


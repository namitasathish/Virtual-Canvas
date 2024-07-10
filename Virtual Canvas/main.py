import cv2
import numpy as np
import time
import os
import HandTrackingModule as htm

script_dir = os.path.dirname(os.path.abspath(__file__))
images_dir = os.path.join(script_dir, 'images')
myList=os.listdir(images_dir)

print(myList)

overlayList=[]
for imgPath in myList:
    image=cv2.imread(f'{images_dir}/{imgPath}')
    overlayList.append(image)
print(len(overlayList))    

header=overlayList[0]

drawColor=(0,0,255)#default color red

cap=cv2.VideoCapture(0)
cap.set(3,1280)
cap.set(4,720)

detector=htm.handDetector(detectionCon=0.85)

xp,yp=0,0
imgCanvas=np.zeros((720,1280,3),np.uint8)

while True:
    success, img =cap.read()
    img=cv2.flip(img,1)

    img=detector.findHands(img)
    lmList=detector.findPosition(img, draw=False)

    if len(lmList)!=0:
      
        #print(lmList)

        #tip of index finger
        x1,y1=lmList[8][1:]
        #tip of middle finger
        x2,y2=lmList[12][1:]

        fingers=detector.fingersUp()
        #print(fingers)

        #selection mode
        if fingers[1] and fingers[2]:
            xp,yp=0,0
           
            print("selection mode")
            if y1<174:
                if 450<x1<550:
                    header=overlayList[0]
                    drawColor=(0,0,255)#red
                elif 650<x1<750:
                    header=overlayList[1]
                    drawColor=(96, 158, 0)#green
                elif 800<x1<950:
                    header=overlayList[2] 
                    drawColor=(255, 165, 0)#blue
                elif 1050<x1<1200:
                    header=overlayList[3] 
                    drawColor=(0,0,0)   #black           
            cv2.rectangle(img,(x1,y1-15),(x2,y2+15),drawColor,cv2.FILLED)
            cv2.rectangle(img,(x1,y1-15),(x2,y2+15),(255,255,255),thickness=2)

        #drawing mode
        if fingers[1] and fingers[2]==False:
            cv2.circle(img,(x1,y1),10,drawColor,cv2.FILLED)
            cv2.circle(img, (x1, y1), 10, (255,255,255), thickness=2)
            print("drawing mode")   

            #drawing for the first time
            if xp==0 and yp==0:
                xp,yp=x1,y1

            if drawColor ==(0,0,0):
              cv2.line(img,(xp,yp),(x1,y1),drawColor,thickness=30) 
              cv2.line(imgCanvas,(xp,yp),(x1,y1),drawColor,thickness=100)     
            else:
              cv2.line(img,(xp,yp),(x1,y1),drawColor,thickness=15) 
              cv2.line(imgCanvas,(xp,yp),(x1,y1),drawColor,thickness=15) 
            xp,yp=x1,y1

    imgGray=cv2.cvtColor(imgCanvas,cv2.COLOR_BGR2GRAY)  
    _,imgInv=cv2.threshold(imgGray,50,255,cv2.THRESH_BINARY_INV)  
    imgInv=cv2.cvtColor(imgInv,cv2.COLOR_GRAY2BGR)  
    img=cv2.bitwise_and(img,imgInv)
    img=cv2.bitwise_or(img,imgCanvas)



    

 

    h,w,c=overlayList[0].shape
    #img=cv2.addWeighted(img,0.5,imgCanvas,0.5,0)
    img[0:h,0:w]=header
    cv2.imshow("Image",img)
    cv2.imshow("Canvas",imgCanvas)
    cv2.waitKey(1)
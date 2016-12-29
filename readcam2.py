import numpy as np
import cv2
import time

cap = cv2.VideoCapture(0)
starttime=time.time()

fontFace = cv2.FONT_HERSHEY_PLAIN
fontScale = 1;
color = (0,0,255)
width = int(cap.get(3))
height = int(cap.get(4))
resolution = str(width) + "x" + str(height)
org = (10,height-10)
M = cv2.getRotationMatrix2D((width/2,height/2),170,1)
digitMinHeight = 40
digitMaxHeight = 55
digitMinWidth = 5

def process(frame):

       return frame    

#def findLines(frame):


while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()

    dt = time.time()
    text = resolution + " // " + str(dt) + " // " + str (dt - starttime)

#    if ret==True:
#       frame = cv2.flip(frame,0)

    if ret==True:
 

    # Our operations on the frame come here
       

       frame = cv2.warpAffine(frame,M,(width,height))
       oriframe=frame
       frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
       frame = cv2.Canny(frame,100,140)

       cv2.imshow('frame',frame)

       if cv2.waitKey(10000) & 0xFF == ord('q'):
            break

    
# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()

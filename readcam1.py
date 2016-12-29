import numpy as np
import cv2
import time, datetime
from KNearestOcr import KNearestOcr


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
ocr=KNearestOcr()
ocr.initModel()


def process(frame):

       return frame    

#def findLines(frame):

i = None

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()
    if i is None:
        i=0
    i += 1
    if i < 10:
        print "i <10"
        cv2.imshow('f',frame)
	cv2.waitKey(1)
        continue
    cv2.destroyWindow ('f')

    dt = time.time()
    dt_string = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    text = resolution + " // " + dt_string + " // " + str (dt - starttime)

#    if ret==True:
#       frame = cv2.flip(frame,0)

    if ret==True:
 

    # Our operations on the frame come here
       

       frame = cv2.warpAffine(frame,M,(width,height))
       oriframe=frame
       frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
       frame = cv2.Canny(frame,200,450)
       cannyframe=frame.copy()

# detect lines
       lines = cv2.HoughLines(frame,1,np.pi/180,140)
       if lines is not None:

           for l, line in enumerate(lines):
               for rho,theta in line:
                   deg = (theta/np.pi*180)-90
                   if deg<1:
		       print rho
                   a = np.cos(theta)
	           b = np.sin(theta)
                   x0 = a*rho
	           y0 = b*rho
                   x1 = int(x0 + 1000*(-b))
                   y1 = int(y0 + 1000*(a))
                   x2 = int(x0 - 1000*(-b))
                   y2 = int(y0 - 1000*(a))

                   cv2.line(oriframe,(x1,y1),(x2,y2),(0,0,255),1)
		   cv2.putText(oriframe,str(l)+".",(x0,y0),fontFace,fontScale,color)
           print

# find and filter contours
       contours, hierarchy = cv2.findContours(frame,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
       filteredContours = [] 
       for c, contour in enumerate(contours):
           x,y,w,h = cv2.boundingRect(contour)
           if (h>digitMinHeight) and (h<digitMaxHeight) and (w>digitMinWidth) and (w< h) and (y<200):
               cv2.rectangle(oriframe,(x,y),(x+w,y+h),(255,0,0))
               filteredContours.append(contour)
               print y

# sort contours according to x coordinate of bounding box
       sortedContours = sorted (filteredContours, key=lambda contour: cv2.boundingRect(contour)[0])

# cut out digits
       digits = []
       for c, contour in enumerate(sortedContours):
           x,y,w,h = cv2.boundingRect(contour)
           cv2.putText(oriframe,str(c)+".",(x,y),fontFace,fontScale,(255,0,0))
           digits.append(cannyframe[y:y+h, x:x+w])

       recognized = []
# display the cut out digits
       if len(digits) is 7:
           for d, digit in enumerate(digits):
               r = ocr.recognize(digit)[0]
               recognized.append(str(int(r)))
#               cv2.imwrite(dt_string + "_" + str(d) + ".png", digit)
           value = ''.join(recognized)
           print dt_string + ": " + value
           with open("zaehlerstand.txt", "a") as myfile:
               myfile.write(dt_string + ": " + value + "\n")
    #           cv2.imshow(str(d), digit)


       cv2.putText(oriframe,text,org,fontFace,fontScale,color)
       cv2.imshow('oriframe',oriframe)
       cv2.imshow('frame',cannyframe)
       if cv2.waitKey(10000) & 0xFF == ord('q'):
            break

    
# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()

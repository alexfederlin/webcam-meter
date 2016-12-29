from KNearestOcr import KNearestOcr
import os,cv2

x=KNearestOcr()

r = 0
x.initModel()

for i in os.listdir(os.getcwd()):
    if i.endswith(".png"): 
        print i
        img = cv2.imread(i)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        r = x.recognize(img)
        print "recognize returned: " + str(r)
        reco = (int(r[0]))
        os.rename (i,str(reco)+"/"+i)


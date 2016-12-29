from KNearestOcr import KNearestOcr
import os,cv2

x=KNearestOcr()

x.loadTrainingData()
r = 0
for i in os.listdir(os.getcwd()):
    if i.endswith(".png"): 
        print i
        img = cv2.imread(i)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        r = x.learn(img)
        print "learn returned: " + str(r)
        if r == -1:
            break 
        if r >= 0 and r <= 9:  
            os.rename (i,str(r)+"/"+i)


x.saveTrainingData() 
x.initModel()

for r,response in enumerate(x._responses):
    print r
    print response

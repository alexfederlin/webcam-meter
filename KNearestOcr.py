import numpy as np
import cv2

class KNearestOcr:
    """A simple example class"""
    _responses = None
    _samples = None
    _knn = None

    def prepareSample(self, img):
        res_img = cv2.resize(img, (10,10))
        print res_img.shape
        out = res_img.reshape(-1,100).astype(np.float32) # each 10x10 image flattened into a 1x100 matrix
        print out.shape
        return out

    def learn (self, img):
        cv2.imshow('learn', img)
        k = cv2.waitKey(0)
        resp = k - 1048624
        print k
        if  resp >= 0 and resp <= 9:

            if self._responses is None:
                self._responses = np.array([resp])
            else:
                self._responses = np.vstack((self._responses, np.array([resp])))

            if self._samples is None:
                self._samples = self.prepareSample(img)
            else:
                self._samples = np.vstack((self._samples,self.prepareSample(img)))

            print "responses shape: " + str(self._responses.shape)
            print "samples shape: " + str(self._samples.shape)

        if k%256 == ord('q'):
            print "returning -1"
            return -1
        print "returning 0"
        return 0

    def saveTrainingData(self):
        np.savez("train.npz",samples=self._samples, responses=self._responses)

    def loadTrainingData(self):
        traindata = np.load("train.npz")
        self._responses=traindata['responses']
        self._samples=traindata['samples']

    def initModel(self):
        self._knn = cv2.KNearest()
        if self._samples is None or self._responses is None:
            self.loadTrainingData()
        self._knn.train(self._samples, self._responses)
    
    def recognize(self,img):
        return self._knn.find_nearest(self.prepareSample(img), k=5)

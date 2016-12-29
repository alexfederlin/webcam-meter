import os
from datetime import datetime

class Plausi:
    """A plausibility checker"""
    _readvalues = []
    _checkedvalues = []
    

    def loadValues(self, filename):
        file = open(filename)
        for line in file:
            fields = line.strip().split(':')
            self._readvalues.append( (fields[0], fields[1]) )
        #for i, (date, val) in enumerate(self._readvalues):
        #    print date + " Zaehlerstand: " + val

    def deltaP(self,val1,val2):
        FMT='%Y%m%d%H%M%S'
        delta_t = ( datetime.strptime(val1[0], FMT) - datetime.strptime(val2[0], FMT) ).total_seconds() / 3600 # in h 
        delta_w = float( int(val1[1])  - int(val2[1])) / 10 # in kWh
        delta_p = delta_w / delta_t
        return delta_p

    def checkValues(self):
        for i, (date, val) in enumerate(self._readvalues):
            if i == 0:
                print "skipping first value and assuming it is valid"
                self._checkedvalues.append ( (date,val) )
                continue

            print val + " previous: " + self._readvalues[i-1][1] + " lastchecked: " + self._checkedvalues[-1][1]
            print 
            if val > self._checkedvalues[-1][1]:
                print "current value is larger or equal than last checkedvalue. Good."
                delta_p = self.deltaP(self._readvalues[i], self._checkedvalues[-1])
#                FMT='%Y%m%d%H%M%S'
#                delta_t = ( datetime.strptime(date, FMT) - datetime.strptime(self._checkedvalues[-1][0], FMT) ).total_seconds() / 3600 # in h 
#                delta_w = float( int(val)  - int(self._checkedvalues[-1][1])) / 10 # in kWh
#                delta_p = delta_w / delta_t
                if delta_p > 1.5:
                    #print str(delta_w) + "/" + str(delta_t.total_seconds()) + "= delta_p: " + str(delta_p) +". Too big a jump - implausible"
                    pass
                else:
                    #print str(delta_w) + "/" + str(delta_t) + "=delta_p: " + str(delta_p) +". plausible"
                    print "delta_p: " + str(delta_p) +". plausible"
                    print "adding " + val + " as checked value"
                    #raw_input("Press Enter to continue...")

                    self._checkedvalues.append ( (date,val) )
        for i, (date, val) in enumerate(self._checkedvalues):
            if 'j' in locals():
                if int(val)-10 > int(self._checkedvalues[j][1]):
                    #calculate power consumption
                    delta_p=self.deltaP(self._checkedvalues[i],self._checkedvalues[j])
                    print str(date) + ": delta_p: " + str(delta_p)
                    j=i
            else:
                j=0
            print date + " checked Zaehlerstand: " + val


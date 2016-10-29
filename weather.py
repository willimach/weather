from Adafruit_BME280 import *

import  time, threading
from datetime import datetime
from weather_bib import *

sensor1 = BME280(mode=BME280_OSAMPLE_8,address=0x76)
sensor2 = BME280(mode=BME280_OSAMPLE_8,address=0x77)
offset1=-2.0
offset2=-1.5

def logging():
    while True:
        try:
            if (datetime.now().minute % 5)==0:
            #if datetime.now().second % 5:
                f=open('weatherlog.txt','a')
                my_time = mytime()
                mystring = str(my_time) + ', ' + str(scan(sensor1,offset1))[1:-1] + ', ' + str(scan(sensor2,offset2))[1:-1]
                f.write(mystring+'\n')
                f.close()
                #print('logged!')
                time.sleep(60)
        except:
            pass
def maintenance():
    while True:
        try:
            if (datetime.now().minute % 15) == 0:
            #if datetime.now().second % 5:
                myplotter(1,4,'T')
                myplotter(2,5,'H')
                myplotter(3,6,'P')
                myftp()
                #print('maintenanced!')
                time.sleep(60)
        except:
            pass
# lock to serialize console output
lock = threading.Lock()
    
# Create the thread pool.
s = threading.Thread(target=logging)
t = threading.Thread(target=maintenance)
s.daemon = True  # thread dies when main thread (only non-daemon thread) exits.
t.daemon = True
s.start()
t.start()   
while True:
    time.sleep(1)

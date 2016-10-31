from Adafruit_BME280 import *

import  time, threading, os
from datetime import datetime
from weather_bib import *

sensor1 = BME280(mode=BME280_OSAMPLE_8,address=0x76)
sensor2 = BME280(mode=BME280_OSAMPLE_8,address=0x77)
T_offset1=-2.0
T_offset2=-1.8
H_offset1=0.0
H_offset2=0.0

path='/home/pi/sharepi3/weather/'
os.chdir(path)

def logging():
    while True:
        try:
            if (datetime.now().minute % 5)==0:
            #if datetime.now().second % 5:
                f=open('weatherlog.txt','a')
                my_time = mytime()
                mystring = str(my_time) + ', ' + str(scan(sensor1,T_offset1,H_offset1))[1:-1] + ', ' + str(scan(sensor2,T_offset2,H_offset2))[1:-1]
                f.write(mystring+'\n')
                f.close()
                #print('logged!')
            time.sleep(1)
        except:
            #print('Log-Fehler')
            pass
        time.sleep(60)
def maintenance():
    while True:
        try:
            if (datetime.now().minute % 15) == 0:
            #if datetime.now().second % 5:
                myplotter(1,4,'T',0)
                myplotter(2,5,'H',0)
                myplotter(3,6,'P',0)
                myplotter(1,4,'T',7)
                myplotter(2,5,'H',7)
                myplotter(3,6,'P',7)
                myftp()
                #print('maintenanced!')
            time.sleep(1)
        except:
            #print('maint.Fehler')
            pass
        time.sleep(60)
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
    time.sleep(100)

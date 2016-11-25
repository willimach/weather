from Adafruit_BME280 import *
from queue import Queue
from datetime import datetime
from weather_bib import *
import  time, threading, os, logging, logging.handlers

sensor1 = BME280(mode=BME280_OSAMPLE_8,address=0x76)
sensor2 = BME280(mode=BME280_OSAMPLE_8,address=0x77)
T_offset1=-2.0
T_offset2=-1.8
H_offset1=0.0
H_offset2=0.0

path='/home/pi/sharepi3/weather/'
os.chdir(path)

#logging
logfilename='Pilog.txt'
mylogger=logging.getLogger('MyLogger')
mylogger.setLevel(logging.INFO)

handler=logging.handlers.RotatingFileHandler(logfilename,maxBytes=1024*100,backupCount=3)
mylogger.addHandler(handler)

mylogger.info(StatusPi('\t\tStarted!'))


def weatherlog():
    try:
        mylogger.info(StatusPi('logging...'))
        my_time = mytime()
        mystring = str(my_time) + ', ' + str(scan(sensor1,T_offset1,H_offset1))[1:-1] + ', ' + str(scan(sensor2,T_offset2,H_offset2))[1:-1] + ', ' + str(URLextractor())[1:-1]
        f=open('weatherlog.txt','a')
        f.write(mystring+'\n')
        f.close()
        mylogger.info(StatusPi('logged'))
    except:
        mylogger.info(StatusPi('Logging-Error!'))
        pass
    
def maintenance():
    try:
        mylogger.info(StatusPi('before Plots'))
        myplotter(1,4,7,'T',0)
        myplotter(2,5,8,'H',0)
        myplotter(3,6,9,'P',0)
        myplotter(1,4,7,'T',7)
        myplotter(2,5,8,'H',7)
        myplotter(3,6,9,'P',7)
        mylogger.info(StatusPi('after Plots'))
        myftp()
        mylogger.info(StatusPi('after upload'))
    except:
        mylogger.info(StatusPi('Maintenance-Error!'))
        pass



# lock to serialize console output
lock = threading.Lock() 

def do_work(item):
    with lock:
        if item == 0:
            weatherlog()
        elif item == 1:
            maintenance()


# The worker thread pulls an item from the queue and processes it
def worker():
    while True:
        item = q.get()
        do_work(item)
        q.task_done()
        
    
# Create the queue and thread pool.
q = Queue()
t = threading.Thread(target=worker)
t.daemon = True  # thread dies when main thread (only non-daemon thread) exits.
t.start()
    
# stuff work items on the queue (in this case, just a number).
while 1:
    if (datetime.now().minute % 5)==0 and q.qsize() < 3: #just 2 items in queue
        q.put(0) #12 is random item
    if (datetime.now().minute % 15)==0:
        q.put(1)
    time.sleep(60)
        
            
q.join()       # block until all tasks are done   
mylogger.info(StatusPi('End weather logging.'))


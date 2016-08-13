import Adafruit_DHT, time
from datetime import datetime

sensor = Adafruit_DHT.DHT11
pin = 21


def mytime():
    import time, datetime
    mytime=datetime.datetime.now()
    date = "%04d.%02d.%02d_%02d:%02d:%02d" % (mytime.year, mytime.month, mytime.day, mytime.hour, mytime.minute, mytime.second)
    return(date)




while 1:
    my_time   = mytime()
    if int(my_time[-2:]) % 20 == 0:
	hum, temp = Adafruit_DHT.read_retry(sensor, pin)
        f=open('weatherlog.txt','a')
	mystring=str(my_time) + '\t' + str(hum) + '\t' + str(temp) + '\n'
        f.write(mystring)
	#print(mystring)
        f.close()
        time.sleep(1)

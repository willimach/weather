import Adafruit_DHT, time
from datetime import datetime

sensor = Adafruit_DHT.DHT11
pin = 21


def mytime():
    import time, datetime
    mytime=datetime.datetime.now()
    date = "%04d.%02d.%02d_%02d:%02d:%02d" % (mytime.year, mytime.month, mytime.day, mytime.hour, mytime.minute, mytime.second)
    return(date)

def myftp():
    from ftplib import FTP
    
    ftp=FTP('willi.mach.at',user='willi',passwd='wi78lli')
    file=open('weatherlog.txt','rb')
    ftp.cwd('www')
    ftp.storbinary('STOR weatherlog.txt',file)
    file.close()
    ftp.quit()


hum, temp = Adafruit_DHT.read_retry(sensor, pin)

while 1:
    mytime=datetime.now().minute
    if mytime == 5 or time == 20 or time == 35 or time == 50:
        f=open('weatherlog.txt','a')
        f.write(str(mytime) + '\t' + str(hum) + '\t' + str(temp) + '\n')
        f.close()
        myftp()
        time.sleep(60)

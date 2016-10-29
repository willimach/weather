
def scan(sensor,offset):
    temp = round(sensor.read_temperature()+offset,1)
    humi = round(sensor.read_humidity(),1)
    press_sea = round(sensor.read_pressure()/100 + 12*3,1)
    return temp,humi,press_sea


def mytime():
    import time, datetime
    mytime=datetime.datetime.now()
    date = "%04d.%02d.%02d_%02d:%02d:%02d" % (mytime.year, mytime.month, mytime.day, mytime.hour, mytime.minute, mytime.second)
    return(date)

def plotextractor(a):
    f=open('weatherlog.txt','r')
    myfile=f.read()
    mylines=myfile.split('\n')
    mylines.pop(-1)

    mylist=[]
    for element in mylines:
        element=element.split(', ')
        mylist.append(element[a])    
    return mylist

def myplotter(column1,column2,quantity):
    # Force matplotlib to not use any Xwindows backend.
    import matplotlib, numpy, datetime
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    from matplotlib.dates import DayLocator, HourLocator, DateFormatter, drange,date2num,num2date
    import gc
    
    timelist = plotextractor(0)
    y1 = plotextractor(column1)
    y2 = plotextractor(column2)

    fig, ax = plt.subplots(figsize=(24,8))
    plt.xticks(rotation=45)
    
    plt.title('FGG36 weather' + '  '*40 + mytime(),loc='right')
    


    x=[]
    for element in timelist:
        x.append(datetime.datetime(int(element[0:4]),int(element[5:7]),int(element[8:10]),int(element[11:13]),int(element[14:16])))
    
    date1 = datetime.datetime(int(timelist[0][0:4]),int(timelist[0][5:7]),int(timelist[0][8:10]))
    date2 = datetime.datetime(int(timelist[-1][0:4]),int(timelist[-1][5:7]),int(timelist[-1][8:10])+1)

    ax.set_xlim(date1,date2)    
    ax.xaxis.set_major_locator(DayLocator())
    ax.xaxis.set_major_formatter(DateFormatter('%Y-%m-%d'))
    
    ax.xaxis.set_minor_locator(HourLocator([6,12,18]))
    ax.xaxis.set_minor_formatter(DateFormatter('%H:%M'))

    ax.grid(True,which='minor',linestyle='--')
    ax.grid(True,which='major',linestyle='-')
    
    plt.plot(x,y1,label="inside")
    plt.plot(x,y2,label="outside")
    plt.legend(bbox_to_anchor=(0.95, 0.95), borderaxespad=0.)


    plt.savefig(quantity + '.png',bbox_inches='tight')
    
    plt.clf()
    plt.close()
    gc.collect()



def myftp():
    from ftplib import FTP
    import weather_conf

    server=weather_conf.server
    user=weather_conf.user
    passwd=weather_conf.passwd

    ftp=FTP(server,user=user,passwd=passwd)
    ftp.cwd('www')


    file=open('H.png','rb')
    ftp.storbinary('STOR H.png',file)
    file.close()
    
    file=open('P.png','rb')
    ftp.storbinary('STOR P.png',file)
    file.close()
    
    file=open('T.png','rb')
    ftp.storbinary('STOR T.png',file)
    file.close()
    
    ftp.quit()




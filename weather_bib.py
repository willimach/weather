def scan(sensor,T_offset,H_offset):
    import gc
    temp = round(sensor.read_temperature()+T_offset,1)
    humi = round(sensor.read_humidity()+H_offset,1)
    press_sea = round(sensor.read_pressure()/100 + 12*3,1)
    gc.collect()
    return temp,humi,press_sea



def mytime():
    import time, datetime
    mytime=datetime.datetime.now()
    date = "%04d.%02d.%02d_%02d:%02d:%02d" % (mytime.year, mytime.month, mytime.day, mytime.hour, mytime.minute, mytime.second)
    return(date)



def plotextractor(a):
    import numpy, re
    f=open('weatherlog.txt','r')
    myfile=f.read()
    mylines=myfile.split('\n')
    mylines.pop(-1)
    f.close()
    
    mylist=[]
    for element in mylines:
        element=element.split(', ')
        if re.search("[+-]?\d+(?:\.\d+)?", element[a]) == None:
            mylist.append(numpy.nan)
        else:
            mylist.append(element[a])
    del mylines
    return mylist



def myplotter(column1,column2,column3,quantity,plottimedays):
    # Force matplotlib to not use any Xwindows backend.
    import matplotlib, numpy, datetime
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    from matplotlib.dates import DayLocator, HourLocator, DateFormatter, drange,date2num,num2date
    import gc

    # define time and y-lists for plotting
    timelist = plotextractor(0)
    y1 = plotextractor(column1)
    y2 = plotextractor(column2)
    y3 = plotextractor(column3)
    #y3 = filter(None, plotextractor(column3))
    #print(plotextractor(colum3))
    #y3 = [77 if x==None else x for x in plotextractor(column3)]
    #print(y3)
    #print(type(y3))
    
    #define image size
    fig, ax = plt.subplots(figsize=(36,8))
    #plot title
    plt.title('FGG36 weather' + '  '*90 + mytime(),loc='right')
    #rotate dates on x-axis
    plt.xticks(rotation=45)
    plt.tick_params(labelright=True)
    
    
    

    #change readable timestampt to datetime-objects
    x=[]
    for element in timelist:
        x.append(datetime.datetime(int(element[0:4]),int(element[5:7]),int(element[8:10]),int(element[11:13]),int(element[14:16])))

    #adding ZAMG-data implemented later: Hence, x and y lists are shorter
    # -> workaround!
    xZAMG=[]
    for i in range(len(y3)):
        xZAMG.append(x[len(x)-len(y3)+i])

    #distinguish between long and short plots - define plotstart
    #(long means all date (0) and short means e.g. 7 dayss)
    if plottimedays==0:
        namestring='weather_'+quantity+'_all'
        date1 = datetime.datetime(int(timelist[0][0:4]),int(timelist[0][5:7]),int(timelist[0][8:10]))
    else:
        namestring='weather_'+quantity+'_lastdays'
        #subtract plottiedays from latest timestamp
        date1 = datetime.datetime(int(timelist[-1][0:4]),int(timelist[-1][5:7]),int(timelist[-1][8:10])) + datetime.timedelta(days=1) + datetime.timedelta(days=-plottimedays)

    #subtract 1 day from latest timestamp so that current day is full visible in plot        
    date2 = datetime.datetime(int(timelist[-1][0:4]),int(timelist[-1][5:7]),int(timelist[-1][8:10])) + datetime.timedelta(days=1)



    ax.set_xlim(date1,date2)    
    ax.xaxis.set_major_locator(DayLocator())
    ax.xaxis.set_major_formatter(DateFormatter('%Y-%m-%d'))

    if plottimedays != 0:
        ax.xaxis.set_minor_locator(HourLocator([6,12,18]))
        ax.xaxis.set_minor_formatter(DateFormatter('%H:%M'))

    ax.grid(True,which='minor',linestyle='--')
    ax.grid(True,which='major',linestyle='-')

    #define legend    
    plt.plot(x,y1,label="inside")
    plt.plot(x,y2,label="outside")
    plt.plot(xZAMG,y3,label="ZAMG",marker='_',linewidth=0)
    plt.legend(bbox_to_anchor=(0.51, 0.95), borderaxespad=0.)

    #save
    plt.savefig(namestring + '.png', bbox_inches='tight')

    #clean to prevent full RAM
    del x, xZAMG,timelist, y1,y2,y3,date1,date2,namestring
    plt.clf()
    plt.close()
    gc.collect()



def myftp():
    from ftplib import FTP
    import weather_conf,logging
    try:
        server=weather_conf.server
        user=weather_conf.user
        passwd=weather_conf.passwd

        ftp=FTP(server,user=user,passwd=passwd)
        ftp.cwd('www')

        #all time plots
        file=open('weather_T_all.png','rb')
        ftp.storbinary('STOR weather_T_all.png',file)
        file.close()

        file=open('weather_P_all.png','rb')
        ftp.storbinary('STOR weather_P_all.png',file)
        file.close()

        file=open('weather_H_all.png','rb')
        ftp.storbinary('STOR weather_H_all.png',file)
        file.close()
        #7day plots
        file=open('weather_T_lastdays.png','rb')
        ftp.storbinary('STOR weather_T_lastdays.png',file)
        file.close()

        file=open('weather_P_lastdays.png','rb')
        ftp.storbinary('STOR weather_P_lastdays.png',file)
        file.close()

        file=open('weather_H_lastdays.png','rb')
        ftp.storbinary('STOR weather_H_lastdays.png',file)
        file.close()   


        ftp.quit()
    except:
        logging.info(StatusPi('FTP-ERROR!'))
        pass
                     
def URLextractor():
    try:
        #extracts fromm ZAMG values for T,H,P
        import re
        from urllib.request import urlopen

        url = 'https://www.zamg.ac.at/cms/de/wetter/wetterwerte-analysen/wien/temperatur/?mode=geo&druckang=red'

        #data = urlopen(url)
        #mydata=str(urlopen(url).read())
        #mylines=str(urlopen(url).read()).split('\\n')
        JWarte=str(urlopen(url).read()).split('\\n')[1101]
        mylist=re.findall("[+-]?\d+(?:\.\d+)?", JWarte)
        ZAMG = float(mylist[3]), float(mylist[4]), float(mylist[10])
        del url, JWarte,mylist
        return ZAMG

    except:
        return ', , , ,'




def StatusPi(errorstring):
    # saves CPU time & RAM usage if error handling occurs
    import os, platform, sys,subprocess
    answerRAM=str(subprocess.check_output("free -m",shell=True))
    lsRAM=answerRAM.split(' ')
    lsRAM=list(filter(None,lsRAM))
    #print(lsRAM)
    #print(len(lsRAM))
    RAM=lsRAM[7] + ' ' + lsRAM[8] + ' ' + lsRAM[9] + '   ' + lsRAM[10] + ' ' + lsRAM[11] + ' ' + lsRAM[12][0:-5] + '   ' + lsRAM[14] + ' ' + lsRAM[15][0:-7]
    #print(RAM)
    mystring=str(mytime()) + '\t' + RAM + '\t' + errorstring
    return mystring


    

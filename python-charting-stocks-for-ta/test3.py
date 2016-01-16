import time
import datetime
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import matplotlib.dates as mdates

eachStock = 'AAPL','TSLA'

def graphData(stock):
    try:
        stockFile = stock+'.txt'

        date, closep, highp, lowp, openp, volume = np.loadtxt(stockFile,delimiter=',',unpack=True,
                                                         converters={0: mdates.strpdate2num('%Y%m%d')})


        fig = plt.figure()
        ax1 = plt.subplot(1,1,1)
        ax1.plot(date, openp)
        ax1.plot(date, highp)
        ax1.plot(date, lowp)
        ax1.plot(date, closep)

        ax1.xaxis.set_major_locator(mticker.MaxNLocator(10))
        ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))

        for label in ax1.xaxis.get_ticklabels():
            label.set_rotation(45)


        plt.show()

    except Exception,e:
        print 'failed main loop',str(e)

for stock in eachStock:
    graphData(stock)
    time.sleep(555)
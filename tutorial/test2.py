#encoding:utf-8
import urllib2
import time
import datetime

#选定股票池
stocksToPull = 'AAPL','GOOG','MSFT','CMG','AMZN','EBAY','TSLA'
#定义获取数据函数
def pullData(stock):
    try:
        print 'Currently pulling',stock
        print str(datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'))
        urlToVisit = 'https://chartapi.finance.yahoo.com/instrument/1.0/'+stock+'/chartdata;type=quote;range=10d/csv'
        saveFileLine = stock+'.txt'

        try:
            readExistingData = open(saveFileLine,'r').read()
            splitExisting = readExistingData.split('\n')
            mostRecentLine = splitExisting[-2]
            lastUnix = mostRecentLine.split(',')[0]
        except Exception,e:
            print str(e)
            time.sleep(1)
            lastUnix = 0

        saveFile = open(saveFileLine,'a')
        sourceCode = urllib2.urlopen(urlToVisit).read()
        splitSource = sourceCode.split('\n')

        for eachLine in splitSource:
            splitLine = eachLine.split(',')
            if len(splitLine)==6:
                if splitLine[0] > lastUnix:
                    if 'value' not in eachLine:
                        lineToWrite = eachLine+'\n'
                        saveFile.write(lineToWrite)

        saveFile.close()

        print 'Pulled',stock
        print 'sleeping...'
        print str(str(datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')))
        time.sleep(1)


    except Exception,e:
        print 'main loop',str(e)

#获取数据
#while True:
for eachStock in stocksToPull:
    pullData(eachStock)
    #time.sleep(16000)

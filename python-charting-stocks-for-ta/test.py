#encoding:utf-8
import urllib2
import time

#选定股票池
stocksToPull = 'AAPL','GOOG','MSFT','CMG','AMZN','EBAY','TSLA'
#定义获取数据函数
def pullData(stock):
    try:
        fileLine = stock+'.txt'
        urlToVisit = 'https://chartapi.finance.yahoo.com/instrument/1.0/'+stock+'/chartdata;type=quote;range=1y/csv'
        sourceCode = urllib2.urlopen(urlToVisit).read()
        splitSource = sourceCode.split('\n')

        for eachLine in splitSource:
            splitLine = eachLine.split(',')
            if len(splitLine)==6:
                if 'values' not in eachLine:
                    saveFile = open(fileLine,'a')
                    lineToWrite = eachLine+'\n'
                    saveFile.write(lineToWrite)
        #显示进程
        print 'Pulled',stock
        print 'sleeping'
        time.sleep(5)

    except Exception,e:
        print 'main loop',str(e)

#获取数据
for eachStock in stocksToPull:
    pullData(eachStock)
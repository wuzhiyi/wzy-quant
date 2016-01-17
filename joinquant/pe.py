#encoding:utf-8
import pandas as pd
import datetime
# 设置统计数据的时间
begin = datetime.date(2005,1,1)
end = datetime.date(2009,12,31)
d = begin
delta = datetime.timedelta(days=1)
# 设置需要统计的股票代码，这里为47只行业龙头股
stocks = ['000651.XSHE','601318.XSHG','000012.XSHE','002299.XSHE','600150.XSHG','600027.XSHG','600900.XSHG'
                ,'600406.XSHG','600151.XSHG','002241.XSHE','000563.XSHE','000002.XSHE','601668.XSHG','002269.XSHE'
                ,'600019.XSHG','600089.XSHG','600362.XSHG','002005.XSHE','600115.XSHG','601866.XSHG','600352.XSHG'
                ,'600004.XSHG','601186.XSHG','002415.XSHE','002489.XSHE','002340.XSHE','601088.XSHG','000581.XSHE','000625.XSHE'
                ,'600917.XSHG','600415.XSHG','600196.XSHG','600256.XSHG','600887.XSHG','600585.XSHG','601006.XSHG','000063.XSHE'
                ,'300027.XSHE','600456.XSHG','600511.XSHG','600036.XSHG','600519.XSHG','600663.XSHG','600030.XSHG','000538.XSHE'
                ,'600108.XSHG','600655.XSHG']
operate_PEs={}
while d <= end:
    #print d
    q = query(valuation.code,valuation.pe_ratio).filter(valuation.code.in_(stocks))#不同报表只需修改valuation为相应报表名称。
    df = get_fundamentals(q, d)
    df1 = pd.DataFrame(index = df['code'].values)
    df1['pe_ratio']=df['pe_ratio'].values
    df2 = pd.DataFrame(index = stocks)
    df2['pe_ratio'] = 0
    operate_PEs.update({d:(df1+df2)})
    d = d + delta


import pickle
#新建文件
f=file('47longtoustocks_PE_05_09.csv','wb')
#把operate_PE序列化存入文件
pickle.dump(operate_PEs,f)
f.close()
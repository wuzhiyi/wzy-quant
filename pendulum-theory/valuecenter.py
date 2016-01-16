# 导入需要用到的库
from statsmodels import regression
import statsmodels.api as sm
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import numpy as np
import math
from datetime import datetime as dt
from matplotlib.colors import LogNorm
from pylab import *
from mpl_toolkits.mplot3d.axes3d import Axes3D

# 取得股票的价格
start = '2005-01-01'
end = '2015-01-12'
asset = get_price('000423.XSHE', fields='price', start_date=start, end_date=end)#东阿阿胶
asset = asset.dropna()
dates = asset.index

# 画出价格随时间变化的图像
_, ax = plt.subplots()

ax.plot(asset)
ticks = ax.get_xticks()
ax.set_xticklabels([dates[i].date() for i in ticks[:-1]]) # Label x-axis with dates

# 拟合
X = np.arange(len(asset))
x = sm.add_constant(X)
model = regression.linear_model.OLS(asset, x).fit()
a = model.params[0]
b = model.params[1]
Y_hat = X * b + a

#真实值-拟合值，差值最大最小作为价值波动区间
# 向下平移
i = (asset.values.T-Y_hat).argmin()
c_low = X[i] * b + a-asset.values[i]
Y_hatlow = X * b + a-c_low

# 向上平移
i = (asset.values.T-Y_hat).argmax()
c_high = X[i] * b + a-asset.values[i]
Y_hathigh = X * b + a-c_high

plt.plot(X, Y_hat, 'k', alpha=0.9);
plt.plot(X, Y_hatlow, 'r', alpha=0.9);
plt.plot(X, Y_hathigh, 'r', alpha=0.9);
plt.xlabel('Date',fontsize=18)
plt.ylabel('Price',fontsize=18)
plt.title('Value center',fontsize=18)
plt.legend(['000423.XSHE', 'Value center line','Value interval line']);

_, ax = plt.subplots(figsize = [18,8])
ax.plot(asset)
ticks = ax.get_xticks()
ax.set_xticklabels([dates[i].date() for i in ticks[:-1]])
#plt.plot(X, Y_hat, 'k', alpha=0.9)
n = 5
d = (-c_high+c_low)/n
c = c_high
while c<=c_low:
    Y = X * b + a-c
    plt.plot(X, Y, 'r', alpha=0.9);
    c = c+d
plt.xlabel('Date',fontsize=18)
plt.ylabel('Price',fontsize=18)
plt.title('Value center quantile',fontsize=18)
plt.legend(['000423.XSHE', 'Value center line','Quantile line'])

_, ax = plt.subplots(figsize = [18,8])
distance = (asset.values.T-Y_hat)[0]
ax.plot(distance)
ticks = ax.get_xticks()
ax.set_xticklabels([dates[i].date() for i in ticks[:-1]])
n = 5
d = (-c_high+c_low)/n
c = c_high
while c<=c_low:
    Y = X * b + a-c
    plt.plot(X, Y-Y_hat, 'r', alpha=0.9);
    c = c+d
plt.xlabel('Date',fontsize=18)
plt.ylabel('Price-center price',fontsize=18)
plt.title('Value center quantile',fontsize=18)
plt.legend(['000423.XSHE', 'Value center line','Quantile line'])

distance = (asset.values.T-Y_hat)[0]
pd.Series(distance).plot(kind='hist', stacked=True, bins=100)
plt.xlabel('Undervalue ------------------------------------------> Overvalue',fontsize=18)
plt.ylabel('Frequency',fontsize=18)
plt.title('Undervalue & Overvalue Statistical Chart',fontsize=18)

initial = '2005-01-01'
start = '2010-01-01'
end = '2016-01-12'
days = pd.date_range(start,end,freq='1d')
XXX = []
YYY = []
ZZZ = []
#n=bins
n = 100
for i in range(len(days)):
    print i
    end = days[i]
    asset = get_price('000423.XSHE', fields='price', start_date=initial, end_date=end)
    asset = asset.dropna()
    # 拟合
    X = np.arange(len(asset))
    x = sm.add_constant(X)
    model = regression.linear_model.OLS(asset, x).fit()
    a = model.params[0]
    b = model.params[1]
    Y_hat = X * b + a
    distance = (asset.values.T-Y_hat)[0]
    Frequency,value = np.histogram(distance, bins=n)
    YYY .append(value[1:])
    ZZZ .append(Frequency)
for i in range(n):
    XXX.append(range(1,len(days)+1))

fig3d = plt.figure(figsize=(14,10))
ax3d = fig3d.add_subplot(1,1,1, projection='3d')
cmap=matplotlib.cm.jet
ZZZ1 = ZZZ
ZZZ = matrix(ZZZ1)*1.0/matrix(array(ZZZ1).sum(1)).T
p = ax3d.plot_surface(array(XXX),array(YYY).T,array(ZZZ).T,rstride=1, cstride=1,cmap=cmap, linewidth=0,norm=matplotlib.colors.PowerNorm(1), alpha=1)

ax3d.set_xlabel('date',fontsize=18)
ax3d.set_ylabel('Value',fontsize=18)
ax3d.set_zlabel('Frequency',fontsize=18)
ax3d.set_title('Undervalue & Overvalue Statistical Distribution',fontsize=18)
ax3d.set_xticks(range(0,len(days),440))
ax3d.set_xticklabels([str(x)[:4] for x in pd.date_range(start,end,freq='12m')])
ax3d.view_init(55, -120)
ax3d.contour(array(XXX),array(YYY).T,array(ZZZ).T, zdir='z',offset=0.0075, cmap=matplotlib.cm.jet,norm=matplotlib.colors.PowerNorm(1))

ZZZ = matrix(ZZZ1)*1.0/matrix(array(ZZZ1).sum(1)).T
ax = sns.heatmap(ZZZ.T,cmap=cmap)
ax.set_xlabel('date',fontsize=18)
ax.set_ylabel('Undervalue & Overvalue',fontsize=18)
ax.set_title('Statistical Distribution',fontsize=18)
ax.set_yticks(range(0,n,n/10))
ax.set_yticklabels(range(30,-25,-5))
ax.set_xticks(range(0,len(days),400))
ax.set_xticklabels([str(x)[:4] for x in pd.date_range(start,end,freq='12m')])
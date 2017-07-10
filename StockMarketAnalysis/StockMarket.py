from __future__ import unicode_literals
import pandas as pd
import matplotlib as mtl
from matplotlib.dates import DateFormatter,WeekdayLocator,DayLocator,MONDAY, date2num
from matplotlib.finance import candlestick_ohlc,quotes_historical_yahoo_ohlc
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime

__author__ = 'zhaochen'

"""
基于python3的股票分析。数据请自行准备。
"""

def pandas_candlestick2_ohlc(dat,stick = "day", otherseries = None):
    mondays = WeekdayLocator(MONDAY)
    alldays = DayLocator()
    dayformater = DateFormatter('%d')

    transdat = dat.loc[:,['date','open','high','low','close']]
    if type(stick) == str:
        if stick == "day":
            plotdat = transdat
            plotdat['date'] = plotdat['date'].map(lambda x:mtl.dates.date2num(datetime.strptime(x,"%Y/%m/%d")))
        elif stick in ["week","month","year"]:
            if stick == "week":
                transdat["week"] = transdat['date'].map(lambda x: datetime.strptime(x,'%Y/%m/%d').isocalendar()[1])
            elif stick == "month":
                transdat["month"] = transdat['date'].map(lambda x: datetime.strptime(x,'%Y/%m/%d').month)
            transdat["year"] = transdat['date'].map(lambda x: datetime.strptime(x,'%Y/%m/%d').year)
            grouped = transdat.groupby(list(set(["year",stick])))

            plotdat = pd.DataFrame({"date":[],"open":[],"high":[],"low":[],"close":[]})
            for name,group in grouped:
                plotdat = plotdat.append(pd.DataFrame({
                    "date":group.index[0],
                    "open":group.iloc[0,1],
                    "low":min(group.low),
                    "high":max(group.high),
                    "close":group.iloc[-1,3]
                },index = [group.index[0]]))

            if stick == "week":
                stick = 7
            elif stick == "month":
                stick =30
            elif stick == "year":
                stick = 365
    elif type(stick) == int and stick >= 1:
        transdat["date"] = [np.floor(i/stick) for i in range(len(transdat))]
        grouped = transdat.groupby("date")
        plotdat = pd.DataFrame({"date":[],"open": [], "high": [], "low": [], "close": []})
        for name,group in grouped:
            plotdat = plotdat.append(pd.DataFrame({
                                        "date": group.iloc[0,0],
                                        "open": group.iloc[0,1],
                                        "high": max(group.high),
                                        "low": min(group.low),
                                        "close": group.iloc[-1,3]},
                                        index = [group.index[0]]))

    else:
        raise ValueError('Valid inputs to argument "stick" include the strings "day", "week", "month", "year", or a positive integer')

    fig, ax = plt.subplots()
    fig.subplots_adjust(bottom=0.2)
    if plotdat.index[-1] - plotdat.index[0] < pd.Timedelta('730 days').days:
        weekFormatter = DateFormatter('%b %d')  # e.g., Jan 12
        ax.xaxis.set_major_locator(mondays)
        ax.xaxis.set_minor_locator(alldays)
    else:
        weekFormatter = DateFormatter('%b %d, %Y')
    ax.xaxis.set_major_formatter(weekFormatter)

    ax.grid(True)

    # Create the candelstick chart
    candlestick_ohlc(ax,
                     (zip(plotdat['date'].tolist(), plotdat['open'].tolist(), plotdat['high'].tolist(),
                     plotdat['low'].tolist(), plotdat['close'].tolist())),
                      colorup ="blue", colordown = "red")

    # Plot other series (such as moving averages) as lines
    if otherseries != None:
        if type(otherseries) != list:
            otherseries = [otherseries]
        dat.loc[:,otherseries].plot(ax = ax, lw = 1.3, grid = True)

    ax.xaxis_date()
    ax.autoscale_view()
    plt.setp(plt.gca().get_xticklabels(), rotation=45, horizontalalignment='right')
    plt.xlabel("date")
    plt.show()


apple = pd.read_csv(r"C:\Users\bjzhaochen\Desktop\AAPL4.csv")
pandas_candlestick2_ohlc(apple,"day")







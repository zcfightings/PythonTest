from __future__ import unicode_literals
import pandas as pd
from matplotlib.dates import DateFormatter,WeekdayLocator,DayLocator,MONDAY, date2num
from matplotlib.finance import candlestick_ohlc
import matplotlib.pyplot as plt
import numpy as np

__author__ = 'zhaochen'


def pandas_candlestick2_ohlc(dat,stick = "day", otherseries = None):
    mondays = WeekdayLocator(MONDAY)
    alldays = DayLocator()
    dayformater = DateFormatter('%d')

    transdat = dat.loc[:,["open","high","low","close"]]
    if type(stick) == str:
        if stick == "day":
            plotdat = transdat
        elif stick in ["week","month","year"]:
            if stick == "week":
                transdat["week"] = pd.to_datetime(transdat.index).map(lambda x:x.isocalender()[1])
            elif stick == "month":
                transdat["month"] = pd.to_datetime(transdat.index).map(lambda x:x.month)
            transdat["year"] = pd.to_datetime(transdat.index).map(lambda x:x.isocalender()[0])
            grouped = transdat.groupby(list(set(["year",stick])))
            plotdat = pd.DataFrame({"open":[],"high":[],"low":[],"close":[]})

            for name,group in grouped:
                plotdat = plotdat.append(pd.DataFrame({
                    "open":group.iloc[0,0],
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
        transdat["stick"] = [np.floor(i/stick) for i in range(len(transdat.index()))]
        grouped = transdat.groupby("stick")
        plotdat = pd.DataFrame({"Open": [], "High": [], "Low": [], "Close": []}) # Create empty data frame containing what will be plotted
        for name, group in grouped:
            plotdat = plotdat.append(pd.DataFrame({"Open": group.iloc[0,0],
                                        "High": max(group.High),
                                        "Low": min(group.Low),
                                        "Close": group.iloc[-1,3]},
                                        index = [group.index[0]]))

    else:
        raise ValueError('Valid inputs to argument "stick" include the strings "day", "week", "month", "year", or a positive integer')

     # Set plot parameters, including the axis object ax used for plotting
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
    candlestick_ohlc(ax, list(zip(list(date2num(plotdat.index.tolist())), plotdat["open"].tolist(), plotdat["high"].tolist(),
                      plotdat["low"].tolist(), plotdat["close"].tolist())),
                      colorup = "black", colordown = "red", width = stick * .4)

    # Plot other series (such as moving averages) as lines
    if otherseries != None:
        if type(otherseries) != list:
            otherseries = [otherseries]
        dat.loc[:,otherseries].plot(ax = ax, lw = 1.3, grid = True)

    ax.xaxis_date()
    ax.autoscale_view()
    plt.setp(plt.gca().get_xticklabels(), rotation=45, horizontalalignment='right')

    plt.show()


apple = pd.read_excel(r"C:\Users\zhaochen\Desktop\AAPL.xlsx")
pandas_candlestick2_ohlc(apple)







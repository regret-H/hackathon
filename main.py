import mplfinance as mpf
import tushare as ts
import mplfinance as mpf
import pandas as pd# 导入DataFrame数据
import re
import matplotlib.pyplot as plt
import numpy as np
import datetime

def getK(id,ktype):
    stockId = id
    df = ts.get_k_data(stockId,ktype=ktype,start='2019-01-15',end='2022-08-15')
    # print(df.columns)
    df.rename(
                columns={
                'date': 'Date', 'open': 'Open',
                'high': 'High', 'low': 'Low',
                'close': 'Close', 'volume': 'Volume'},
                inplace=True)
    df['Date'] = pd.to_datetime(df['Date'])
    df.set_index(['Date'], inplace=True)
    print(df[0:10])
    # print(df)

    mycolor=mpf.make_marketcolors(up="red",down="green",edge="i",wick="i",volume="in")
    mystyle=mpf.make_mpf_style(marketcolors=mycolor,gridaxis="both",gridstyle="-.")
    mpf.plot(df,type="line",mav=(5,10,20),style=mystyle,volume=True,show_nontrading=False,savefig='pic/%s_Stock_of_%s_candle_line.jpg'%(ktype,stockId))#
    plt.show()

def dataFormat(time):
    time = str(time)
    return time[0:4]+'/'+time[4:6]+'/'+time[6:8]
def showK():
    stockId = '000002.SZ'
    ktype = "D"
    pattern = re.compile(r'^\d{6}\.(SZ)|(SH)$')
    if (pattern.search(stockId) == None):
        return "input error"
    names = ['stockCode', 'Date', 'Open', 'High', 'Low', 'Close', 'yesterdayPrice',
             'gap', 'gapRate', 'Volume', 'tradeAmountPrice']
    tmp = pd.read_excel("allstock/" + str(stockId) + ".xls", names=names)
    stock = tmp.loc[:,['Date','Open','High','Low','Close','Volume']]

    stock['Date'] = stock['Date'].apply(lambda x:dataFormat(x))#时间格式化
    stock['Date'] = pd.to_datetime(stock['Date'],format="%Y/%m/%d")
    stock.set_index(['Date'], inplace=True)
    print(stock)
    mycolor = mpf.make_marketcolors(up="red", down="green", edge="i", wick="i", volume="in")
    mystyle = mpf.make_mpf_style(marketcolors=mycolor, gridaxis="both", gridstyle="-.")
    # print(stock['Date'])
    mpf.plot(stock, type="line", mav=(5, 10, 20), style=mystyle, volume=True, show_nontrading=False)  #
    # plt.show()
    # try:
    #     stock = pd.read_excel("allstock/" + str(stockId) + ".xls", names=names)
    #     stock['Date'] = pd.to_datetime(str(stock['Date']))
    #     # print(pd.to_datetime('20221101'))
    #     stock.set_index(['Date'], inplace=True)
    #     # print(df)
    #     print(stock[0:10])
    #
    #     mycolor = mpf.make_marketcolors(up="red", down="green", edge="i", wick="i", volume="in")
    #     mystyle = mpf.make_mpf_style(marketcolors=mycolor, gridaxis="both", gridstyle="-.")
    #     mpf.plot(stock, type="line", mav=(5, 10, 20), style=mystyle, volume=True, show_nontrading=False)  #
    #     plt.show()
    # except:
    #     return "Sorry,no such file or directory"
if __name__ == '__main__':
    # getK('000001','W')
    # showK()
    stockId = '000001.SZ'
    # print(ts.get_k_data('600000',start='2019-01-15',ktype='D', end='2022-08-15'))
# 设置基本参数

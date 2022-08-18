# -*- coding: utf-8 -*-
import numpy as np
import json
import pandas as pd
import flask
from flask import Flask,request
from flask_cors import CORS
import re
from flask import send_file
from flask import render_template
from manage import stock_an

server = flask.Flask(__name__)  # 实例化server，把当前这个python文件当做一个服务，__name__代表当前这个python文件
# r'/*' 是通配符，让本服务器所有的URL 都允许跨域请求
CORS(server, resources=r'/*')


class MyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        else:
            return super(MyEncoder, self).default(obj)
@server.route('/getStockById', methods=['POST'])
def getStockById():
    if  request.method == 'POST':
        print("data:")
        stockId = request.form["id"]
        pattern = re.compile(r'^\d{6}\.(SZ)|(SH)$')
        if(pattern.search(stockId)==None):
            return "input error"
        names = ['stockCode', 'tradeCode', 'startPrice', 'highestPrice', 'lowestPrice', 'closePrice', 'yesterdayPrice',
                 'gap', 'gapRate', 'tradeAmount', 'tradeAmountPrice']
        try:
            stock = pd.read_excel("allstock/"+str(stockId)+".xls", names=names)
            return stock.to_json(orient="index", force_ascii=False)
        except:
            return "Sorry,no such file or directory"
@server.route('/addStock', methods=['POST'])
def addStock():
    if  request.method == 'POST':
        print("data:")
        userId = request.form["userId"]
        stockIds = request.form.getlist("stockIds")
        nums = request.form.getlist("nums")
        print(request.form)
        print(userId)
        print(stockIds)
        print(nums)
        try:
            result = stock_an(stockIds,nums)
        except:
            return "input error"
        return json.dumps(result,cls=MyEncoder)
        # pattern = re.compile(r'^\d{6}\.(SZ)|(SH)$')
        # if(pattern.search(stockId)==None):
        #     return "input error"
        # names = ['stockCode', 'tradeCode', 'startPrice', 'highestPrice', 'lowestPrice', 'closePrice', 'yesterdayPrice',
        #          'gap', 'gapRate', 'tradeAmount', 'tradeAmountPrice']
        #
        # try:
        #     stock = pd.read_excel("allstock/"+str(stockId)+".xls", names=names)
        #     return stock.to_json(orient="index", force_ascii=False)
        # except:
        #     return "Sorry,no such file or directory"
@server.route('/pic',methods = ['GET'])
def returnPictureExample():
    print(request.args.get('stockId'))
    ktype = request.args.get('ktype')#D,W,M
    print(ktype)
    return send_file('pic/%s_Stock_of_000001_candle_line.jpg'%ktype, mimetype='image/gif')


@server.route('/')
def index():
    stockId = request.args.get('stockId')
    print(stockId)
    return render_template('index.html',stockId=stockId)

@server.route('/showP')
def showP():
    return render_template('showP.html')

@server.route('/getData')
def getData():
    stockId = request.args.get('stockId')
    print(stockId)
    names = ['stockCode', 'Date', 'Open', 'High', 'Low', 'Close', 'yesterdayPrice', 'gap', 'gapRate', 'Volume',
             'tradeAmountPrice']
    tmp = pd.read_excel("allstock/" + str(stockId) + ".xls", names=names)
    stock = tmp.loc[:, ['Date', 'Open', 'Close', 'Low', 'High']]
    stock['Date'] = stock['Date'].apply(lambda x: dataFormat(x))  # 时间格式化
    # print(stock.values[0:10])
    # print(stock.to_json(orient="values"))
    return stock.to_json(orient="values")

def dataFormat(time):
    time = str(time)
    return time[0:4]+'/'+time[4:6]+'/'+time[6:8]
# @server.route('/test',methods = ['GET'])
# def getStockData():


if __name__ == '__main__':
    server.run(debug=True)# 启动服务



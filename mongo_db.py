from pymongo import MongoClient
import os
import re
import pandas as pd
import json
import xlrd

client = MongoClient()
Stocks = client.Stocks

testinsert = {"author": "Maxsu",
              "text": "My test stock",
              "date": "8/17/2022 11:58AM"}


def xls_filter(f):
    if f[-3:] in ['xls']:
        return True
    else:
        return False


def read_xlsx_file(filename):
    data = xlrd.open_workbook(filename)
    table = data.sheets()[0]
    rows = table.nrows
    data = []
    for i in range(1, rows):
        values = table.row_values(i)
        data.append(
            (
                {
                    "index": int(i),
                    "stockCode": str(values[0]),
                    "tradeCode": values[1],
                    "startPrice": float(values[2]),
                    "highestPrice": float(values[3]),
                    "lowestPrice": float(values[4]),
                    "closePrice": float(values[5]),
                    "yesterdayPrice": float(values[6]),
                    "gap": float(values[7]),
                    "gapRate": float(values[8]),
                    "tradeAmount": float(values[9]),
                    "tradeAmountPrice": float(values[10])
                }
            )
        )
    return data


files = os.listdir('allstock')
files = list(filter(xls_filter, files))

# print(files)

# 设置列名
names = ['stockCode', 'tradeCode', 'startPrice', 'highestPrice', 'lowestPrice', 'closePrice', 'yesterdayPrice', 'gap',
         'gapRate', 'tradeAmount', 'tradeAmountPrice']
pattern = re.compile(r'^\d{6}\.((SZ)|(SH))')
for file in files:
    print(file)
    file_id = pattern.search(file)[0]  # 提取股票id
    # stock = pd.read_excel("allstock/"+file, names=names)
    # s_json = stock.to_json(orient="index", force_ascii=False)#转换成json格式
    d1 = read_xlsx_file("allstock/" + file)
    js = json.dumps(d1, sort_keys=True, ensure_ascii=False, indent=4, separators=(',', ':'))
    # print(js)
    f = open("jsonstock/" + file_id + ".json", 'w')
    f.write(js)
    f.close()


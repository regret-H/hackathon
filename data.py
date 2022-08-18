import os
import re
import pandas as pd
import json

files = os.listdir('allstock')
# print(files)

#设置列名
names = ['stockCode','tradeCode','startPrice','highestPrice','lowestPrice','closePrice','yesterdayPrice','gap','gapRate','tradeAmount','tradeAmountPrice']
pattern = re.compile(r'^\d{6}\.((SZ)|(SH))')
for file in files[0]:
    print(file)
    file_id = pattern.search(file)[0]#提取股票id

    stock = pd.read_excel("allstock/"+file, names=names)
    s_json = stock.to_json(orient="index", force_ascii=False)#转换成json格式
    print(json.loads(s_json)['0'])

    # f = open("stock/"+file_id+".txt", 'w')
    # f.write(str(s_json))
    # f.close()

    # f = open('S1.txt', 'r')
    # dict_s = eval(f.read())
    # print(dict_s)
    # f.close()




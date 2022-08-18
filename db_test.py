from pymongo import MongoClient
import os
import re
import pandas as pd
import json

client = MongoClient()
Stocks = client.Stocks

# files = os.listdir('jsonstock')
# #files = files[:4]
#
# pattern = re.compile(r'^\d{6}\.((SZ)|(SH))')
# for file in files:
#     print(file)
#     file_id = pattern.search(file)[0]#提取股票id
#     filename=file_id.replace(".",'')
#     collection = Stocks[filename]
#     with open("jsonstock/"+file_id+".json","r",encoding="utf-8") as f:
#         json_data=json.load(f)
#         collection.insert_many(json_data)




myquery = {"gap":-0.51}

find01 = Stocks['300856SZ']
print(find01)
# 开始请求，首先导入使用的包，使用request进行网页请求，使用pandas保存数据。
import requests
import pandas as pd
import time 
import json
pd.set_option('display.max_rows',600)
# 设置请求头，伪装为浏览器
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'
}
url = 'https://c.m.163.com/ug/api/wuhan/app/data/list-total'   # 定义要访问的地址 这里选择网易实时疫情播报平台
r = requests.get(url, headers=headers)  # 使用requests发起请求

# 查看请求结果
# print(r.status_code)  # 查看请求状态 200
# print(type(r.text)) #数据类型 str
# print(len(r.text)) #数据长度 311533

data_json = json.loads(r.text) # 将数据转化为便于分析的json格式
# print(data_json) # 查看结果
# print(data_json.keys()) # 查看json数据的键值 进一步剖析数据
data = data_json['data'] # 取出json中的数据/世界,中国各地疫情消息
# print(data.keys()) # 查看键值 进一步剖析数据


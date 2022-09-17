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

# 开始提取目标数据
data_province = data['areaTree'][2]['children']  # 取出中国各省的实时数据
# print(type(data_province)) # list
# print(data_province[0].keys()) # 查看每个省键名称 /需要today里的数据即每日新增确诊 其中extData里的数据即无症状感染者
for i in range(len(data_province)): # 遍历查看各省名称、更新时间/此例为5
    print(data_province[i]['name'],data_province[i]['lastUpdateTime'])
    if i == 5:
        break
# 用DataFrame以字典格式生成数据的例子，传入一个列表，列表每一个元素都是字典
test_dict = [ {'a':1,'b':2,'c':3,},
              {'a':111,'b':222} ]
# 以下对数据的查看不在赘述"print"
pd.DataFrame(test_dict)
pd.DataFrame(data_province).head() # 直接生成数据效果并不理想
# 获取id、lastUpdateTime、name
info = pd.DataFrame(data_province)[['id','lastUpdateTime','name']]
info.head()

# 列表推导式例子
l1 = [1,1,1,2,2,2]
[i+1 for i in l1 ]     

# 获取today中的数据
today_data = pd.DataFrame([province['today'] for province in data_province ]) 
today_data.head()
['today_'+i for i in today_data.columns] # 用上述推导方式命名提取的数据名字
today_data.columns = ['today_'+i for i in today_data.columns] # 由于today中键名和total键名相同，因此需要修改列名称
today_data.head()

# 同理获取total数据
total_data = pd.DataFrame([province['total'] for province in data_province ])
total_data.columns = ['total_'+i for i in total_data.columns]
total_data.head()
pd.concat([info,total_data,today_data],axis=1).head() # 将三个数据合并

# 将提取数据的方法封装为函数
def get_data(data,info_list):
    info = pd.DataFrame(data)[info_list] # 主要信息
    
    today_data = pd.DataFrame([i['today'] for i in data ]) # 生成today的数据
    today_data.columns = ['today_'+i for i in today_data.columns] # 修改列名
    
    total_data = pd.DataFrame([i['total'] for i in data ]) # 生成total的数据
    total_data.columns = ['total_'+i for i in total_data.columns] # 修改列名
    
    return pd.concat([info,total_data,today_data],axis=1) # info、today和total横向合并最终得到汇总的数据

today_province = get_data(data_province,['id','lastUpdateTime','name'])
print(today_province)
def save_data(data,name): # 定义保存数据方法
    file_name = name+'_'+time.strftime('%Y_%m_%d',time.localtime(time.time()))+'.csv'
    data.to_csv(file_name,index=None,encoding='utf_8_sig')
    print(file_name+' 保存成功！')

time.strftime('%Y_%m_%d',time.localtime(time.time())) # 查询当天时间

#save_data(today_province,'today_province') # 保存数据/各省实时数据

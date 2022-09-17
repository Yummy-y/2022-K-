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
# print(today_province)
def save_data(data,name): # 定义保存数据方法
    file_name = name+'_'+time.strftime('%Y_%m_%d',time.localtime(time.time()))+'.csv'
    data.to_csv(file_name,index=None,encoding='utf_8_sig')
    print(file_name+' 保存成功！')

time.strftime('%Y_%m_%d',time.localtime(time.time())) # 查询当天时间

#save_data(today_province,'today_province') # 保存数据/各省实时数据

# 输出全国历史数据

chinaDayList = data['chinaDayList'] # 取出chinaDayList
type(chinaDayList) # 查看chinaDayList的格式
# chinaDayList[0] # 当天数据
alltime_China = get_data(chinaDayList,['date','lastUpdateTime'])
alltime_China.head()
save_data(alltime_China,'alltime_China')

# 输出全国各省历史数据

url = 'https://c.m.163.com/ug/api/wuhan/app/data/list-by-area-code?areaCode=420000' # 定义数据地址
r = requests.get(url, headers=headers) # 进行请求
data_json = json.loads(r.text) # 获取json数据

data_json.keys()
data_json['data']['list'][0]
data_test = get_data(data_json['data']['list'],['date'])
data_test['name'] = '湖北省'
data_test.head()
today_province[['id','name']].head()
a = ['1','2','3','4']
b = ['q','w','e','r']

# for i,j in zip(a, b):
#     print(i,j)

{ i:j  for i,j in zip(a, b)}
province_dict = {num:name for num,name in zip(today_province['id'],today_province['name'])}

# 查看前五个内容
# count = 0
# for i in province_dict:
#     print(i,province_dict[i])
#     count += 1
#     if count == 5:
#         break

df1 = pd.DataFrame([{'a':1,'b':2,'c':3,},{'a':111,'b':222}])
df2 = pd.DataFrame([{'a':9,'b':8,'c':7,},{'a':345,'c':789}])
# 合并
df1 = pd.concat([df1,df2],axis=0)
# df1

# 总结上述方法
start = time.time()
for province_id in province_dict: # 遍历各省编号
    
    try:
        # 按照省编号访问每个省的数据地址，并获取json数据
        url = 'https://c.m.163.com/ug/api/wuhan/app/data/list-by-area-code?areaCode='+province_id
        r = requests.get(url, headers=headers)
        data_json = json.loads(r.text)
        
        # 提取各省数据，然后写入各省名称
        province_data = get_data(data_json['data']['list'],['date'])
        province_data['name'] = province_dict[province_id]
        
        # 合并数据
        if province_id == '420000':
            alltime_province = province_data
        else:
            alltime_province = pd.concat([alltime_province,province_data])

        save_data(alltime_province,'alltime_province')

            
            # print('-'*20,province_dict[province_id],'成功',
            #       province_data.shape,alltime_province.shape,
            #       ',累计耗时:',round(time.time()-start),'-'*20)
        
        # 设置延迟等待
        time.sleep(10)
        
    except:
        print('-'*20,province_dict[province_id],'wrong','-'*20)

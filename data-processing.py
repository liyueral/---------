import numpy as np
import pandas as pd
import matplotlib.pyplot as mp

df = pd.read_csv('gas.csv',names=['id',
                                  'cd',
                                  'baseprice',
                                  'basenum',
                                  'contprice',
                                  'dealnum',
                                  'orderdate',
                                  'jsd',
                                  'enddate'])

# print(df.shape)
# 将少量含空值去除
df1 = df.dropna()
df1 = df1.drop('enddate',axis=1)

# 规整交易地区名称
df1 = df1.replace(['.*中海油浙江宁波.*','.*广东.*',
                   '.*珠海.*','.*中海油粤东.*',
                   '.*中海油海南.*','.*中石化北海.*',
                   '.*中海油天津.*','.*中海油福建.*',
                   '.*陕西.*'] , ['中海油宁波江浙沪皖',
                                    '珠三角地区',
                                    '珠三角地区',
                                    '中海油粤东',
                                    '中海油海南',
                                    '中石化北海',
                                    '中海油天津',
                                    '中海油福建',
                                    '西部'],regex=True)
# print(df1.shape)
# 重定义字段数据类型
df1.astype(dtype={'id':int,
                  'cd':int,
                  'baseprice':float,
                  'basenum':float,
                  'contprice':float,
                  'dealnum':float,
                  'orderdate':object,
                  'jsd':str
                  },copy=True)
# print(df1.dtypes)
# df1_baseprice = df1['baseprice']
# df1_basenum = df1['basenum']
# df1_contprice = df1['contprice']
# df1_dealnum = df1['dealnum']

# 按挂牌日期和所属地区(cd)降序排列
df2 = df1.sort_values(by=['orderdate','cd'],ascending=False)

# 生成交易额新列 单位万元
df2.eval('volume = contprice * dealnum / 10000',inplace=True)
# print(df2)

# 只取出挂牌日期、交易地区(cd，1表示华东、2表示华北、3表示华南、4表示华中
# 5表示西南、6表示西北、7表示东北)、交易量、交易额
df3 = df2[['orderdate','cd','dealnum','volume']]
# print(df3)
# data = np.array(df2)
# print(data[0])

# 构键年索引列表
# L = list(df3['orderdate'])
# L = [i[:4] for i in list(df3['orderdate'])]

# 构键月索引列表
# L = list(df3['orderdate'])
# L = [i[:7] for i in list(df3['orderdate'])]

# 将交易量、交易额拿出来，用挂牌日期和交易地点做等级索引
# 直接用选出来的列不可以，需要先转化为numpy数组，且等级索引传参为列表，需要list转换一下
# 此处直接用列表推导式得到年、月索引列表
df4 = pd.DataFrame(np.array(df3[['dealnum','volume']]),
                   index=[[i[:4] for i in list(df3['orderdate'])],
                          [i[:7] for i in list(df3['orderdate'])],
                          list(df3['orderdate']),list(df3['cd'])],
                   columns=['dealnum','volume'])

# dfm = pd.DataFrame(np.array(df3[['dealnum','volume']]),
#                    index=[list(df3['orderdate']),list(df3['cd'])],
#                    columns=['dealnum','volume'])

# 重新指定行列名
df4.columns.names = ['object']
df4.index.names = ['year','month','orderdate','cd']
print(df4)

# 按层求和 年、月、日期、地区
df_y = df4.sum(level='year')
df_m = df4.sum(level='month')
df_d = df4.sum(level='orderdate')

df_y_o = df4.sum(level=['year','cd'])
df_m_o = df4.sum(level=['month','cd'])
df_d_o = df4.sum(level=['orderdate','cd'])

df_c = df4.sum(level='cd')
# print(df_y)
# print(df_m)
# print(df_d)
# print(df_y_o)
# print(df_y_o.sort_index(by=['year','cd'])['dealnum'])
# print(df_y_o['dealnum'].unstack())
# print(list(df_y_o['dealnum']))
# print(df_y_o.index[la])
print(df_m_o)
# print(df_d_o)
# print(df_c)

# 画图
# 中文显示
mp.rcParams['font.sans-serif'] = ['SimHei'] # 显示中文
mp.rcParams['axes.unicode_minus'] = False # 显示负号
# 1.画各年份各地区交易量 、交易额
mp.figure("各年份-地区交易量",facecolor='lightgray')
mp.title("各年份-地区交易量",fontsize=20)
mp.xlabel("年份",fontsize=14)
mp.ylabel("交易量(吨)",fontsize=14)
mp.tick_params(labelsize=10)
mp.grid(axis='y',linestyle=':')

# data=list(df_y_o.sort_index(by=['year','cd'])['dealnum'])
# 获取交易量数组，将series转化为dataframe，再转化为numpy数组
df_y_o_np = np.array(df_y_o['dealnum'].unstack())
# print(df_y_o_np)
# print(df_y_o_np[:,0])
# df_y_o = pd.Series(data=df_y_o_np,
#                    index=['2015','2016','2017','2018'],
#                    columns=['华东','华北','华南','西北'])
x = np.arange(len(df_y))
mp.bar(x,df_y_o_np[:,0],0.2,color='orangered',label='华东',alpha=0.75)
mp.bar(x + 0.2,df_y_o_np[:,1],0.2,color='blue',label='华北')
mp.bar(x + 0.4,df_y_o_np[:,2],0.2,color='red',label='华南')
mp.bar(x + 0.6,df_y_o_np[:,3],0.2,color='yellow',label='西北')
mp.xticks(x + 0.2,['2015','2016','2017','2018'])
for i in range(4):
    for a,b in zip(x + i*0.2,df_y_o_np[:,i]):
        mp.text(a,b+1,'%.0f' % b,ha='center',va='bottom')
mp.legend()

# 画月份交易图
mp.figure("月份-地区交易量",facecolor='lightgray')
mp.title("月份-地区交易量",fontsize=20)
mp.xlabel("月份",fontsize=14)
mp.ylabel("交易量(吨)",fontsize=14)
mp.tick_params(labelsize=10)
mp.grid(axis='y',linestyle=':')

df_m_o_np = np.array(df_m_o['dealnum'].unstack())
# print(df_m_o['dealnum'])
# 发现2017年10月11月 缺失了 将其补上  numpy数组添加行比较方便,因此没在dataframe数据类型中添加
df_m_o_np = np.insert(df_m_o_np,27,np.zeros((2,4)),axis=0)
# print(df_m_o_np)
# print(len(df_m))
x = np.arange(len(df_m)+2) # 由于添加了缺失的2017年10月和11月两个月,所以需要加2
mp.bar(x,df_m_o_np[:,0],0.2,color='green',label='华东',alpha=0.75)
mp.bar(x + 0.2,df_m_o_np[:,1],0.2,color='blue',label='华北')
mp.bar(x + 0.4,df_m_o_np[:,2],0.2,color='red',label='华南')
mp.bar(x + 0.6,df_m_o_np[:,3],0.2,color='yellow',label='西北')
list_m = sorted(list(df_m.index))
mp.xticks([0,6,12,18,24,30,36],['2015/7','2016/1','2016/7','2017/1','2017/7','2018/1','2018/7'])

mp.legend()
mp.show()

#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
# get_ipython().run_line_magic('matplotlib', 'inline')

plt.rcParams['font.sans-serif'] = ['SimHei']  # 显示中文
plt.rcParams['axes.unicode_minus'] = False  # 显示负号


# In[2]:


data_g = pd.read_csv('./gas_deal.csv')
data_g.head()


# In[3]:


data_g.info()


# In[4]:


data_g.describe()


# In[5]:


data_g['orderdate'] = pd.to_datetime(data_g.orderdate,format='%Y-%m-%d')
data_g = data_g.set_index('orderdate')
data_g.head()


# In[6]:


price = data_g.groupby([data_g.index,'cd'])['contprice'].sum()/data_g.groupby([data_g.index,'cd'])['contprice'].count()
prices = price.unstack()
prices.plot(figsize=(30,15))
plt.title('各地区交易均价走势',fontsize=25)
plt.xlabel('时间',fontsize=20)
plt.ylabel('元/吨',fontsize=20)
plt.grid(linestyle=':')
plt.tick_params(labelsize=20)
plt.legend(['华东','华北','华南','西北'],fontsize=20,loc='best',frameon=False)


# In[7]:


plt.figure(figsize=(10, 6))
data_a = data_g.groupby('cd')['trans-amount'].sum().sort_values(ascending=False)
labels = data_a.rename(index={1:'华东',2:'华北',3:'华南',6:'西北'}).index
colors = ['tomato','sandybrown', 'deepskyblue', 'limegreen']
patches, l_text, p_text = plt.pie(
    data_a,
    labels=labels,
    colors=colors,
    explode=(0.08, 0.08,0,0),
    autopct='%4.2f%%',
    startangle=90,
    shadow=True,
    pctdistance=0.8)

for t in l_text + p_text:
    t.set_size(20)
for t in p_text:
    t.set_color('black')
plt.legend(
    fontsize=15, loc='best', title='各地区交易额占比', frameon=False)
plt.axis('equal')


# In[8]:


plt.figure(figsize=(10, 6))
data_y_n = data_g.resample('Y')['dealnum'].sum().sort_values(ascending=False)

labels = []
for index in data_y_n.index:
    labels.append(str(index)[:4])

colors = ['tomato','sandybrown', 'deepskyblue', 'limegreen']
patches, l_text, p_text = plt.pie(
    data_y_n,
    labels=labels,
    colors=colors,
    explode=(0.08, 0.08,0,0),
    autopct='%4.2f%%',
    startangle=90,
    shadow=True,
    pctdistance=0.7)

for t in l_text + p_text:
    t.set_size(20)
for t in p_text:
    t.set_color('black')
plt.legend(
    fontsize=15, loc='best', title='各年份交易量占比', frameon=False)
plt.axis('equal')


# In[9]:


plt.figure(figsize=(10, 6))
data_y_a = data_g.resample('Y')['trans-amount'].sum().sort_values(ascending=False)

labels = []
for index in data_y_a.index:
    labels.append(str(index)[:4])

colors = ['tomato','sandybrown', 'deepskyblue', 'limegreen']
patches, l_text, p_text = plt.pie(
    data_y_a,
    labels=labels,
    colors=colors,
    explode=(0.08, 0.08,0,0),
    autopct='%4.2f%%',
    startangle=90,
    shadow=True,
    pctdistance=0.7)

for t in l_text + p_text:
    t.set_size(20)
for t in p_text:
    t.set_color('black')
plt.legend(
    fontsize=15, loc='best', title='各年份交易额占比', frameon=False)
plt.axis('equal')


# In[10]:


plt.figure(figsize=(30,10))
data_N_A = data_g.resample('M')[['dealnum','trans-amount']].sum()
data_N_A['dealnum'].plot()
(data_N_A['trans-amount']/10000).plot()
plt.title('交易趋势图',fontsize=25)
plt.xlabel('时间',fontsize=20)
plt.ylabel('数量',fontsize=20)
plt.grid(linestyle=':')
plt.tick_params(labelsize=20)
plt.legend(['交易量--吨','交易额--万元'],fontsize=20,loc='best',frameon=False)


# In[11]:


data_1 = data_g[data_g['cd']==1].resample('M')['dealnum'].sum().fillna(0)
data_2 = data_g[data_g['cd']==2].resample('M')['dealnum'].sum().fillna(0)
data_3 = data_g[data_g['cd']==3].resample('M')['dealnum'].sum().fillna(0)
data_6 = data_g[data_g['cd']==6].resample('M')['dealnum'].sum().fillna(0)
data_cd = pd.DataFrame({'华东':data_1,'华北':data_2,'华南':data_3,'西北':data_6})
data_cd.plot.bar(figsize=(30,10))
plt.title('各地区每月交易量',fontsize='25')
plt.xlabel('月份',fontsize=20)
plt.ylabel('交易量/吨',fontsize=20)

data_index = []
for index in data_cd.index:
    data_index.append(str(index)[:7])
data_index
ax = plt.gca()
ax.set_xticklabels(data_index,fontsize=15,rotation=45,horizontalalignment='right')
plt.legend(data_cd.columns,fontsize=20,loc='best',frameon=False)
plt.grid(axis='y',linestyle = ':')


# In[12]:


data_1 = data_g[data_g['cd']==1].resample('M')['trans-amount'].sum().fillna(0)/10000
data_2 = data_g[data_g['cd']==2].resample('M')['trans-amount'].sum().fillna(0)/10000
data_3 = data_g[data_g['cd']==3].resample('M')['trans-amount'].sum().fillna(0)/10000
data_6 = data_g[data_g['cd']==6].resample('M')['trans-amount'].sum().fillna(0)/10000
data_cd = pd.DataFrame({'华东':data_1,'华北':data_2,'华南':data_3,'西北':data_6})
data_cd.plot.bar(figsize=(30,10))
plt.title('各地区每月交易额',fontsize='25')
plt.xlabel('月份',fontsize=20)
plt.ylabel('交易额（万元）',fontsize=20)

data_index = []
for index in data_cd.index:
    data_index.append(str(index)[:7])
data_index
ax = plt.gca()
ax.set_xticklabels(data_index,fontsize=15,rotation=45,horizontalalignment='right')
plt.legend(data_cd.columns,fontsize=20,loc='best',frameon=False)
plt.grid(axis='y',linestyle= ':')

plt.show()
# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





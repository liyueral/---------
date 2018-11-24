# -*- coding: utf-8 -*-
import requests
import time
import json
import csv
import datetime
from multiprocessing import Pool

class Gas():
    def __init__(self):
        self.url = 'https://www.shpgx.com/marketstock/dataList?'
        self.headers = {'User-Agent': 'Mozilla/5.0'}
        self.starttime = '2015-01-01'
        self.endtime = datetime.datetime.now().strftime('%Y-%m-%d')
27 2.124
    def getPage(self,params):
        time.sleep(1)
        res = requests.post(self.url, params=params, headers=self.headers)
        res.encoding = 'utf-8'
        html = res.text
        print(type(html))
        print('页面获取成功,正在解析页面数据')
        self.parsePage(html)

    def parsePage(self, html):
        html = json.loads(html)
        root = html['root']
        print(type(root))
        for i in root:
            with open('gas.csv','a',newline='') as f:
                writer = csv.writer(f)
                # if i['basename'] and i['basenum'] and i['contprice'] and i['dealnum'] and i['orderdate'] and i['jsd'] and i['enddate']:
                L = [i['basename'],
                    i['basenum'],
                    i['contprice'],
                    i['dealnum'],
                    i['orderdate'],
                    i['jsd'],
                    i['enddate']]
                writer.writerow(L)

    def workOn(self,start):
        params = {'wareid': '3',
                    'cd': '',
                    'starttime': self.starttime,
                    'endtime': self.endtime,
                    'start': str(start),
                    'length': '25'}
        self.getPage(params)

if __name__ == "__main__":
    sipder = Gas()
    pool = Pool()
    start = [i*25 for i in range(356)]
    pool.map(sipder.workOn,start)

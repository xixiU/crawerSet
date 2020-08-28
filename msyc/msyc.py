# -*- coding: utf-8 -*-
"""
Created on Sat Dec  1 11:21:55 2018

@author: x
xixi_comeon
@describe: 洋葱乐购签单
"""


import requests
from pandas import DataFrame as df

from openpyxl import Workbook
from openpyxl import load_workbook

from bs4 import BeautifulSoup
import urllib.request
import json 
import pickle as pl
import os,time
from datetime import datetime
import sys
import time
import csv

headers_lmbda = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36 MicroMessenger/6.5.2.501 NetType/WIFI WindowsWechat QBCore/3.43.691.400 QQBrowser/9.0.2524.400',
    'X-Requested-With':'XMLHttpRequest',
    'Accept': 'application/json',
    'Accept-Language': 'zh-CN,zh;q=0.8,en-us;q=0.6,en;q=0.5;q=0.4',
    'Accept-Encoding': 'gzip, deflate',
    'Connection': 'keep-alive',
    'Host': 'm.msyc.cc',
    #'Content-Length': '239',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Cookie': 'JSESSIONID=28231DB1161B9BAD70A64EB7DF11F736; Hm_lvt_990d71bc0417b5322e54113b10d1913b=1543634247; Hm_lpvt_990d71bc0417b5322e54113b10d1913b=%d'%(int(time.time())),
    'Origin': 'https://m.msyc.cc',
    'Referer': 'https://m.msyc.cc/wx/ucenter/cart-order-sumbit.html?tmn=277481',
}

    
class msyc:
    def __init__(self,):
        self.headers = headers_lmbda#一次生成
        self.login_url='https://m.msyc.cc/user/login/v1'
        self.url='https://m.msyc.cc/salesPromotionRest/getCartPrice/v666'
        self.ordel_url='https://m.msyc.cc/app/sodrest/checkQty'
        self.pay_url='https://m.msyc.cc/cart/getCartByCardIds/v2'
        self.data_string = lambda x,y=1:{'cartIds':'{"foreignList":[],"onionList":["id":"%d","count":"%d"],"wineFirstList":[],"freshList":[]}'%(x,y)}
        self.pust_data = lambda x,y=1:{'cartIds':'{"foreignList":[],"onionList":[{"id":"%d","count":"%d"}],"wineFirstList":[],"freshList":[]}'%(x,y),'discountAmt':20,'isSingle':0,'couponNo':'5041129459340322','addressId':0}
        self.create_order_url='https://m.msyc.cc/app/sodrest/createSod/v2?t=%d'%(int(time.time()))
        self.cerate_data = lambda x,y=1:{'client':'web','tmnId':'277481','addressId':'2172238','cartIds':'{"foreignList":[],"onionList":[{"id":"%d","count":"%d"}],"wineFirstList":[],"freshList":[]}'%(x,y),'discountAmt':20,'isSingle':0,'couponNo':'5041129459340322'}
        self.dubug_filename='session.pl'
        self.session = requests.Session()

    def debug(self):
        with open(self.dubug_filename,'rb') as f_r:
            session = pl.load(f_r)
        print(session.headers)        
        print(print(session.cookies.get_dict()))

    def sign_in(self):
        """
        签到  
        """
        sign_url='https://m.msyc.cc/wx/ucenter/signin.html?tmn=277481'
        m_header = self.headers

        m_header['Referer']='https://m.msyc.cc/wx/ucenter/members.html?tmn=277481'
        info= self.session.get(sign_url,headers=self.headers)
        print(info.text)

    def login(self,username='xxx',password='xx'):
        if not os.path.exists(self.dubug_filename):
            post_data={'client':'WEB','loginName':username,'passWord':password,'returnUrl':'https://m.msyc.cc/wx/ucenter/members.html?tmn=1','tmn':'1'}
            info = self.session.post(self.login_url,headers=self.headers,data=post_data,verify=False)
            print(info.status_code)
            print(info.text)
            #with open(self.dubug_filename,'wb') as f_w:
            #    pl.dump(self.session,f_w)
        else:
            with open(self.dubug_filename,'rb') as f_r:
                self.session=pl.load(f_r)
        self.sign_in()
    def get_soup(self):
#        info = self.session.get(question_url,headers=headers,verify=False)#
#        if info.status_code !=200:
#            print('error')
#            sys.exit()
##        print(response.info())
        try:
            #response = urllib.request.urlopen(url,data=bytes(json.dumps(headers), encoding="utf-8"))
            # parpare = self.session.get(url='https://www.icourse163.org/course/BIT-268001',headers=headers)
            # print(parpare.status_code)
            #info = self.session.post(self.pay_url,headers=headers,data=self.pust_data(635,2),verify=False)#,verify=False
            info = self.session.post(self.create_order_url,headers=self.headers,data=self.cerate_data(2060,2),verify=False)#,verify=False
            #create_order_url
            data = json.loads(info.content)
            print(data)
            return data
        except urllib.error.HTTPError as e:
            print(e.code)
            print('未获取到soup对象')
            sys.exit()
            

if __name__ =='__main__':
    my8 =msyc()

    # import sched
    # import time
    # from datetime import datetime
    # # 初始化sched模块的 scheduler 类
    # # 第一个参数是一个可以返回时间戳的函数，第二个参数可以在定时未到达之前阻塞。
    # schedule = sched.scheduler(time.time, time.sleep)
    # # 被周期性调度触发的函数
    # def printTime(inc):
    #     print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    #     schedule.enter(inc, 0, printTime, (inc,))
    # # 默认参数60s
    # def main(inc=60):
    #     # enter四个参数分别为：间隔事件、优先级（用于同时间到达的两个事件同时执行时定序）、被调用触发的函数，
    #     # 给该触发函数的参数（tuple形式）
    #     schedule.enter(0, 0, printTime, (inc,))
    #     schedule.run()
    #     sys.exit()
    # # 10s 输出一次
    # main(10)

    from apscheduler.schedulers.blocking import BlockingScheduler
    from datetime import datetime
    # 输出时间
    def job():
        my8.login()
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    # BlockingScheduler
    scheduler = BlockingScheduler()
    scheduler.add_job(job, 'interval', seconds=3300)
    scheduler.start()
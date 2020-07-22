#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-11-23 17:25:50
# @Author  : xi
# @Version : 1.0.0
# @describe: icourse163 课程评论爬取,中文乱码请参考https://blog.csdn.net/G_66_hero/article/details/73100056

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
import datetime
import csv

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.81 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
    'Host': 'www.icourse163.org',
    'Content-Length': '49',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Cookie': 'NTESSTUDYSI=399b45cf631c4ea3a9a1c953183e3976; EDUWEBDEVICE=9eb5bc9e7fae47f3bf8ccb0f2c1c77d1; WM_NI=nMYgzlBpnnzVKmTfcl6YumPGiGoxiOGNXTnAGoAD7WFQTTMUuurpD6qrFz3u%2F4u3IiqV1%2FdNYdjoRYuoUrJ90P2ZmZyqG2Qo%2FKKcBWgEGbgEyzeLUOcKJKgWsPSn9p2NZmY%3D; WM_NIKE=9ca17ae2e6ffcda170e2e6eeb6d744a6b69cb7f080b3eb8bb2d14b838b9aafb86ff3aabb95ce40969f8b95e42af0fea7c3b92aae939788f96882b0a28ff95e89b39c87e268f687bb8ed34dab99a199ec45859298b5ed4b85b18fa5b65d868f9cb5d05fb7abbe91c73eb3ae8a9bb27fedecbbd4cc63b38affd0e7469bbca690d153b7b19b93c933f490febbf052bbaf89d3d465ed958584c15da59b8983e64fbba6abadd845a19586ace65db1909d8fbc7cf292968edc37e2a3; WM_TID=mTyjtzTDvVdFEERQRQI9f07v9a9BAR4f; utm="eyJjIjoiIiwiY3QiOiIiLCJpIjoiIiwibSI6IiIsInMiOiIiLCJ0IjoiIn0=|aHR0cHM6Ly93d3cuZ29vZ2xlLmNvbS8="; hb_MA-A976-948FFA05E931_source=www.google.com',
    'Origin': 'https://www.icourse163.org',
    'Referer': 'https://www.icourse163.org/course/BIT-268001',
    'edu-script-token': '399b45cf631c4ea3a9a1c953183e3976',
}

    
class icourse163:
    def __init__(self,coureId='268001'):
        self.coureId=coureId
        self.url='https://www.icourse163.org/web/j/mocCourseV2RpcBean.getCourseEvaluatePaginationByCourseIdOrTermId.rpc?csrfKey=399b45cf631c4ea3a9a1c953183e3976'
        self.pagesize='50'
        self.session = requests.Session()
           
    def get_info(self):
        data = self.get_soup()
        all_rows=[]
        title=['id','gmtModified','commentorId','content','mark','termId','agreeCount','faceUrl']
        all_rows.append(title)
        try:
            totlePageCount = data['result']['query']['totlePageCount']
            for item in data['result']['list']:
                all_rows.append([item['id'],item['gmtModified'],item['commentorId'],item['content'],item['mark'],item['termId'],item['agreeCount'],item['faceUrl']])
            for page in range(2,totlePageCount):
                info = self.session.post(self.url,headers=headers,data={'courseId':self.coureId ,'pageIndex': '%d'%page,'pageSize': self.pagesize,'orderBy': '3'})#,verify=False
                data = json.loads(info.content)
                for item in data['result']['list']:
                    all_rows.append([item['id'],item['gmtModified'],item['commentorId'],item['content'],item['mark'],item['termId'],item['agreeCount'],item['faceUrl']])
                print('process page %d ok'%page)
                time.sleep(0.5)
            with open('%s.csv'%self.coureId,'w',encoding='utf-8') as f_w:
                fw_csv = csv.writer(f_w)
                fw_csv.writerows(all_rows)
                print('oK')
        except Exception as e:
            print(e)
      
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
            info = self.session.post(self.url,headers=headers,data={'courseId':self.coureId ,'pageIndex': '1','pageSize': self.pagesize,'orderBy': '3'})#,verify=False
            data = json.loads(info.content)
            return data
        except urllib.error.HTTPError as e:
            print(e.code)
            print('未获取到soup对象')
            sys.exit()
            

if __name__ =='__main__':
    my8 =icourse163()
    my8.get_info()
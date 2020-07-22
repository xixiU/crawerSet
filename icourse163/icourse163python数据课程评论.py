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
    'Cookie': 'NTESSTUDYSI=53214034e38148a0a96c634d7ceda814; EDUWEBDEVICE=6326a4d24c9f48e2b1033de71eb48307; __utmc=63145271; __utmz=63145271.1544952370.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); WM_NI=nDlgxaCjKotvtU54YT7ipvx9Z5RGZqm7gaXkiEHUR2y3jzfr46r%2B%2FpJPgOUtjVJGUFrfYF9abBJ92B6K4L4Mei9EdZNaw8mnzORpyYTf6nP%2BXr7InLgHnA344pUdY6ECc0c%3D; WM_NIKE=9ca17ae2e6ffcda170e2e6eed3e560f6b987acaa3382b88fa7c15e938f8fbab848b4b0fcaae968ad9ff791fb2af0fea7c3b92aae9ca488fb6b81b68590f77eb88bfbd5dc60f5b7c097fb339aeb9ea8d97bafe9a982db61ab9b88b6d13abbeda69be57af8eabeccae7c8a90a9b0d880aa8a86a8d84eb2ba97a7bc6ba29e86dab14af695fcadb747a7b7f7a6e7528ebfb9d9f066ba919e91fc5398bafa8fd3219caef9aaed48a598a2a2b240f8b09b85dc3e879dadd1e237e2a3; WM_TID=NZH2ejRIx7JBUBRFVVY9bot8Ynl9V98h; __utma=63145271.564051313.1544952370.1544952370.1544955095.2',
    'Origin': 'https://www.icourse163.org',
    'Referer': 'https://www.icourse163.org/course/ZJU-199001',
    'edu-script-token': '53214034e38148a0a96c634d7ceda814',
}

    
class icourse163:
    def __init__(self,coureId='199001'):
        self.coureId=coureId
        self.url='https://www.icourse163.org/web/j/mocCourseV2RpcBean.getEvaluateAvgAndCount.rpc?csrfKey=53214034e38148a0a96c634d7ceda814'
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
            # parpare = self.session.get(url='https://www.icourse163.org/course/ZJU-199001',headers=headers)
            # print(parpare.status_code)
            info = self.session.post(self.url,headers=headers,data={'courseId':self.coureId ,'pageIndex': '1','pageSize': self.pagesize,'orderBy': '3'})#,verify=False
            print(info.content)
            data = json.loads(info.content)
            return data
        except urllib.error.HTTPError as e:
            print(e.code)
            print('未获取到soup对象')
            sys.exit()
            

if __name__ =='__main__':
    my8 =icourse163()
    my8.get_info()

#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2019-12-27 18:56:46
# @Author  : yuan
# @Version : 1.0.0
# @describe: 通过url获取个人信息

import os
import urllib
import requests
import re
from bs4 import BeautifulSoup
from bs4.element import Comment

def tag_visible(element):
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    if isinstance(element, Comment):
        return False
    return True

class Crawer(object):
    def __init__(self,url,filename):
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3394.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        # 'Host': 'www.zhibo8.cc',
        'Cache-Control': 'max-age=0',
        'Upgrade-Insecure-Requests': '1'}
        self.session = requests.Session()
        self.url  = url
        self.removeUnChinese = lambda pageContext:re.sub(re.compile(r'[\u4e00-\u9fa5]'),"",pageContext)
        self.savePagepPath = 'pageCache'
        self.filename = filename 
        if not os.path.exists(self.savePagepPath):
            os.mkdir(self.savePagepPath)
    def get_soup(self):
        try:
            #response = urllib.request.urlopen(url,data=bytes(json.dumps(headers), encoding="utf-8"))
            info = self.session.get(self.url,headers=self.headers,timeout=5)#,verify=False
            # print(info.content)#byte code style
            soup=BeautifulSoup(info.content,'html.parser')#response.read()
            texts = soup.findAll(text=True)
            visible_texts = filter(tag_visible, texts)  
            return u" ".join(t.strip() for t in visible_texts)#返回所有页面元素，取出css html部分
        except  Exception:
            print('error:timeout ')
            return ""
            
    def get_Email(self,pagecontext):
        result = re.findall(r'[\w\.-]+@[\w\.-]+', pagecontext)
        return result if result!=None else ""
    def get_QQ(self,pagecontext):
        '''
        还需要进一步完善
        '''
        pattern = r"[1-9][0-9]{4,14}"#第一位1-9之间的数字，第二位0-9之间的数字，数字范围4-14个之间
        result = re.findall(pattern, pagecontext)
        return result if result!=None else ""

    
    def start(self):
        '''返回格式:去除非中文后的正文，QQ,Email'''
        pageContext = self.get_soup().strip()
        with open(os.path.join(self.savePagepPath,self.filename+'.txt'),'w+') as f_w:
            f_w.write(pageContext)
        return self.get_QQ(pageContext),self.get_Email(pageContext)

if __name__ == "__main__":
    print(Crawer('http://www.zizitang.com/',1).start())
        
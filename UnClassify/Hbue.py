#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2019-11-16 10:27:27
# @Author  : www.veryhaoke.com
# @Version : 1.0.0
# @describe: p爬取  http://news.hbue.edu.cn/jyyw/list.htm

import os
import requests
from bs4 import BeautifulSoup
import csv
import urllib
import sys
class Hbue(object):
    def __init__(self,max_item=100):
        """
        max_item: 最多默认爬取的条数，默认为100
        """
        self.headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3394.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Accept-Encoding': 'gzip, deflate',#,br
        'Connection': 'keep-alive',
        'Host': 'news.hbue.edu.cn',
        'Cache-Control': 'max-age=0',
        'Upgrade-Insecure-Requests': '1'}
        self.host='http://news.hbue.edu.cn'
        self.base_url='http://news.hbue.edu.cn/jyyw/list{}.htm'
        self.session = requests.Session()#后续都通过session完成爬取
        self.max_item = max_item
        
    def getSoup(self,start=1,url=None):
        if url==None:
            url = self.base_url.format(start)
        try:
            info = self.session.get(url,headers=self.headers)#,verify=False
            soup=BeautifulSoup(info.content,'html.parser')#response.read()
            return soup
        except urllib.error.HTTPError as e:
            print(e.code)
            print('未获取到soup对象,即将退出')
            sys.exit()
    def getContent(self,startpage=1):
        soup = self.getSoup(startpage)
        tag=soup.find('ul',attrs={'class':'wp_article_list'})

        result = []
        if len(tag)>0:
            nodeinfo = tag.find_all('li')
            for item in nodeinfo:
                newTag= item.find('span',attrs={'class':'Article_Title'})
                timeTag =item.find('span',attrs={'class':'Article_PublishDate'})#<span class="Article_PublishDate">2019-11-15</span>
                # print("新闻标题:"+newTag.text)
                # print("新闻链接:"+newTag.find('a')['href'])
                # print('发布时间'+timeTag.text)
                apgeItem = [newTag.text,self.host+newTag.find('a')['href'],timeTag.text]
                apgeItem.extend(self.getAtricalDeatil(self.host+newTag.find('a')['href']))
                result.append(apgeItem)
        return result
    def getAtricalDeatil(self,url):
        soup = self.getSoup(url=url)
        metasTag = soup.find('p',attrs={"class":"arti_metas"})
        metasInfo = metasTag.text#来源：主题教育领导小组办公室   党委宣传部发布者：陶慧发布时间：2019-11-15
        # print(metasInfo)
        sourceDep = metasInfo[metasInfo.index("来源：")+len("来源："):metasInfo.index('发布者')]
        publicPeo = metasInfo[metasInfo.index("发布者：")+len("发布者："):metasInfo.index('发布时间')]
        publicTime  = metasInfo[metasInfo.index("发布时间：")+len("发布时间："):]

        pageDetail = soup.find('div',attrs={"class":"wp_articlecontent"}).text
        return [sourceDep,publicPeo,publicTime,pageDetail]
    def start(self,save_filename='export.csv'):

        startPage = 1
        allresult=[["标题","链接地址","发布时间","来源","发布者","页内发布时间","正文"]]
        while len(allresult)<self.max_item:
            allresult.extend(self.getContent(startPage))
            startPage+=1
        with open(save_filename,'w') as f_w:
            spamwriter = csv.writer(f_w)
            spamwriter.writerows(allresult)
        print("Done!Buy a coffe for biggo haa")
if __name__ == "__main__":
    Hbue().start()
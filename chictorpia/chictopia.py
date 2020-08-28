#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-09-05 18:44:20
# @Author  : yuan
# @Version : 1.0.0
# @describe: 

import requests

from bs4 import BeautifulSoup
import urllib
import pickle as pl
import os
import sys

sys.setrecursionlimit(10000)

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3394.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.9',
    'Accept-Encoding': 'gzip, deflate',
    'Connection': 'keep-alive',
    'Host': 'www.chictopia.com',
    'If-None-Match': 'W/"04e8b92f35dd86aa1a5fbfd29e7a8ad9"',
    'Cache-Control': 'max-age=0',
    'Upgrade-Insecure-Requests': '1'}

class chictopia:
    def __init__(self,debug_model=True):
        self.session = requests.Session()
        self.debug=debug_model#just for debug model
        self.saveSessionFileName='session_.pl'
        self.url='http://www.chictopia.com'
        self.url_except='/browse'
        if not os.path.exists('img'):
            os.mkdir('img')
    def get_soup(self):
        try:
            #response = urllib.request.urlopen(url,data=bytes(json.dumps(headers), encoding="utf-8"))
            info = self.session.get(self.url,headers=headers)#,verify=False
            # print(info.content)
            soup=BeautifulSoup(info.content,'html.parser')#response.read()
            if self.debug:
                with open(self.saveSessionFileName,'wb') as f_w:
                    pl.dump(soup,f_w,0)
            return soup

        except urllib.error.HTTPError as e:
            print(e.code)
            print('未获取到soup对象')
            sys.exit()
    def get_info(self):
        if os.path.exists(self.saveSessionFileName):
            with open(self.saveSessionFileName,'rb') as f_r:
                self.soup = pl.load(f_r,encoding='utf-8')
        else:
            self.soup=self.get_soup()
        picture_tags = self.soup.find_all('div',attrs={'style':'position:relative;'})
        for one_tag in picture_tags:
            tag_page = one_tag.find('a')
            if tag_page:
                url = tag_page['href']
                if url!=self.url_except:
                    self.get_tag_info(url)
    def get_tag_info(self,page_url):
        try:
            info_page = self.session.get(self.url+page_url)
            soup = BeautifulSoup(info_page.content,'html.parser')

            tag_soup = soup.find('div',attrs={'class':'left clear px10','style':'text-transform:capitalize;text-decoration:underline;line-height:15px;'})
            if tag_soup:
                tag_boxs = tag_soup.find_all('div',attrs={'class':'left px10','style':'text-decoration:underline;line-height:15px;'})
                #class="left clear px10" style="text-transform:capitalize;text-decoration:underline;line-height:15px;"
                if tag_boxs:
                    box_list=[]
                    for tag_box in tag_boxs:
                        # print(tag_box)
                        if tag_box.text!=None:
                            # print(''.join(tag_box.text.split()))
                            box_list.append(''.join(tag_box.text.split()))
                    if len(box_list)>0:
                        url_soup = soup.find('div',attrs={'id':'left_column','class':'left'}).find('div',attrs={'style':'position:relative;'})
                        url_tag = url_soup.find('img')
                        urllib.request.urlretrieve(url_tag['src'], 'img/'+'_'.join(box_list)+'.jpg')

        except urllib.error.HTTPError as e:
            print(e.code)
            print('未获取到soup对象')
            sys.exit()       


if __name__ == "__main__":
    my = chictopia()
    my.get_info()

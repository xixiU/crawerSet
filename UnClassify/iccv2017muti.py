# -*- coding: utf-8 -*-
"""
Created on Fri Nov 17 19:09:04 2017

@author: x

Blog:xixiu.github.io
"""

import urllib.request
import time,datetime
import os
import socket
import re
import http.client
import threading

class Iccv_rawler(object):
    # 睡眠时长
    __time_sleep = 0.1
    #默认下载文件夹
    __mydir ='iccv2017'
    __i_headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.101 Safari/537.36',}
    __proxy=False
    __url='http://openaccess.thecvf.com/ICCV2017.py'
    __paperlist=[]
    __biblist=[]
    original_fileneme='bibref.txt'
    # t 下载图片时间间隔
    def __init__(self, t=0.1,mydir='iccv2017'):
        self.time_sleep = t
        self.__mydir='./' + mydir + '/'

    def pageget(self):
        print('begin  to getpage')

         #设置代理
        if(self.__proxy):
            proxy = {'http':'127.0.0.1:12306'}
            proxy_support = urllib.request.ProxyHandler(proxy)
            opener = urllib.request.build_opener(proxy_support,urllib.request.HTTPHandler(debuglevel=1))
            urllib.request.install_opener(opener)
        try:
            req=urllib.request.Request(url=self.__url,headers=self.__i_headers)
            page=urllib.request.urlopen(req)
#            data=page.read().decode('utf8')#ISO-8859-1
            data=page.read().decode('utf8')
            
        except http.client.IncompleteRead as icread:
            data=icread.partial.decode('utf-8')
        except urllib.error.URLError as e:
            print("-----urlErrorurl:", self.__url)
            pass
        except socket.timeout as e:
            print("-----socket timout:", self.__url)
        else:
            print('1')
        finally:
            page.close()
            self.get_keyword(data)
            self.write_bib()
            self.__downloadPdf()
        

    def __downloadPdf_single(self, single_info,i):
        
        time.sleep(self.time_sleep)
        name = lambda x:x.split('/')[-1]
        try:
            if not os.path.isdir(self.__mydir):
                os.makedirs(self.__mydir )
            lengthpap=len(self.__paperlist)
            print('TIme:%s begin to download the %d -th ,left %d to download .\nThe name of the pdf is %s \n'%(time.ctime(time.time()),i,lengthpap-i,name(single_info)))
            urllib.request.urlretrieve('http://openaccess.thecvf.com/content_ICCV_2017/papers'+single_info ,self.__mydir + name(single_info))
        except Exception as ex:
            template = "An exception of type {0} occurred. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            print (message)
    
    def write_bib(self):
        with open(self.original_fileneme,'w',encoding='utf-8') as f:
            for x in self.__biblist:
                f.write(str(x).replace('<br>','') )
            f.close
        print('write bib ref success!Please chech in the progaram dir\n')
    def get_keyword(self,data):
        #在pattern中需要去掉()，/
        print('begin to filter')
        pattern_bibref=r'<div class="bibref">(.*?)</div>'
        self.__biblist=re.compile(pattern_bibref,re.DOTALL).findall(data)#len(keyword_list) 619
        pattern_pdf=r'<a href="content_ICCV_2017/papers(.*?)">pdf</a>'
        self.__paperlist=re.compile(pattern_pdf,re.DOTALL).findall(data)#618
    
    # 下载
    def __downloadPdf(self):
        i=1
        for x in self.__paperlist:
            one_thr = threading.Thread(target=self.__downloadPdf_single, args=[x,i])
            one_thr.start()
            one_thr.join()
            i+=1
#            self.__downloadPdf_single(x)
    
    def start(self):
        start_time=time.time()
        self.pageget()
        print("All done\n---Time use %s  ---" %str(datetime.timedelta(seconds=int(time.time()-start_time))))
        


if __name__ == '__main__':
    myiccv=Iccv_rawler()
    myiccv.start()

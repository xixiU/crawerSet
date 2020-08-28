#coding:utf-8
import requests
import time
import os
from urllib import parse

class Spider(object):
    def __init__(self):
        self.__username ='2086774733'
        #self.__password=config.get('qq_info','qq_password')
        self.headers={
                'host': 'h5.qzone.qq.com',
                'accept-encoding':'gzip, deflate, br',
                'accept-language':'zh-CN,zh;q=0.8',
                'accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                'user-agent':'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:55.0) Gecko/20100101 Firefox/55.0',
                'connection': 'keep-alive'
        }
        self.req=requests.Session()
        self.cookies={}#2129275436
        self.g_tk=2129275436

    

    def login(self):
        #self.web.switch_to_frame('login_frame')
        #log=self.web.find_element_by_id("switcher_plogin")
        #log.click()
        #time.sleep(1)
        #username=self.web.find_element_by_id('u')
        #username.send_keys(self.__username)
        #ps=self.web.find_element_by_id('p')
        #ps.send_keys(self.__password)
        #btn=self.web.find_element_by_id('login_button')
        #time.sleep(1)
        #btn.click()
        print('请扫码登陆')
        while 1:        
            if 'http://' in self.web.title:
                break
        print('扫码登陆成功')
        time.sleep(2)
        self.web.get('https://user.qzone.qq.com/{}'.format(self.__username))
        cookie=''
        for elem in self.web.get_cookies():
            cookie+=elem["name"]+"="+ elem["value"]+";"
        self.cookies=cookie
        self.get_g_tk()
        #time.sleep(10)
        self.headers['Cookie']=self.cookies
        self.web.quit()
        
    
    def get_frends_url(self):
        url='https://h5.qzone.qq.com/proxy/domain/base.qzone.qq.com/cgi-bin/right/get_entryuinlist.cgi?'
        params = {"uin": self.__username,
              "fupdate": 1,
              "action": 1,
              "g_tk": self.g_tk}
        url = url + parse.urlencode(params)
        return url

    def get_frends_num(self):
        t=True
        offset=0
        url=self.get_frends_url()
        self.headers['Cookie']='zzpaneluin=;zzpanelkey=;pgv_pvi=5792370688;pgv_si=s6894398464;pgv_pvid=5690981080;pgv_info=ssid=s6046263493;pt2gguin=o2086774733;uin=o2086774733;skey=@MbRFMQRSV;ptisp=ctc;RK=NxVLfE1aEU;ptcz=b97c945a211c0e78d418577d4425bac274004ae6653b77dfdda584ab33d3b62f;p_uin=o2086774733;p_skey=J5Yy4Fu1ccXEniTSRFX9Ab-Jy1-CWZKEjAFvTIxM--U_;pt4_token=Ooy0EPRKEQoe-pJ3Zd1IcshhKTyyUnYsg5hMAN7GVCg_;Loading=Yes;rv2=808E4195F86ED28DA5FDC8040477EE429EB30C6370FC2C20A9;property20=8443CE14F0D25F57798D0C8AEC85B5FBAF1C9F2B7E7B9F572A28A8CA8E84085051C9B84B2F15857C;randomSeed=720441;'
        while(t):
            url_=url+'&offset='+str(offset)
            page=self.req.get(url=url_,headers=self.headers)
            if "\"uinlist\":[]" in page.text:
                t=False
            else:

                if not os.path.exists("./frends/"):
                    os.mkdir("frends/")
                with open('./frends/'+str(offset)+'.json','w',encoding='utf-8') as w:
                    w.write(page.text)
                offset += 50

    def get_mood_url(self):
        url='https://h5.qzone.qq.com/proxy/domain/taotao.qq.com/cgi-bin/emotion_cgi_msglist_v6?'
        params = {
              "sort":0,
                  "start":0,
              "num":20,
            "cgi_host": "http://taotao.qq.com/cgi-bin/emotion_cgi_msglist_v6",
              "replynum":100,
              "callback":"_preloadCallback",
              "code_version":1,
            "inCharset": "utf-8",
            "outCharset": "utf-8",
            "notice": 0,
              "format":"jsonp",
              "need_private_comment":1,
              "g_tk": self.g_tk
              }
        url = url + parse.urlencode(params)
        return url


    def get_mood_detail(self):
        from getFrends import frends_list
        url = self.get_mood_url()
        for u in frends_list[:100]:
            print('%s  is process'%(u))
            t = True
            u['data']=u['data'].strip()
            QQ_number=u['data']
            url_ = url + '&uin=' + str(QQ_number)
            pos = 0
            while (t):
                url__ = url_ + '&pos=' + str(pos)
                mood_detail = self.req.get(url=url__, headers=self.headers)
                print(QQ_number,pos)
                if "\"msglist\":null" in mood_detail.text or "\"message\":\"对不起,主人设置了保密,您没有权限查看\"" in mood_detail.text:
                    t = False
                else:
                    if not os.path.exists("./mood_detail/"):
                        os.mkdir("mood_detail/")
                    if not os.path.exists("./mood_detail/"+u['data'].strip()):
                        os.mkdir("mood_detail/"+u['data'])
                    with open('./mood_detail/'+u['data']+"/" +str(QQ_number)+"_"+ str(pos) + '.json', 'w',encoding='utf-8') as w:
                        w.write(mood_detail.text)
                    pos += 20
            time.sleep(2)


    def get_g_tk(self):
        p_skey = self.cookies[self.cookies.find('p_skey=')+7: self.cookies.find(';', self.cookies.find('p_skey='))]
        h=5381
        for i in p_skey:
            h+=(h<<5)+ord(i)
        print('g_tk',h&2147483647)
        self.g_tk=h&2147483647


        

if __name__=='__main__':
    sp=Spider()
#    sp.login()
    sp.get_frends_num()
    sp.get_mood_detail()
#    from data_analys import dataToExcel

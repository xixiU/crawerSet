# -*- coding: utf-8 -*-
"""
Created on Wed Nov 29 22:25:18 2017

@author: x

Blog:xixiu.github.io
"""

# import itchat
# itchat.login()
# friends= itchat.get_friends()
#!/usr/bin/env python
# encoding=utf-8
from __future__ import print_function

import os
import requests
import re
import time
import xml.dom.minidom
import json
import sys
import math
import subprocess
import ssl
import threading
import urllib,urllib.request
import csv
import pickle

DEBUG = False

MAX_GROUP_NUM = 2  # 每组人数
INTERFACE_CALLING_INTERVAL = 5  # 接口调用时间间隔, 间隔太短容易出现"操作太频繁", 会被限制操作半小时左右
MAX_PROGRESS_LEN = 50

QRImagePath = os.path.join(os.getcwd(), 'qrcode.jpg')

tip = 0
uuid = ''

base_uri = ''
redirect_uri = ''
push_uri = ''

skey = ''
wxsid = ''
wxuin = ''
pass_ticket = ''
deviceId = 'e000000000000000'

BaseRequest = {}

ContactList = []
My = []
SyncKey = []
all_data=[]
try:
    xrange
    range = xrange
except:
    # python 3
    pass


def responseState(func, BaseResponse):
    ErrMsg = BaseResponse['ErrMsg']
    Ret = BaseResponse['Ret']
    if DEBUG or Ret != 0:
        print('func: %s, Ret: %d, ErrMsg: %s' % (func, Ret, ErrMsg))

    if Ret != 0:
        return False

    return True



def getUUID():
    global uuid

    url = 'https://login.weixin.qq.com/jslogin'
    params = {
        'appid': 'wx782c26e4c19acffb',
        'fun': 'new',
        'lang': 'zh_CN',
        '_': int(time.time()),
    }

    r= myRequests.get(url=url, params=params)
    r.encoding = 'utf-8'
    data = r.text

    # print(data)

    # window.QRLogin.code = 200; window.QRLogin.uuid = "oZwt_bFfRg==";
    regx = r'window.QRLogin.code = (\d+); window.QRLogin.uuid = "(\S+?)"'
    pm = re.search(regx, data)

    code = pm.group(1)
    uuid = pm.group(2)

    if code == '200':
        return True

    return False


def showQRImage():
    global tip

    url = 'https://login.weixin.qq.com/qrcode/1/' + uuid
    params = {
        't': 'webwx',
        '_': int(time.time()),
    }

    r = myRequests.get(url=url, params=params)

    tip = 1

    f = open(QRImagePath, 'wb')
    f.write(r.content)
    f.close()
    time.sleep(1)

    if sys.platform.find('darwin') >= 0:
        subprocess.call(['open', QRImagePath],shell=True)
    else:
        subprocess.call(['xdg-open', QRImagePath],shell=True)

    print('请使用微信扫描二维码以登录')
    
    os.system('qrcode.jpg')    


def waitForLogin():
    global tip, base_uri, redirect_uri, push_uri

    url = 'https://login.weixin.qq.com/cgi-bin/mmwebwx-bin/login?tip=%s&uuid=%s&_=%s' % (
        tip, uuid, int(time.time()))

    r = myRequests.get(url=url)
    r.encoding = 'utf-8'
    data = r.text

    # print(data)

    # window.code=500;
    regx = r'window.code=(\d+);'
    pm = re.search(regx, data)

    code = pm.group(1)

    if code == '201':  # 已扫描
        print('成功扫描,请在手机上点击确认以登录')
        tip = 0
    elif code == '200':  # 已登录
        print('正在登录...')
        regx = r'window.redirect_uri="(\S+?)";'
        pm = re.search(regx, data)
        redirect_uri = pm.group(1) + '&fun=new'
        base_uri = redirect_uri[:redirect_uri.rfind('/')]

        # push_uri与base_uri对应关系(排名分先后)(就是这么奇葩..)
        services = [
            ('wx2.qq.com', 'webpush2.weixin.qq.com'),
            ('qq.com', 'webpush.weixin.qq.com'),
            ('web1.wechat.com', 'webpush1.wechat.com'),
            ('web2.wechat.com', 'webpush2.wechat.com'),
            ('wechat.com', 'webpush.wechat.com'),
            ('web1.wechatapp.com', 'webpush1.wechatapp.com'),
        ]
        push_uri = base_uri
        for (searchUrl, pushUrl) in services:
            if base_uri.find(searchUrl) >= 0:
                push_uri = 'https://%s/cgi-bin/mmwebwx-bin' % pushUrl
                break

        # closeQRImage
        if sys.platform.find('darwin') >= 0:  # for OSX with Preview
            os.system("osascript -e 'quit app \"Preview\"'")
    elif code == '408':  # 超时
        pass
    # elif code == '400' or code == '500':

    return code


def login():
    global skey, wxsid, wxuin, pass_ticket, BaseRequest

    r = myRequests.get(url=redirect_uri)
    r.encoding = 'utf-8'
    data = r.text

    # print(data)

    doc = xml.dom.minidom.parseString(data)
    root = doc.documentElement

    for node in root.childNodes:
        if node.nodeName == 'skey':
            skey = node.childNodes[0].data
        elif node.nodeName == 'wxsid':
            wxsid = node.childNodes[0].data
        elif node.nodeName == 'wxuin':
            wxuin = node.childNodes[0].data
        elif node.nodeName == 'pass_ticket':
            pass_ticket = node.childNodes[0].data

    # print('skey: %s, wxsid: %s, wxuin: %s, pass_ticket: %s' % (skey, wxsid,
    # wxuin, pass_ticket))

    if not all((skey, wxsid, wxuin, pass_ticket)):
        return False

    BaseRequest = {
        'Uin': int(wxuin),
        'Sid': wxsid,
        'Skey': skey,
        'DeviceID': deviceId,
    }

    return True


def webwxinit():

    url = (base_uri + 
        '/webwxinit?pass_ticket=%s&skey=%s&r=%s' % (
            pass_ticket, skey, int(time.time())) )
    params  = {'BaseRequest': BaseRequest }
    headers = {'content-type': 'application/json; charset=UTF-8'}

    r = myRequests.post(url=url, data=json.dumps(params),headers=headers)
    r.encoding = 'utf-8'
    data = r.json()

    if DEBUG:
        f = open(os.path.join(os.getcwd(), 'webwxinit.json'), 'wb')
        f.write(r.content)
        f.close()

    all_data_pickle=os.path.join(os.getcwd(),'all_data_pickle.txt')
    with open(all_data_pickle,'wb') as f_member:
        pickle.dump(data,f_member,0)
    
#    print(data)

    global ContactList, My, SyncKey,all_data
    all_data=data
    dic = data
    ContactList = dic['ContactList']
    My = dic['User']
    my_info(My)
    SyncKey = dic['SyncKey']

    state = responseState('webwxinit', dic['BaseResponse'])
    return state


    
def webwxgetcontact():

    url = (base_uri + 
        '/webwxgetcontact?pass_ticket=%s&skey=%s&r=%s' % (
            pass_ticket, skey, int(time.time())) )
    headers = {'content-type': 'application/json; charset=UTF-8'}


    r = myRequests.post(url=url,headers=headers)
    r.encoding = 'utf-8'
    data = r.json()
    
    
    if DEBUG:
        f = open(os.path.join(os.getcwd(), 'webwxgetcontact.json'), 'wb')
        f.write(r.content)
        f.close()


    dic = data
    MemberList = dic['MemberList']

    # 倒序遍历,不然删除的时候出问题..
    SpecialUsers = ["newsapp", "fmessage", "filehelper", "weibo", "qqmail", "tmessage", "qmessage", "qqsync", "floatbottle", "lbsapp", "shakeapp", "medianote", "qqfriend", "readerapp", "blogapp", "facebookapp", "masssendapp",
                    "meishiapp", "feedsapp", "voip", "blogappweixin", "weixin", "brandsessionholder", "weixinreminder", "wxid_novlwrv3lqwv11", "gh_22b87fa7cb3c", "officialaccounts", "notification_messages", "wxitil", "userexperience_alarm"]
    for i in range(len(MemberList) - 1, -1, -1):
        Member = MemberList[i]
        if Member['VerifyFlag'] & 8 != 0:  # 公众号/服务号
            MemberList.remove(Member)
        elif Member['UserName'] in SpecialUsers:  # 特殊账号
            MemberList.remove(Member)
        elif Member['UserName'].find('@@') != -1:  # 群聊
            MemberList.remove(Member)
        elif Member['UserName'] == My['UserName']:  # 自己
            MemberList.remove(Member)#

    return MemberList


def syncKey():
    SyncKeyItems = ['%s_%s' % (item['Key'], item['Val'])
                    for item in SyncKey['List']]
    SyncKeyStr = '|'.join(SyncKeyItems)
    return SyncKeyStr


def syncCheck():
    url = push_uri + '/synccheck?'
    params = {
        'skey': BaseRequest['Skey'],
        'sid': BaseRequest['Sid'],
        'uin': BaseRequest['Uin'],
        'deviceId': BaseRequest['DeviceID'],
        'synckey': syncKey(),
        'r': int(time.time()),
    }

    r = myRequests.get(url=url,params=params)
    r.encoding = 'utf-8'
    data = r.text

    # print(data)

    # window.synccheck={retcode:"0",selector:"2"}
    regx = r'window.synccheck={retcode:"(\d+)",selector:"(\d+)"}'
    pm = re.search(regx, data)

    retcode = pm.group(1)
    selector = pm.group(2)

    return selector


def webwxsync():
    global SyncKey

    url = base_uri + '/webwxsync?lang=zh_CN&skey=%s&sid=%s&pass_ticket=%s' % (
        BaseRequest['Skey'], BaseRequest['Sid'], urllib.quote_plus(pass_ticket))
    params = {
        'BaseRequest': BaseRequest,
        'SyncKey': SyncKey,
        'rr': ~int(time.time()),
    }
    r = myRequests.post(url=url, data=json.dumps(params))
    r.encoding = 'utf-8'
    data = r.json()

    # print(data)

    dic = data
    SyncKey = dic['SyncKey']

    state = responseState('webwxsync', dic['BaseResponse'])
    return state


        
def heartBeatLoop():
    while True:
        selector = syncCheck()
        if selector != '0':
            webwxsync()
        time.sleep(1)

def save_to_pickle(data_info,filename):
    """
    save data to file using pickle
    
    :data_info: data to save 
    :filename: the name of file to write
    """
    pickle_filepath=os.path.join(os.getcwd(),filename)
    with open(pickle_filepath,'wb') as f_w :
        pickle.dump(data_info,f_w,0)
    
def save_friend_list_to_csv(friend_list,filename='MemberList.csv'):
    """
    乱码
    #import codecs
    #fcsv_w_csv.write(codecs.BOM_UTF8)#py2乱码 上面不用codecs.open()直接使用open即可
    """
    WeChatFriend_csv=os.path.join(os.getcwd(), filename)
    import codecs
    with codecs.open(WeChatFriend_csv,'w',encoding='utf_8_sig') as fcsv_w:
        fcsv_w_csv = csv.writer(fcsv_w)
#        fcsv_w_csv.writerow(first_row) 
        if type(friend_list[0]).__name__=='list':
            fcsv_w_csv.writerows(friend_list)
        else:
            fcsv_w_csv.writerow(friend_list)

def my_info(dict_my):
    """
    return to my info list
    :dict_my: dictionary of my infomation
    """
    my_Uin=dict_my['Uin']
    my_Username=dict_my['UserName']
    my_NickName=dict_my['NickName']
    my_Sex=dict_my['Sex']
    my_Signature=dict_my['Signature']
    my_HeadImgUrl=dict_my['HeadImgUrl']
    
    my_list=[my_Uin,my_Username,my_NickName,my_Sex,my_Signature,my_HeadImgUrl]
    
    from dbProcess import  Db_process
    my_db=Db_process()
#    print(my_list,end='***')
    try:
        
        my_db.save_user(my_list)
    except Exception as ex:
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        print(message)
    finally:
        my_db.con_close()
    return my_list

def down_HeadImg(name,url,headers):
    """
    
    """
    name = os.getcwd()+'/friendImage/'+str(name)+'.jpg'
    imageUrl = 'https://wx2.qq.com'+url+'&type=big'
    r = myRequests.get(url=imageUrl,headers=headers)
    imageContent = (r.content)
    fileImage = open(name,'wb')
    fileImage.write(imageContent)
    fileImage.close()
    
def main():
    global myRequests
    
    if hasattr(ssl, '_create_unverified_context'):
        ssl._create_default_https_context = ssl._create_unverified_context

    headers = {'User-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.125 Safari/537.36',}
    myRequests = requests.Session()
    myRequests.headers.update(headers)


    if not getUUID():
        print('获取uuid失败')
        return

    print('正在获取二维码图片...')
    showQRImage()

    while waitForLogin() != '200':
        pass

    os.remove(QRImagePath)

    if not login():
        print('登录失败')
        return

    if not webwxinit():
        print('初始化失败')
        return

    MemberList = webwxgetcontact()

    threading.Thread(target=heartBeatLoop)

    MemberCount = len(MemberList)
    print('通讯录共%s位好友' % MemberCount)
    d = {}
#    imageIndex = 0
    all_rows=[]
    first_row=['UserName','name','remark','province','city','gender','sinagure','starfriend','HeadImgUrl','UserName','From']
    
    from dbProcess import  Db_process
    my_db=Db_process()
    
    for Member in MemberList:
        row=[]
#        imageIndex = imageIndex + 1
#        name = os.getcwd()+'/friendImage/'+str(imageIndex)+'.jpg'
#        imageUrl = 'https://wx2.qq.com'+Member['HeadImgUrl']+'&type=big'
#        r = myRequests.get(url=imageUrl,headers=headers)
#        imageContent = (r.content)
#        fileImage = open(name,'wb')
#        fileImage.write(imageContent)
#        fileImage.close()
#        print('正在下载第：'+str(imageIndex)+'位好友头像')
#        down_HeadImg(imageIndex,Member['HeadImgUrl'],headers)
        d[Member['UserName']] = (Member['NickName'], Member['RemarkName'])
        name = Member['NickName'].rstrip('\n')#'昵称'
        name = 'noname' if name == '' else  name
        province = Member['Province']#'省份'
        province = 'noprovince' if province =='' else province
        city = Member['City'] #城市
        city = 'nocity' if city == '' else  city
        sign = Member['Signature'].rstrip('\n')
        sign = 'nosign' if sign == '' else  sign
        remark = Member['RemarkName']#'备注'
        remark = 'noremark' if remark == '' else remark
        alias = Member['Alias']
        alias = 'noalias' if alias == '' else alias
        row=[Member['UserName'],name,remark,province,city,Member['Sex'],sign,Member['StarFriend'],Member['HeadImgUrl'],My['Uin']]
        all_rows.append(row)
#        print(name,',',city,',',Member['Sex'],',',Member['StarFriend'],',',sign,', ',remark,',',alias,',' )
        
        try:
            my_db.save_friend(row)
        except Exception as ex:
            template = "An exception of type {0} occurred. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            print(message)
    #close connection
    my_db.con_close()
    
    #save friend to csv
    all_rows.insert(0,first_row)
    save_friend_list_to_csv(all_rows)
    #
#    save_to_pickle(MemberList,'MemberList.txt')
    
#        import csv
#        fw_csv = csv.writer(f_w)
##        fw_csv.writerow([])
#        fw_csv.writerows(MemberCount)

if __name__ == '__main__':
    #main()
    from analyse import start_analyse
    start_analyse()


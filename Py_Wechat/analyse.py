# -*- coding: utf-8 -*-
"""
Created on Sun Dec  3 17:19:23 2017

@author: x

Blog:xixiu.github.io
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

plt.rcParams['font.sans-serif'] = ['SimHei']

df = pd.read_csv('MemberList.csv')

def city():
    '''微信朋友圈的城市'''
    city_address = df['city'].value_counts()
    city_address=city_address[city_address.index!='nocity']
    plt.figure(1)
    plt.subplot(221)
    city_address[1:10].plot(kind='barh',title ='好友城市分布')
    
def province():
    '''微信朋友圈的城市'''
    province_address = df['province'].value_counts()
    province_address=province_address[province_address.index!='noprovince']
    plt.figure(1)
    plt.subplot(222)
    province_address[1:10].plot(kind='bar',title ='好友省级分布')
    plt.show()
    
def gender():
    '''微信朋友的性别比例
        1:男  2：女   3：未知
    '''
    gender = df['male'].value_counts()
    print (gender)
    
def star():
    '''星标好友
        1:星标   0：非星标
    '''
    star = df['star'].value_counts()
    print (star)
    
def friend_count():
    remark = df['remark']#备注
    name = df['name']
    
    remarkCount = 0
    maleCount = 0
    femaleCount = 0
    for i in range(1,len(remark)):
        if str(remark[i]).strip() == str(name[i]).strip() or remark[i] == '  noremark  ':
            remarkCount = remarkCount + 1
        else:
            if judgeGender(i) == 'male':
                maleCount = maleCount + 1
            elif judgeGender(i) == 'female':
                femaleCount = femaleCount + 1
    print ('微信总朋友人数：',str(len(remark)),'\n')
    print ('预计认识的总人数：',str(len(remark)-remarkCount),'\n')
    print ('认识的人中汉子人数：',maleCount,'妹子人数：',femaleCount)
    draw_gender_bar(maleCount,femaleCount)
    
def draw_gender_bar(maleCount,femaleCount):
    plt.figure(2)
    sex_count={'maleCount':maleCount,'femaleCount':femaleCount}
    
    plt.bar(range(len(sex_count)), sex_count.values(), align='center',color=['red','green'])#
    plt.xticks(range(len(sex_count)), sex_count.keys())
    male = mpatches.Patch(color='red', label='男')
    female = mpatches.Patch(color='green', label='女')
    plt.legend(handles=[male,female],)
    plt.title('性别')
    plt.show()
    

def judgeGender(index):
    '''判断传入的某个位置的用户的性别
        参数：int行
        返回结果：字符串
    '''
    gender = df['gender']
    if gender[index] == 1:
        return 'male'
    elif gender[index] == 2:
        return 'female'
    else:
        return 'unknown' 
    
def start_analyse():
    """
    to start
    """
    friend_count()
    city()
    province()
    
    

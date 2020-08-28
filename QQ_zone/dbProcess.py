# -*- coding: utf-8 -*-
"""
Created on Fri Sep 29 16:00:10 2017

@author: x
"""
import pymysql
class Db_process(object):
    def __init__(self):
        self.con=pymysql.connect(
            host='xx',
            user='root',
            password="123456",
            database='qq_z',
            port=3306,
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor,
        )
        self.cur=self.con.cursor()
    def fetch_maxId(self):
        select_sql='select max(s_id) from s_info;'
        self.cur.execute(select_sql)
        data = self.cur.fetchone()
#        print("data类型是%s,内容是:%s"%(type(data),data))
        return data['max(s_id)']
    
    def fetch_maxUserId(self):
        select_sql='select * from q_user;'
        self.cur.execute(select_sql)
        data = self.cur.fetchall()
        for xx in data:
            print(xx)
    #    print("data类型是%s,内容是:%s"%(type(data),data))
    
    #print(fetch_maxId())
    
    def fetch_data():
        pass
    
my=Db_process()
dd=my.fetch_maxId()
print(dd)

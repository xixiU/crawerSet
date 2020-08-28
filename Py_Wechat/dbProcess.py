# -*- coding: utf-8 -*-
"""
Created on Fri Sep 29 16:00:10 2017

@author: x
"""
import pymysql
class Db_process(object):
    def __init__(self):
        self.con=pymysql.connect(
            host='localhost',
            user='root',
            password="123456",
            database='we_chat',
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
    
    def save_user(self,infolist):
        """
        Uin,UserName, nickname,gender,sinagure,head_img,u_time
        """
        sql = "INSERT INTO wechat_user (Uin,UserName, nickname,gender,sinagure,head_img,u_time) VALUES (%s, %s, %s, %s,%s, %s,now())"
        submit_result=self.cur.execute(sql, infolist)#1 success
        self.con.commit()
        
    def save_dict_user(self,dict_my):
        """
        Uin,UserName, nickname,gender,sinagure,head_img,u_time
        """
        sql = "INSERT INTO wechat_user (Uin,UserName, nickname,gender,sinagure,head_img,u_time) VALUES (%s, %s, %s, %s,%s, %s,now())"
        my_Uin=dict_my['Uin']
        my_Username=dict_my['UserName']
        my_NickName=dict_my['NickName']
        my_Sex=dict_my['Sex']
        my_Signature=dict_my['Signature']
        my_HeadImgUrl=dict_my['HeadImgUrl']
        
        submit_result=self.cur.execute(sql, (my_Uin,my_Username,my_NickName,my_Sex,my_Signature,my_HeadImgUrl))#1 success
        self.con.commit()

    def save_friend(self,infolist):
        """
        id,UserName, nickname,remark,province,city,gender,sinagure,starfriend,head_img,u_uin
        """
        
        sql = "INSERT INTO wechat_friends (id,UserName, nickname,remark,province,city,gender,sinagure,starfriend,head_img,u_uin) VALUES (null,%s, %s,%s, %s,%s, %s,%s, %s,%s,%s)"
        submit_result=self.cur.execute(sql, infolist)#1 success
        self.con.commit()
    def con_close(self):
        self.con.close()
        
    
#my=Db_process()
#info=['@ff1d93df2f8ae59fccfb494bf900491c0b34ab8817fb600f27df5771e284eaa9','农鑫','noprovince','nocity','1','有人知道我需要什么','/fheiahfiahfoiahf/',]
#my.save_user(info)

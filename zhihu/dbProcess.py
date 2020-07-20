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
            database='zhihu',
            port=3306,
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor,
        )
        self.cur=self.con.cursor()

    
    def insert_user(self,user_info):
        sql = "INSERT INTO user (username,userimage, userurl,userheadline,userfollower) VALUES (%s, %s, %s, %s,%s)"
        self.cur.execute(sql, user_info)
        self.con.commit()
        print('插入用户成功')
        
    def insert_question(self,question_info):
        sql = "INSERT INTO question (question_id,follower, view_times,comment_number,answers,question_createtime,question_modifytime) VALUES (%s, %s, %s, %s,%s,%s,%s)"
        self.cur.execute(sql, question_info)#1 success
        self.con.commit()
        print('插入问题成功')
        
    def insert_answer(self,answer_info,question_id):
        sql = "INSERT INTO answer (question_id,answer_id, answerurl,answercreatetime,answermotifiedtime,answercomment,answerupvoteCount,answer_info) VALUES (%s, %s, %s, %s,%s,%s,%s,%s)"
        self.cur.execute(sql, (question_id,*answer_info))#1 success
        self.con.commit()
        print('插入回答成功')
        
    def close(self):
        self.cur.close()
    
#my=Db_process()
#dd=my.fetch_maxId()
#print(dd)
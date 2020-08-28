#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import os
import xlwt
import pymysql
import datetime,time
import shutil
#存入Excel
# def dataToExcel():
#     d=[i for i in os.listdir('mood_detail') if not i.endswith('.xls')]
#     for ii in d:
#         wb=xlwt.Workbook()
#         sheet=wb.add_sheet('sheet1',cell_overwrite_ok=True)
#         sheet.write(0,0,'content')
#         sheet.write(0,1,'createTime')
#         sheet.write(0,2,'commentlist')
#         sheet.write(0,3,'source_name')
#         sheet.write(0,4,'cmtnum')
#         fl=[i for i in os.listdir('mood_detail/'+ii) if i.endswith('.json')]
#         print('mood_detail/'+ii)
#         k=1
#         for i in fl:
#             with open('mood_detail/'+ii+"/"+i,'r',encoding='latin-1') as w:
#                 s=w.read()[17:-2]
#                 js=json.loads(s)
#                 print(i)
#                 for s in js['msglist']:
#                     m=-1
#                     sheet.write(k,m+1,str(s['content']))
#                     sheet.write(k,m+2,str(s['createTime']))
#                     if not s['commentlist']:
#                         s['commentlist']=list()
#                     sheet.write(k,m+3,str([(x['content'],x['createTime2'],x['name'],x['uin']) for x in list(s['commentlist'])]))
#                     sheet.write(k,m+4,str(s['source_name']))
#                     sheet.write(k,m+5,str(s['cmtnum']))
#                     k+=1
#         if not os.path.exists('mood_detail/Excel/'):
#             os.mkdir('mood_detail/Excel/')
#         try:
#             wb.save('mood_detail/Excel/'+ii+'.xls')
#         except Exception:
#             print("error")
#

def ISOString2Time( s ):
    ''' 
    convert a ISO format time to second
    from:2006-04-12 16:46:40 to:23123123
    把一个时间转化为秒
    '''
    d=datetime.datetime.strptime(s,"%Y-%m-%d %H:%M:%S")
    return time.mktime(d.timetuple())

def Time2ISOString( s ):
    ''' 
    convert second to a ISO format time
    from: 23123123 to: 2006-04-12 16:46:40
    把给定的秒转化为定义的格式
    '''
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime( float(s) ) ) 

def dataToExcel():
    ll=0
    d=[i for i in os.listdir('mood_detail') if not i.endswith('.xls')]
    for ii in d:
        wb=xlwt.Workbook()
        sheet=wb.add_sheet('sheet1',cell_overwrite_ok=True)
        sheet.write(0,0,'content')
        sheet.write(0,1,'createTime')
        sheet.write(0,2,'commentlist')
        sheet.write(0,3,'source_name')
        sheet.write(0,4,'cmtnum')
        fl=[i for i in os.listdir('mood_detail/'+ii) if i.endswith('.json')]
        print('mood_detail/'+ii)
        k=1
        for i in fl:
            with open('mood_detail/'+ii+"/"+i,'r',encoding='utf-8') as w:
                s=w.read()[17:-2]
                js=json.loads(s)
                print(i)
                if 'msglist' not in js.keys():
                    break
                for s in js['msglist']:
                    ll+=1
                    m=-1
                    sheet.write(k,m+1,str(s['content']))
                    sheet.write(k,m+2,str(s['createTime']))
                    if not s['commentlist']:
                        s['commentlist']=list()
                    sheet.write(k,m+3,str([(x['content'],x['createTime2'],x['name'],x['uin']) for x in list(s['commentlist'])]))
                    sheet.write(k,m+4,str(s['source_name']))
                    sheet.write(k,m+5,str(s['cmtnum']))
                    k+=1
        if not os.path.exists('mood_detail/Excel/'):
            os.mkdir('mood_detail/Excel/')
        print(ll)
        try:
            wb.save('mood_detail/Excel/'+ii+'.xls')
        except Exception:
            print("error")

#dataToExcel()



def dataToMySQL():
	#INSERT INTO info VALUES('869057465','1504058154','新号18135187265，望惠存！原来的号基本不用了～',"[('哈哈哈哈你学我[em]e249[/em]', '2017-08-30 10:01:13', 'Say Hello', 1733982939), ('@{uin:392258690,nick:鸽子家族的哲学家,who:1,auto:1}伟植在哪里上班呢？', '2017-08-30 10:11:44', '陈家石', 869057465), ('西安的号？[em]e400824[/em][em]e400824[/em]', '2017-08-30 10:32:20', '糖葫芦', 2939702623), ('半夜骚扰', '2017-08-30 11:37:11', '林贤华', 961488353), ('到了？', '2017-08-30 13:30:45', 'Argon', 203958502), ('老板发财', '2017-08-30 13:30:53', '周小胖', 1030789996), ('家石我他妈又把自己关了', '2017-08-31 09:49:09', '2016', 46517378)]",'华为畅享7 Plus,',1,2)
    con=pymysql.connect(
        host='localhost',
        user='root',
        password="123456",
        database='qq_z',
        port=3306,
		 charset='utf8mb4',
		 cursorclass=pymysql.cursors.DictCursor,
    )
    cur=con.cursor()
    
    
    
    d=[i for i in os.listdir('mood_detail') if not i.endswith('.xls')]
    print(len(d))
    k=22670#说说id的计数
    for ii in d:
        
        fl=[i for i in os.listdir('mood_detail/'+ii) if i.endswith('.json')]
        print('mood_detail/'+ii)
        #开是写入q_user
        q_user_sql='insert into q_user(uin,uinname,check_time,total,last_createIime) values(%s,%s,now(),%s,%s)'
        frist_jsonfile=fl[0]
        first_w=open('mood_detail/'+ii+"/"+frist_jsonfile,'r',encoding='utf-8')
        first_s=first_w.read().strip()[17:-2]
        first_js=json.loads(first_s)
        if not 'msglist' in first_js:
            continue
        cur.execute(q_user_sql,(first_js['usrinfo']['uin'],first_js['usrinfo']['name'],first_js['total'],first_js['usrinfo']['createTime']))
        first_w.close()
        #下面开始写入s_info

        for i in fl:
            with open('mood_detail/'+ii+"/"+i,'r',encoding='utf-8') as w:
                s=w.read().strip()[17:-2]
                is_orignal=True
#                print("进入了一个新的josn  %s\n内容为%s"%(w,s))
#                print("进入了一个新的josn  %s\n"%(w))
                js=json.loads(s)
                if not 'msglist' in js:
                    break
                for s in js['msglist']:
                    #这里有一条说说
                    #m=-1
                    is_orignal=False
                    if not s['commentlist']:
                        s['commentlist']=list()  #这句话有什么用
                    if 'rt_con' in s:
                        is_orignal=False
                    else:
                        is_orignal=True
                        #pass#卢世志
#                    str_conlist=str([(x['content'] ,x['createTime2'],x['name'],x['uin'],x['source_name'] if 'source_name' in x else "") for x in list(s['commentlist'])])

                    #cur.execute(sql.format(int(i[:i.find('_')]),s['created_time'],str(s['content']),str_conlist,str(s['source_name']),int(s['cmtnum'])))#,str(s['name'])
                    if 'pictotal' in s and 'pic' in s:
                        pic_url= str([picitem['url1'] for picitem in s['pic']]) 
                        pictotal= str(s['pictotal'] if 'pictotal' in s else "") 
                    else:
                        pic_url=None
                        pictotal=None
                    #pic_url=[str([picitem['smallurl'] for picitem in s['pic']]) if 'pictotal' in s else None]
                    s_info_sql='insert into s_info (s_id,uin,uinname,create_time,createTime,is_oringinal,content,cmtnum,source_name,pic,pictotal,rt_sum,lbs_idname,lbs_name,lbs_pos_x,lbs_pos_y) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
                    cur.execute(s_info_sql,(k,str(i[:i.find('_')]),str(s['name']),str(s['created_time']),Time2ISOString(str(s['created_time'])),is_orignal,str(s['content']),int(s['cmtnum']),str(s['source_name'] if 'source_name' in s else None ),pic_url,pictotal,s['rt_sum'],s['lbs']['idname'] if 'lbs' in s and 'idname' in s['lbs'] else None,s['lbs']['name'] if 'lbs' in s and 'name' in s['lbs'] else None,s['lbs']['pos_x'] if 'lbs' in s and 'pos_x' in s['lbs'] else None,s['lbs']['pos_y'] if 'lbs' in s and 'pos_y' in s['lbs'] else None))
                    
                    con.commit()
                    #下面开始写入q_rt表
                    if not is_orignal:
                        q_rt_sql='insert into q_rt (rt_id,rt_content,rt_uin,rt_uinname,rt_source_name,rt_createtime,rt_list) values (%s,%s,%s,%s,%s,%s,%s)'
                        #pic_url=[str([picitem['smallurl'] for picitem in s['pic']]) if 'pictotal' in s else None]
                        rt_list_info=str([(rtitem['con'],rtitem['name'],rtitem['uin'],rtitem['source_name'],rtitem['time']) for rtitem in s['rtlist']]) if 'rtlist' in s else None
                        
                        cur.execute(q_rt_sql,(k,s['rt_con']['content'],s['rt_uin'],s['rt_uinname'],str(s['rt_source_name'] if 'rt_source_name' in s else None),s['rt_createTime'],rt_list_info))
                    #下面开始写入q_comment表
                    q=1
                    for x in list(s['commentlist']):
                        #if 'created_time' in x:
                        #这里产生一条评论
                        q_comment_sql='insert into q_comment(s_id,q_id,content,create_time,createTime,uin,name,pictotal,picurl,source_name) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
                        q_pictotal=(x['pictotal'] if 'pictotal' in x else None) 
                        q_pic_url=[str([picitem['s_url'] for picitem in x['pic']]) if 'pictotal' in x else None]
                        cur.execute(q_comment_sql,(k,q,x['content'],x['create_time'],Time2ISOString(x['create_time']),x['uin'],x['name'],q_pictotal,q_pic_url,str(x['source_name'] if 'source_name' in x else None)))
                        
                        #这里处理对评论的回复
                        if 'list_3' in x:
                            r=1
                            for list_reply in x['list_3']:
                                q_comment_reply_sql='insert into q_comment_reply(s_id,q_id,r_id,from_uin,from_uinname,content,create_time,createTime,source_name) values (%s,%s,%s,%s,%s,%s,%s,%s,%s)'
                                cur.execute(q_comment_reply_sql,(k,q,r,list_reply['uin'],list_reply['name'],list_reply['content'],list_reply['create_time'],Time2ISOString(list_reply['create_time']),str(list_reply['source_name'] if 'source_name' in list_reply else None)))
                                r=r+1
                        q=q+1    
                    k+=1
        shutil.rmtree('mood_detail/'+ii)
    w.close()
    con.close()


#dataToMySQL()

if __name__ == '__main__':
#    a=Time2ISOString('1487109758')
#    print(a)
     dataToMySQL()

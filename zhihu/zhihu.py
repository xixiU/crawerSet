# -*- coding: utf-8 -*-
"""
Created on Fri Aug 17 20:15:16 2018

@author: x

知乎
"""
import requests
from pandas import DataFrame as df

from bs4 import BeautifulSoup
import urllib.request
import json
import pickle as pl
import os,time
from datetime import datetime
import sys
from dbProcess import Db_process
sys.setrecursionlimit(1000000) #例如这里设置为一百万
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3394.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
    'Host': 'www.zhihu.com',
    'Upgrade-Insecure-Requests': '1'}

def Time2ISOString( s ):
    ''' 
    convert second to a ISO format time
    from: 23123123 to: 2006-04-12 16:46:40
    把给定的秒转化为定义的格式
    '''
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime( float(s) ) ) 
class Zhihu:
    def __init__(self):
        self.session = requests.Session()
        self.cur = Db_process()
    
    def get_question_info(self,soup):
        try:
            
            tags=soup.find_all('strong',attrs={'class':'NumberBoard-itemValue'})#.find('div',attrs={'class':'NumberBoard QuestionFollowStatus-counts NumberBoard--divider'})
            if len(tags)==2:
#                follower = tags[0].get_text().replace('关注者','').replace(',','')
#                view_times = tags[1].get_text().replace('被浏览','').replace(',','')
                follower = tags[0]['title']
                view_times = tags[1]['title']
                
            question = soup.find('div',attrs={'class':'QuestionPage'})
            #获取评论数
            comment_number = question.find('meta',itemprop='commentCount')['content']
            #获取回答数
            answers = question.find('meta',itemprop='answerCount')['content']
            question_createtime = question.find('meta',itemprop='dateCreated')['content']
            
            question_createtime = datetime.strptime(question_createtime, '%Y-%m-%dT%H:%M:%S.000Z').strftime('%Y-%m-%d %H:%M:%S')
            
            question_modifytime = question.find('meta',itemprop='dateModified')['content']
            question_modifytime = datetime.strptime(question_modifytime, '%Y-%m-%dT%H:%M:%S.000Z').strftime('%Y-%m-%d %H:%M:%S')
            #(question_id,follower, view_times,comment_number,answers,question_createtime,question_modifytime)
            self.cur.insert_question([self.question_id,int(follower),int(view_times),int(comment_number),int(answers),question_createtime,question_modifytime])
        except:
            print('')
            
    def get_soup(self,question_url):
#        info = self.session.get(question_url,headers=headers,verify=False)#
#        if info.status_code !=200:
#            print('error')
#            sys.exit()
##        print(response.info())
        try:
            response = urllib.request.urlopen(question_url,data=bytes(json.dumps(headers), encoding="utf-8"))
            soup=BeautifulSoup(response.read(),'lxml')#
            return soup
        except urllib.error.HTTPError as e:
            print(e.code)
            print('未获取到soup对象')
            sys.exit()
            
    def get_user(self,answer_node):
        if not isinstance(answer_node,dict):
            user = answer_node.find('div',attrs={'class':'ContentItem AnswerItem'})
#            print(user['data-zop'])#{"authorName":"财财猫馆","itemId":393543593,"title":"你人生中的第一套房是怎么买到的？","type":"answer"}
            answer_id = user['name']
            userheadline = user.find('div',attrs={'class':'RichText ztext AuthorInfo-badgeText'}).get_text()
            username_mata = user.find('meta',itemprop='name')['content']
            userimage_mata = user.find('meta',itemprop='image')['content']
            userfollower_mata = user.find('meta',itemprop='zhihu:followerCount')['content']
            url_mata = user.find_all('meta',itemprop='url')
            userurl_mata=url_mata[0]['content']
            answerurl_mata=url_mata[1]['content']
            answercreatetime_meta = user.find('meta',itemprop='dateCreated')['content']
            answermotifiedtime_meta = user.find('meta',itemprop='dateModified')['content']
            
            answercreatetime_meta = datetime.strptime(answercreatetime_meta, '%Y-%m-%dT%H:%M:%S.000Z').strftime('%Y-%m-%d %H:%M:%S')
            answermotifiedtime_meta = datetime.strptime(answermotifiedtime_meta, '%Y-%m-%dT%H:%M:%S.000Z').strftime('%Y-%m-%d %H:%M:%S')
            
            answercomment_meta = user.find('meta',itemprop='commentCount')['content']
            answerupvoteCount_meta = user.find('meta',itemprop='upvoteCount')['content']
            answer_info = user.find('div',attrs={'class':'RichContent-inner'})
            answer_info = answer_info.get_text()
            
        else:
            answer_id = answer_node['id']
            answerurl_mata = answer_node['url']
            
            author = answer_node['author']
            username_mata = author['name']
            userimage_mata = author['avatar_url']
            userurl_mata = author['url']
            userheadline = author['headline']
            userfollower_mata = author['follower_count']
            
            answercreatetime_meta = answer_node['created_time']
            answercreatetime_meta = Time2ISOString(answercreatetime_meta)
            
            answermotifiedtime_meta = answer_node['updated_time']
            answermotifiedtime_meta = Time2ISOString(answermotifiedtime_meta)
            answercomment_meta = answer_node['comment_count']
            answerupvoteCount_meta = answer_node['voteup_count']
            answer_info = answer_node['content']
        #username,userimage, userurl,userheadline,userfollower)
        self.cur.insert_user([username_mata,userimage_mata,userurl_mata,userheadline,userfollower_mata])
        #(question_id,answer_id, answerurl,answercreatetime,answermotifiedtime,answercomment,answerupvoteCount,answer_info
        self.cur.insert_answer([answer_id,answerurl_mata,answercreatetime_meta,answermotifiedtime_meta,answercomment_meta,answerupvoteCount_meta,answer_info],self.question_id)
            
#    def get_similar_question(self):
#        url = 'https://www.zhihu.com/api/v4/questions/275899485/similar-questions?include=data%5B*%5D.answer_count%2Cauthor%2Cfollower_count&limit=5'
#        params={'include':'data[*].answer_count,author,follower_count',
#                'limit':5}
    def get_all_answer(self,filename ='json_test.pl'):
#        url ='https://www.zhihu.com/api/v4/questions/%s/answers'%self.question_id
#        params = {'include':	'data[*].is_normal,admin_closed_comment,reward_info,is_collapsed,annotation_action,annotation_detail,collapse_reason,is_sticky,collapsed_by,suggest_edit,comment_count,can_comment,content,editable_content,voteup_count,reshipment_settings,comment_permission,created_time,updated_time,review_info,relevant_info,question,excerpt,relationship.is_authorized,is_author,voting,is_thanked,is_nothelp;data[*].mark_infos[*].url;data[*].author.follower_count,badge[?(type=best_answerer)].topics',
#                  'limit':	5,
#                  'offset':5,
#                  'sort_by':'default'}
        js_header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3394.0 Safari/537.36',
    'Accept': 'application/json',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Accept-Encoding': 'gzip, deflate',
    'Connection': 'keep-alive',
    'Host': 'www.zhihu.com',
    'x-requested-with': 'Fetch',
    'Referer':'https://www.zhihu.com/question/%s'%self.question_id,
    'x-ab-param':'top_an=0;top_root_few_topic=0;web_ask_flow=default;pin_efs=orig;top_hqt=0;top_hca=0;top_feedre_rtt=41;top_mlt_model=0;top_video_rew=0;top_gif=0;top_free_content=-1;top_user_gift=0;se_tf=1;top_billvideo=0;top_feedre=1;top_nuc=0;top_keyword=0;top_multi_model=0;top_recall=1;top_feedre_itemcf=31;top_yhgc=0;top_bill=0;top_memberfree=1;top_tffrt=0;ls_play_continuous_order=1;se_wiki_box=0;top_30=0;top_adpar=0;top_root_web=0;top_sj=2;top_tr=0;top_followtop=0;top_gr_model=0;se_gi=0;top_billupdate1=0;top_f_r_nb=1;pin_ef=orig;top_retagg=0;top_ntr=1;top_billread=1;top_nszt=0;top_nid=0;top_alt=0;top_root_mg=1;top_ebook=0;top_tmt=0;top_yc=0;top_gr_auto_model=0;top_newfollow=0;top_sjre=0;se_dt=0;top_card=-1;top_retag=0;top_vdio_rew=0;top_billab=0;top_is_gr=0;top_topic_feedre=21;top_universalebook=1;top_nucc=0;web_logoc=blue;top_root=0;top_root_ac=-1;top_tag_isolation=0;top_nad=1;top_uit=0;tp_sft=a;top_follow_reason=0;top_nmt=0;top_billupdate=0;top_feedre_cpt=101;top_dtmt=2;top_gr_topic_reweight=0;top_billpic=0;top_cc_at=-1;top_lowup=1;top_login_card=1;top_tagore=1;top_video_fix_position=0;top_feedtopiccard=0;top_keywordab=0'}
        all_url ='https://www.zhihu.com/api/v4/questions/%s/answers'%(self.question_id)+'?include=data%5B%2A%5D.is_normal%2Cadmin_closed_comment%2Creward_info%2Cis_collapsed%2Cannotation_action%2Cannotation_detail%2Ccollapse_reason%2Cis_sticky%2Ccollapsed_by%2Csuggest_edit%2Ccomment_count%2Ccan_comment%2Ccontent%2Ceditable_content%2Cvoteup_count%2Creshipment_settings%2Ccomment_permission%2Ccreated_time%2Cupdated_time%2Creview_info%2Crelevant_info%2Cquestion%2Cexcerpt%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%3Bdata%5B%2A%5D.mark_infos%5B%2A%5D.url%3Bdata%5B%2A%5D.author.follower_count%2Cbadge%5B%3F%28type%3Dbest_answerer%29%5D.topics&limit=5&offset=2&sort_by=default'#注意 offset设置为2了
#        response = self.session.get(url,params=params,headers=headers,verify=False)
        while True:
#            if not os.path.exists(filename):
#                response = self.session.get(all_url,headers=js_header,verify=False)#会乱码
#                with open(filename,'wb') as f_w:
#                    pl.dump(response,f_w,0)
#            else:
#                with open(filename,'rb') as f_r:
#                    response = pl.load(f_r)
            response = self.session.get('https://www.zhihu.com/api/v4/questions/275899485/answers?include=data%5B%2A%5D.is_normal%2Cadmin_closed_comment%2Creward_info%2Cis_collapsed%2Cannotation_action%2Cannotation_detail%2Ccollapse_reason%2Cis_sticky%2Ccollapsed_by%2Csuggest_edit%2Ccomment_count%2Ccan_comment%2Ccontent%2Ceditable_content%2Cvoteup_count%2Creshipment_settings%2Ccomment_permission%2Ccreated_time%2Cupdated_time%2Creview_info%2Crelevant_info%2Cquestion%2Cexcerpt%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%3Bdata%5B%2A%5D.mark_infos%5B%2A%5D.url%3Bdata%5B%2A%5D.author.follower_count%2Cbadge%5B%3F%28type%3Dbest_answerer%29%5D.topics&limit=5&offset=20702&sort_by=default',headers=js_header,verify=False)#会乱码
            page = response.json()
            print(page['paging']['is_end'])
            self.get_answer(page['data'])
            if page['paging']['is_end']=='True':
                break
            else:
                all_url = page['paging']['next']
 


    def get_answer(self,soup):
        if isinstance(soup,(dict,list)):
            #这里是一个dict对象
            for single_answer in soup:
                self.get_user(single_answer)
        else:
            answers = soup.find_all('div',attrs={'class':'List-item'})
            for answer in answers:
                self.get_user(answer)
            
    def get_question(self,question_url,filename ='275899485.pl'):
        self.question_id = question_url.split('/')[-1]
        if not os.path.exists(filename):
            soup = self.get_soup(question_url)
            with open(filename,'wb') as f_w:
                pl.dump(soup,f_w,0)
        else:
            with open(filename,'rb') as f_r:
                soup = pl.load(f_r)
        soup = self.get_soup(question_url) 
#        self.get_question_info(soup)
#        self.get_answer(soup)
        self.get_all_answer()

if __name__ =='__main__':
    myzhihu =Zhihu()
    myzhihu.get_question(question_url='https://www.zhihu.com/question/275899485')
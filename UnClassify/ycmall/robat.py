#coding=utf8
import itchat
import re,time
from  msyc import msyc

# tuling plugin can be get here:
# https://github.com/littlecodersh/EasierLife/tree/master/Plugins/Tuling
#from tuling import get_response

my8 =msyc()
my8.login()
@itchat.msg_register('Text')
def text_reply(msg):
    if u'作者' in msg['Text'] or u'主人' in msg['Text']:
        return u'调试中'
    elif u'源代码' in msg['Text'] or u'获取文件' in msg['Text']:
        itchat.send('@fil@main.py', msg['FromUserName'])
        return u'这就是现在机器人后台的代码，是不是很简单呢？'
    elif u'获取图片' in msg['Text']:
        itchat.send('@img@applaud.gif', msg['FromUserName']) # there should be a picture
    else:
        return u'收到：' + msg['Text']+time.ctime()+'\n微信调试中'

@itchat.msg_register(['Picture', 'Recording', 'Attachment', 'Video'])
def atta_reply(msg):
    return ({ 'Picture': u'图片', 'Recording': u'录音',
        'Attachment': u'附件', 'Video': u'视频', }.get(msg['Type']) +
        u'已下载到本地') # download function is: msg['Text'](msg['FileName'])

@itchat.msg_register(['Map', 'Card', 'Note', 'Sharing'])
def mm_reply(msg):
    if msg['Type'] == 'Map':
        return u'收到位置分享'
    elif msg['Type'] == 'Sharing':
        return u'收到分享' + msg['Text']
    elif msg['Type'] == 'Note':
        return u'收到：' + msg['Text']
    elif msg['Type'] == 'Card':
        return u'收到好友信息：' + msg['Text']['Alias']

@itchat.msg_register('Text', isGroupChat = True)
def group_reply(msg):
    if msg['isAt']:
        if isinstance(msg['Text'],str) and msg['Text'].find('https://m.msyc.cc/')!=-1:
            if len(msg['Text'].split())>2:
                print(msg['Text'])
                _,parchease_url,nums =msg['Text'].split()#去掉@xx部分
                nums= int(nums)
                print(parchease_url)
                goodid_info = urlProcess(parchease_url)
            else:
                goodid_info = urlProcess(msg['Text'])
                nums=1

            if isinstance(goodid_info,int):
                data = my8.create_order(goodid_info,nums)
                return  data
            else:
                return goodid_info
            pass
        elif msg['Text'].find('签到')!=-1:
            return my8.sign_in()
        else:
            print (u'@%s\u2005%s' % (msg['ActualNickName'],u'收到：' + msg['Text']))+time.ctime()+'\n微信调试中'
        return u'@%s\u2005%s' % (msg['ActualNickName'],u'收到：' + msg['Text'])

@itchat.msg_register('Friends')
def add_friend(msg):
    itchat.add_friend(**msg['Text'])
    itchat.send_msg(u'调试中\n'
        + u'源代码  ：回复源代码\n' + u'图片获取：回复获取图片\n'
        + u'欢迎Star我的项目关注更新！', msg['RecommendInfo']['UserName'])



def urlProcess(url):#https://m.msyc.cc//wx/foreign-detail.html?id=51258&tmn=1
    """
    从url中分离出商品id
    """
    pattern = re.compile('id=([0-9]*)')
    result = pattern.findall(url)
    if result:
        print(result[0])
        return int(result[0])
    else:
        return '未获取到商品id'+'@袁荣杰\u2005'

if __name__ == "__main__":
    itchat.auto_login(True)#, enableCmdQR=True
    itchat.run()
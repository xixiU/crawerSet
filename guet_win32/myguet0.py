# coding: utf-8

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
    if ok_id==1 and ok_pw==1 and ok_button==True:
        print("一次登陆尝试")

def get_message(hwnd):
    buf_size = win32gui.SendMessage(hwnd, win32con.WM_GETTEXTLENGTH) + 1  # 要加上截尾的字节  
    str_buffer = win32gui.PyMakeBuffer(buf_size)  # 生成buffer对象
    kk=win32api.SendMessage(hwnd, win32con.WM_GETTEXT, buf_size, str_buffer)  # 获取buffer
    print(kk)
    str_buffer = str(str_buffer[:-1])  # 转为字符串
    return str_buffer
    
class ipGUET(object):  
    def __init__(self, fgFilePath=None):  
        self.Mhandle = win32gui.FindWindow(None,'IP出校控制器')  
        print ("IP 出校器初始化完成,父类句柄为%x"%(self.Mhandle) )
#         TButton0_handle = find_subHandle(self.Mhandle, [("TButton",0)])
#         TButton1_handle = find_subHandle(self.Mhandle,[("TComboBox",0),("Edit",0)])
        TEdit_id_handle = find_subHandle(self.Mhandle, [("TEdit",1)])#用户名
        TEdit_pw_handle = find_subHandle(self.Mhandle, [("TEdit",0)])#密码
        TStatusBar_handle = find_subHandle(self.Mhandle, [("TStatusBar",0)])#版本信息
        TButton_lianjie_handle=win32gui.FindWindowEx(self.Mhandle,0,None,"连接")
        TButton_chaxun_handle=win32gui.FindWindowEx(self.Mhandle,0,None,"查询")
        GroupBox_handle= find_subHandle(self.Mhandle, [("TGroupBox_",0)])#余额
        print ("用户名句柄:%x\t密码句柄:%x\n连接按钮句柄:%x\t查询按钮句柄:%x \n版本信息句柄:%x\n余额句柄:%x" % (TEdit_id_handle,TEdit_pw_handle,TStatusBar_handle,TButton_lianjie_handle,TButton_chaxun_handle,GroupBox_handle))
        #guet_connect(self.Mhandle,TEdit_id_handle,'1316010139',TEdit_pw_handle,'182336 ',TButton_lianjie_handle)
        print(get_message(TEdit_id_handle))
        #print ("文本%s"%win32gui.GetWindowText(TStatusBar_handle))

if __name__=="__main__":
    #win32api.MessageBox(win32con.NULL, 'Python 你好！', '你好', win32con.MB_OK)  
     my_ipguet=ipGUET()
    







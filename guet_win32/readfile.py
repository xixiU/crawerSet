#coding=utf-8
import re
def remanager_file():
  file_object=open('222.txt')
  for line in file_object.readlines( ):
    pattern = r'成功找到：(.*?)密码：(.*?)$'
    result_list = re.compile(pattern).findall(line)
    if len(result_list)!=0:
      print(result_list[0][0])
      print(result_list[0][1])


if __name__=="__main__":
  remanager_file()

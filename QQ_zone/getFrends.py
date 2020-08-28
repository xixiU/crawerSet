#coding:utf-8
import json
import os
def get_Frends_list():
    k = 0
    file_list=[i for i in os.listdir('./frends/') if i.endswith('json')]
    frends_list=[]
    for f in file_list:
        #print(f)
        with open('./frends/{}'.format(f),'r',encoding='utf-8') as w:
            data=w.read()[95:-5]
            print(data)
            js=json.loads(data)
            #print(js)
            for i in js:
                k+=1
                frends_list.append(i)
    return frends_list


def get_list2():
    w=open('./friend2/unique.json','r')
    output_list=[]
    mydict={}
    for line in w.readlines():
        mydict['lable']=line.strip('\n')
        output_list.append(mydict)
    return output_list
frends_list=get_list2()
print(frends_list)

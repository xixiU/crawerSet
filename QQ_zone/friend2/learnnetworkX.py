# -*- coding: utf-8 -*-
"""
Created on Wed Oct  4 22:23:27 2017

@author: x
"""

import networkx as nx
import matplotlib.pyplot as plt
import  operator

plt.rcParams['font.sans-serif'] = ['SimHei']
#
#G = nx.DiGraph()
#mycsv=open('test.csv',encoding='utf-8')
#for line in mycsv.readlines():
#    csvlist=line.strip().rstrip().split('\t')
#    mycsvlist=[tuple(csvlist[0:2]),tuple(csvlist[2:4])]
##    mytuple=tuple(csvlist[0:2])
#    #print(mycsvlist)
#
#    if len(mycsvlist[0]) ==1 or len(mycsvlist[1]) ==1 or len(dict(mycsvlist))==1:
#        continue
##    print(len(mycsvlist))
##    print(len(dict(mycsvlist)))
##    road_nodes = {'%s': '%s', '%s': '%s'}%(csvlist[0],csvlist[1],csvlist[2],csvlist[3])
#    #road_nodes = {'a':{1:1}, 'b':{2:2}, 'c':{3:3}}
##    road_edges = [('csvlist[0]', 'csvlist[2]')]
#    road_nodes=dict(mycsvlist)
##    print(road_nodes)
##    for k,v in road_nodes.items(): 
##        one_node={'%s': '%s'}%(k,v)
##        print(one_node)
##        G.add_node(one_node)
##    print(road_nodes)
#    G.add_nodes_from(road_nodes)
##    print("节点个数%d"%G.number_of_nodes())
##    G.add_nodes_from(mycsvlist[0],mycsvlist[1])
#    road_edges_list=tuple(road_nodes.keys())
##    print("edge个数%d"%G.number_of_edges())
#    G.add_edge(road_edges_list[0],road_edges_list[1])
#
##print("number of edges:%d"%G.number_of_edges()) #10187
##print("number of nodes:%d"%G.number_of_nodes()) #8233
##nx.draw(G,'810170537')
#zhenzhen=nx.generators.ego.ego_graph(G,'939070749')
#nx.draw(zhenzhen)
#
#plt.savefig("赵真好友关系.png")
#plt.show()

#得到一个图
def Get_Graph():
    G = nx.Graph()
    mycsv=open('unique_friendrelationship.csv',encoding='utf-8')
    for line in mycsv.readlines():
        csvlist=line.strip().rstrip().split('\t')
        mycsvlist=[tuple(csvlist[0:2]),tuple(csvlist[2:4])]
    #    mytuple=tuple(csvlist[0:2])
    #    print(mycsvlist)
    
        if len(mycsvlist[0]) ==1 or len(mycsvlist[1]) ==1 or len(dict(mycsvlist))==1:
            continue
    #    print(len(mycsvlist))
    #    print(len(dict(mycsvlist)))
    #    road_nodes = {'%s': '%s', '%s': '%s'}%(csvlist[0],csvlist[1],csvlist[2],csvlist[3])
        #road_nodes = {'a':{1:1}, 'b':{2:2}, 'c':{3:3}}
    #    road_edges = [('csvlist[0]', 'csvlist[2]')]
        road_nodes=dict(mycsvlist)
    #    print(road_nodes)
    #    for k,v in road_nodes.items(): 
    #        one_node={'%s': '%s'}%(k,v)
    #        print(one_node)
    #        G.add_node(one_node)
#            print(road_nodes)
        G.add_nodes_from(road_nodes)
    #    print("节点个数%d"%G.number_of_nodes())
    #    G.add_nodes_from(mycsvlist[0],mycsvlist[1])
        road_edges_list=tuple(road_nodes.keys())
    #    print("edge个数%d"%G.number_of_edges())
        G.add_edge(road_edges_list[0],road_edges_list[1])
    return G
    
#method to add Graphy
def Get_Graph2(useQQuin=True):
    G = nx.Graph()
    mycsv=open('unique_friendrelationship.csv',encoding='utf-8')
    for line in mycsv.readlines():
        # uin0  name1 uin2 name3
        csvlist=line.strip().rstrip().split('\t')
        if len(csvlist)!=4:
            continue
        if useQQuin:
           G.add_edge(csvlist[0],csvlist[2])
           G.add_nodes_from([csvlist[0],csvlist[2]])
           G.node[csvlist[0]]['name']=csvlist[1]
           G.node[csvlist[2]]['name']=csvlist[3]
        else:
           G.add_edge(csvlist[1],csvlist[3])
           G.add_nodes_from([csvlist[0],csvlist[2]])
           G.node[csvlist[1]]['uin']=csvlist[0]
           G.node[csvlist[3]]['uin']=csvlist[2]
           
         
    return G
#图的基本信息

#传入一个图G
def basic_info(G):
    
    f=open('basic_info.txt','w')
    f.write('网络节点数：')
    f.write(str(G.number_of_nodes()) + '\n')
    f.write('网络边数：')
    f.write(str(G.size()) + '\n')
    f.write('网络边加权和：')
    f.write(str(G.size(weight='weight')) + '\n')
    scc=nx.strongly_connected_components(G)#返回强连通子图的list
    wcc=nx.weakly_connected_components(G)#返回弱连通子图的list
    print("弱连接: ")
    f.write('弱连接:'+'\n')
    for c in wcc:
#        print (c)
        f.write(str(c))
    f.write('\n')
    print("强连接: ")
    f.write('强连接:'+'\n')
    for s in scc:
#        print(str(s))
        f.write(str(s)+',')
#        node_value=nx.get_node_attributes(G,r'%s'%(''.join(s)))
#        print(node_value)
        
    f.write('\n')
    f.write('有向图平均路径长度：')
    f.write(str(nx.average_shortest_path_length(G)) + '\n')
    G=G.to_undirected()
    f.write('平均聚类系数：')
    f.write(str(nx.average_clustering(G)) + '\n')
    f.write('平均路径长度：')
    f.write(str(nx.average_shortest_path_length(G)) + '\n')
    
def egp_graoh(G,node):
    if G.has_node(node):
        print("存在")
#        nx.draw(ego,1,with_labels=True)
        for x in G.neighbors(node):
            print(x+'fhaujhfiuaehf')
        return nx.subgraph(G,G.neighbors(node) )
    else :
        print(00000)
        return G


def draw_ego_graph(G,character,hops=1,show_lables=True):
    """
    Expecting a graph_from-gdf
    """
    y="%s的%s代好友网络"%(character,hops)
    #Get the Ego Gaph and Position
    ego=nx.ego_graph(G,character,hops)
    pos = nx.spring_layout(ego)
    plt.figure(figsize=(12,12))
    plt.axis('off')
    
#    Draw
    nx.draw_networkx_edges(ego,pos,alpha=0.8,with_lables=True)
    nx.draw_networkx_nodes(ego,pos,with_lables =True,node_size=50,cmp=plt.cm.hot)
    if show_lables:   nx.draw_networkx_labels(ego,pos)
    plt.title('<C>={}'.format(y))
    plt.show()
    
def key_people(G):
    centrality=nx.degree_centrality(G)
    nx.set_node_attributes(G,'centrality',centrality)
    degrees =sorted(centrality.items(),key=operator.itemgetter(1),reverse =True)
    for item in degrees[0:10]:print("%s : %0.3f"%item)
    

if __name__=='__main__':
    myGraph=Get_Graph2(useQQuin=True)
#    basic_info(myGraph)
    
    draw_ego_graph(myGraph,'图样图森破',hops=1,show_lables=True)
    key_people(myGraph)
#    nx.draw(myGraph,with_labels=True)
#    myegp_graoh=egp_graoh(myGraph,'591608941')
#    draw_ego_graph(myGraph)
#    nx.draw(myegp_graoh,3)
#    plt.savefig("赵真好友关系.png")
#    plt.show()
#    basic_info(myGraph)
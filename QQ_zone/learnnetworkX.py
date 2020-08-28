# -*- coding: utf-8 -*-
"""
Created on Wed Oct  4 22:23:27 2017

@author: x
"""

import networkx as nx
import matplotlib.pyplot as plt
import operator

plt.rcParams['font.sans-serif'] = ['SimHei']


def get_graph():
    G = nx.DiGraph()
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
        print(road_nodes)
        G.add_nodes_from(road_nodes)
    #    print("节点个数%d"%G.number_of_nodes())
    #    G.add_nodes_from(mycsvlist[0],mycsvlist[1])
        road_edges_list=tuple(road_nodes.keys())
    #    print("edge个数%d"%G.number_of_edges())
        G.add_edge(road_edges_list[0],road_edges_list[1])
    return G

G=get_graph()
    #nx.draw(G,with_labels=True,)
#    print(G.number_of_nodes()) #245282
#    print(G.number_of_edges()) #292953
#    plt.savefig("youxiangtu.png")
#    plt.show()

#def show():
#    degrees = sorted(G.degree(),key=operator.itemgetter(0),reverse=True)
#    for node in degrees[0:10]:
#        print (nx.get_node_attributes(G, node))

#网络度量指标       
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
    f.write('弱连通子图个数：')
    f.write(str(len(wcc)) + '\n')
    f.write('强连通子图个数：')
    f.write(str(len(scc)) + '\n')
    largest_scc=scc[0]#返回最大的强连通子图
    f.write('最大强连通子图节点数：')
    f.write(str(len(largest_scc)) + '\n')
    f.write('有向图平均路径长度：')
    f.write(str(nx.average_shortest_path_length(G)) + '\n')
    G=G.to_undirected()
    f.write('平均聚类系数：')
    f.write(str(nx.average_clustering(G)) + '\n')
    f.write('平均路径长度：')
    f.write(str(nx.average_shortest_path_length(G)) + '\n')
from py2neo import Graph, NodeSelector, Node, Relationship
from py2neo.ogm import GraphObject, Property
from app import app

csvpath = 'd:/ex2/0.csv'
graph = Graph()

def csvunion(filename):
    fp = open(filename,'r',encoding='UTF-8')
    fp0 = open(csvpath,'a',encoding='UTF-8')
    for line in fp:
        if(line):
            fp0.writelines(line)
    fp.close()
    fp0.close()

def getnode(name):
    cql = "MATCH (n{name:'" + name + "'}) return n"
    res = graph.run(cql).data()
    # print(res)
    if (res):
        node = res[0].get('n')
    else:
        node = []
    return node

def getrelation(s,r,e):
    relations = graph.match(start_node=s, end_node=e, rel_type=r, bidirectional=True)
    if(relations):
        return relations
    else:
        return []

def inputnode(name,temp):
    if getnode(name) == []:
        node = Node(name=name, file=temp)
    else:
        node = getnode(name)
        node['file'] = temp
        graph.push(node)
    return node

def cqlrun(filename,temp):
    fp = open(filename,'r',encoding='UTF-8')
    lines = fp.readlines()
    for line in lines:
        if(line):
            tri = line.strip().split()
            if(len(tri)==3):
                if(getrelation(tri[0],tri[1],tri[2])!=[]):
                    startnode = inputnode(tri[0],temp)
                    # print(startnode)
                    endnode = inputnode(tri[2],temp)
                    # print(endnode)
                    rel = Relationship(startnode, tri[1], endnode)
                    # print(rel)
                    s = startnode | endnode | rel
                    graph.create(s)
            elif(len(tri)==4):
                if(getrelation(tri[0],tri[1]+tri[2],tri[3])!=[]):
                    startnode1 = inputnode(tri[0],temp)
                    # print(startnode)
                    startnode2 = inputnode(tri[2],temp)
                    endnode = inputnode(tri[3],temp)
                    endnode['relationship'] = tri[1]
                    graph.push(endnode)
                    # print(endnode)
                    rel1 = Relationship(startnode1, '主语', endnode)
                    rel2 = Relationship(startnode2, '宾语', endnode)
                    rel3 = Relationship(startnode1, tri[1], startnode2)
                    # print(rel)
                    s = startnode1 | startnode2 | endnode | rel1 | rel2 | rel3
                    graph.create(s)

def cqlgen(nlist):
    cql = ''
    for i in nlist:
        cql = cql + "match (n{file:'" + i + "'}) return n union "
    cql = cql[:-7]
    return cql
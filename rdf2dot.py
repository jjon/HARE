#!/opt/local/bin/python
# -*- coding: utf-8 -*- # 

from rdflib import Graph, Namespace
from rdflib.term import URIRef, Literal, BNode
from pprint import pprint
import yaml
import pydot

g = Graph().parse("/Users/jjc/Documents/Dissertation/Notes/1233HostageDeal/modelTesting/hostages10.n3", format='n3')

xml = Namespace('http://www.w3.org/XML/1998/namespace')
foaf = Namespace('http://xmlns.com/foaf/0.1/')
snotes = Namespace('http://my.sourcenotes.org/2006/04/sourcenotes#')
heml = Namespace('http://www.heml.org/schemas/2003-09-17/heml#')
rdf = Namespace('http://www.w3.org/1999/02/22-rdf-syntax-ns#')
rdfs = Namespace('http://www.w3.org/2000/01/rdf-schema#')
dc = Namespace('http://purl.org/dc/elements/1.1/')
dct = Namespace('http://purl.org/dc/terms/')
rel = Namespace('http://www.perceive.net/schemas/20021119/relationship#')
pome = Namespace('http://prosopOnto.medieval.england/2006/04/pome#')
crm = Namespace('http://cidoc.ics.forth.gr/rdfs/cidoc_v4.2.rdfs#')
me = Namespace('file:///Users/jjc/Documents/Dissertation/Notes/1233HostageDeal/modelTesting/1233Hostages.rdf#')


ralph = URIRef('file:///Users/jjc/Documents/Dissertation/Notes/1233HostageDeal/modelTesting/hostages10.n3#Mortimer_Ralph_d_1247')

def walkGraph(graph,start,subGraph) :
    try :
        for (p,o) in graph.predicate_objects(start):
            if (start,p,o) not in subGraph and (pome['Person'] in graph.objects(o,None) or crm['Event'] in graph.objects(o,None)):
                subGraph.add((start,p,o))
                walkGraph(graph,o,subGraph)
    except :
        pass
        
def g_to_dot(subGraph, dotOut):
    # generate nodes
    nodes = {}
    for s,p,o in subGraph.triples((None,None,None)):
        for x in s,o:
            x = subGraph.qname(x).encode('utf-8').replace(':','_')
            if x not in nodes.keys():
                nodes[x] = x
        ## make a dictionary assigning colors to objects of predicates, check to see if p is in it, add attribute to node
        if subGraph.qname(p) == "ns4:hostageGiver":
            print p #test
    for node in nodes:
        ## figure out how to use pydot's object dictionary for node attributes
        if 'exchange' in node:
            dotOut.add_node(pydot.Node(name=node, shape='box', style="filled", fillcolor="#cccc99"))
        else:
            dotOut.add_node(pydot.Node(name=node, shape='box'))
                
    # generate edges
    for s,p,o in subGraph.triples((None,None,None)):
        s = subGraph.qname(s).encode('utf-8').replace(':','_')
        p = subGraph.qname(p).encode('utf-8').replace(':','_')
        o = subGraph.qname(o).encode('utf-8').replace(':','_')
        dotOut.add_edge(pydot.Edge(nodes[s], nodes[o], label=p, fontsize="9pt"))
    #print nodes
    

subg = Graph()
d = pydot.Dot(graph_name="testgraph", graph_type="digraph", rankdir="BT", strict=True)
walkGraph(g,ralph,subg)
#print len(subg)

g_to_dot(subg,d)
#print d.to_string()
d.write_svg('/Users/jjc/Desktop/temp6.svg')
#d.write_dot('/Users/jjc/Desktop/temp9.dot')

## ================ Making a python dictionary out of the rdflib graph =============================
# exchanges = list(g.subjects(rdf['type'],crm['Event']))
# people = list(g.subjects(rdf['type'], pome['Person']))
# 
# def get_property_values(subject):
#     subject_dict = {}
#     for p,o in g.predicate_objects(subject):
#         if not isinstance(o, Literal):
#             subject_dict[g.qname(p)] = g.qname(o)
#         else:
#             subject_dict[g.qname(p)] = o.strip()
#     return subject_dict
#     
# ## Use this function to generate class instances with properties rather than dict. entries?
# 
# pgraph = {}
# for key in people:
#     pgraph[g.qname(key)] = get_property_values(key)
#     
# for key in exchanges:
#     pgraph[g.qname(key)] = get_property_values(key)
#pprint(pgraph)

## guido's findpath function
# def find_path(graph, start, end, path=[]):
#     path = path + [start]
#     if start == end:
#         return path
#     if not graph.has_key(start):
#         return None
#     for node in graph[start]:
#         if node not in path:
#             newpath = find_path(graph, node, end, path)
#             if newpath: return newpath
#     return None

## functionalize this so that it can be called recursively?
# for x in pgraph[u'Peter_fitz_Herbert'].itervalues():
#     if x in pgraph:
#         for y in pgraph[x].itervalues():
#             if y in pgraph and pgraph[y][u'rdf:type'] == u'pome:Person':
#                 print pgraph[y]

# class instances are hashable so create node instances and use them in a dictionary for a graph as guido suggests?
# 
# graph = {'A': ['B', 'C'],
#          'B': ['C', 'D'],
#          'C': ['D'],
#          'D': ['C'],
#          'E': ['F'],
#          'F': ['C']}
# >>> class Person(object):
# ...     pass
# ... 
# >>> p = Person()
# >>> p2 = Person()
# >>> {p:[p2]}
# {<__main__.Person object at 0x134c8d0>: [<__main__.Person object at 0x134c810>]}

## test yaml dump:
## print yaml.dump(pgraph)

## ========================= End python dictionary graph testing =============== 

        
## ===================== Recursion in an RDFlib graph ==========================
## inspired by the sparql thingie in rdfextras. Use this to generate sub-graphs in dot?
## interesting: walkGraph is non-deterministic, ie. I get a different path each time
# 

### this gives me the subgraph that I want. How to generate edges in pydot
# ralph = URIRef('file:///Users/jjc/Documents/Dissertation/Notes/1233HostageDeal/modelTesting/hostages10.n3#Mortimer_Ralph_d_1247')
# 
# def walkGraph(graph,start,subGraph) :
#     try :
#         for (p,o) in graph.predicate_objects(start):
#             if (start,p,o) not in subGraph and (pome['Person'] in g.objects(o,None) or crm['Event'] in g.objects(o,None)):
#                 subGraph.add((start,p,o))
#                 print (g.qname(start),g.qname(p),g.qname(o)) # debug
#                 walkGraph(graph,o,subGraph)
#     except :
#         pass
# 
# c = Graph()
# walkGraph(g,ralph,c)
# 
# c = Graph()
# d = pydot.Dot(graph_name="testgraph", graph_type="digraph", strict=True, suppress_disconnected=True)
# walkGraph(g,ralph,c)
# print c.serialize(format='n3')
#####################################################

# ralph = URIRef('file:///Users/jjc/Documents/Dissertation/Notes/1233HostageDeal/modelTesting/hostages10.n3#Mortimer_Ralph_d_1247')
# tuple_list = []
# def walkGraph(graph,start,subGraph) :
#     try :
#         for (p,o) in graph.predicate_objects(start):
#             if (start,p,o) not in subGraph and (pome['Person'] in g.objects(o,None) or crm['Event'] in g.objects(o,None)):
#                 subGraph.add((start,p,o))
#                 tuple_list.append((g.qname(start),g.qname(p),g.qname(o))) # debug
#                 walkGraph(graph,o,subGraph)
#         return tuple_list
#     except :
#         pass
# 
# c = Graph()
# print walkGraph(g,ralph,c)
# 
# c = Graph()
# walkGraph(g,ralph,c)
# d = pydot.Dot(graph_name="testgraph", graph_type="digraph", strict=True, suppress_disconnected=True)
# print c.serialize(format='n3')
#####################################################


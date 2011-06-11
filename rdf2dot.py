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

lookfor = {
    "hostage_exchange": {'height': '0.25', 'shape': 'box', 'label': 'exchange', 'group': True, 'fontsize': '9pt', 'style':'filled', 'fillcolor': "#cccc99"},
    "hostage": {'height': '0.25', 'style':'filled', 'fillcolor': "#cc99cc", 'shape':'box'}
}

def walkGraph(graph,start,subGraph) :
    try :
        for (p,o) in graph.predicate_objects(start):
            if (start,p,o) not in subGraph and (pome['Person'] in graph.objects(o,None) or crm['Event'] in graph.objects(o,None) or pome['Place'] in graph.objects(o,None)):
                subGraph.add((start,p,o))
                walkGraph(graph,o,subGraph)
    except :
        pass
        
        
def g_to_dot(subGraph, dotOut):
    # generate nodes:
    nodes = {}
    for s,o in subGraph.subject_objects():
        for x in s,o:
            qname = subGraph.qname(x).encode('utf-8')
            uriref = x
            type = list(g.objects(x, rdf['type']))
            predicates = list(g.predicates(x))
            x = qname.split(':')[1]
            if x not in nodes.keys():
                nodes[x] = {'qname':qname, 'types':type, 'uriref': uriref, 'predicates': predicates}
    for node in nodes:
        if crm['Event'] in nodes[node]['types']:
            
            n = pydot.Node(name=node)
            n.obj_dict['attributes'] = lookfor['hostage_exchange']
            dotOut.add_node(n)
            
        
        elif pome['hostage'] in list(g.predicates(None,nodes[node]['uriref'])):
            n = pydot.Node(name=node)
            n.obj_dict['attributes'] = lookfor['hostage']
            dotOut.add_node(n)

        else:
            n = pydot.Node(name=node, shape='box', height="0.25")
            dotOut.add_node(n)

    # generate edges
    for s,p,o in subGraph.triples((None,None,None)):
        s = subGraph.qname(s).encode('utf-8').split(':')[1]
        p = subGraph.qname(p).encode('utf-8').split(':')[1]
        o = subGraph.qname(o).encode('utf-8').split(':')[1]
        if p == "participated_in":
            continue
        else:
            dotOut.add_edge(pydot.Edge(s, o, label=p, fontsize="9pt"))
    
    
    ## trying to generate a subgraph for ranking nodes
#     for node in nodes:
#         print list(g.predicates(None,nodes[node]['uriref']))
#     sgraph = pydot.Subgraph('', rank="same")
#     for x in exchanges:
#         sgraph.add_node(pydot.Node('x'))    
#     dotOut.add_subgraph(sgraph)
    

    
subg = Graph()
d = pydot.Dot(graph_name="testgraph", graph_type="digraph", rankdir="BT", strict=False)

walkGraph(g,ralph,subg)
g_to_dot(subg,d)

## OUTPUT:
#print d.to_string()
d.write_svg('/Users/jjc/Desktop/temp8.svg', prog='dot')
#d.write_dot('/Users/jjc/Desktop/temp7.dot')


#!/opt/local/bin/python
# -*- coding: utf-8 -*- #

##yay! fixed that stupid encoding problem with sitecustomize.py. no more .encode('utf-8') calls!

from rdflib import Graph, Namespace, URIRef, Literal, BNode
import pydot

#### create namespaces for RDFlib #####
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


#### create RDFlib graph ####
tgraph = Graph()
tgraph.parse("/Users/jjc/Documents/Dissertation/Notes/1233HostageDeal/modelTesting/hostages11.n3", format='n3')

#### create empty Dot graph via pydot ####
d = pydot.Dot(graph_name="testgraph", graph_type="digraph", strict=True, suppress_disconnected=False, rankdir="TB")
d.set_node_defaults(shape="box")

#### set starting nodes, and empty rdflib Graph() for walkGraph() to populate
ralph = URIRef('file:///Users/jjc/Documents/Dissertation/Notes/1233HostageDeal/modelTesting/hostages11.n3#Mortimer_Ralph_d_1247')

stutevill = URIRef('file:///Users/jjc/Documents/Dissertation/Notes/1233HostageDeal/modelTesting/hostages11.n3#William_de_Stutevill')

henry = URIRef('file:///Users/jjc/Documents/Dissertation/Notes/1233HostageDeal/modelTesting/hostages11.n3#Henry_III')

engelard = URIRef('file:///Users/jjc/Documents/Dissertation/Notes/1233HostageDeal/modelTesting/hostages11.n3#Engelard_de_Cigogné')

segrave = URIRef('file:///Users/jjc/Documents/Dissertation/Notes/1233HostageDeal/modelTesting/hostages11.n3#Segrave_Stephen_d_1241')

wmgamages = URIRef('file:///Users/jjc/Documents/Dissertation/Notes/1233HostageDeal/modelTesting/hostages11.n3#William_de_Gamages')

walter = URIRef('file:///Users/jjc/Documents/Dissertation/Notes/1233HostageDeal/modelTesting/hostages11.n3#Beauchamp_Walter_de')

warwickcastle = URIRef('file:///Users/jjc/Documents/Dissertation/Notes/1233HostageDeal/modelTesting/hostages11.n3#Warwick_Castle')


subg = Graph()

#### Parameters: resources and properties we're interested in ###
NARYRELATION = pome['NaryRelation']
RELATIONS = [pome['Person'], pome['Place']]
FOCUS_PROPERTIES = [pome['hostage'], pome['pledge']]

####### Helper Functions #######
## SuRF probably has stuff to do this. Have to look into this
def isResource(graph, uri):
    return rdf['type'] in graph.predicates(uri)

def resourceType(graph, uri):
    if isResource(graph,uri):
        return graph.objects(uri,rdf['type']).next()
    else:
        return None

######## RDFlib and Dotgraph functions ########
def walkGraph(graph,start,subGraph):
    """ for a given resource 'start' in an rdf graph 'graph',
        a recursive function to populate 'subGraph'
        with the nodes connected to 'start'
    """
    try :
        for (p,o) in graph.predicate_objects(start):
            if (start,p,o) not in subGraph and (pome['Person'] in graph.objects(o,None) or NARYRELATION in graph.objects(o,None)):
                subGraph.add((start,p,o))
                walkGraph(graph,o,subGraph)
    except :
        pass
        
walkGraph(tgraph, ralph, subg)

### extract a list of resources we're interested in from the result of walkGraph
walkGraph_resources = []
for x,y in subg.subject_objects():
    walkGraph_resources.append(x)
    walkGraph_resources.append(y)


### Generate nodes and edges ###
def nodes_edges(rdfgraph, uri, dotgraph):
    ## Generate dotgraph nodes for the resources we're interested in
    n = pydot.Node( rdfgraph.qname(uri),
                label=rdfgraph.qname(uri),
                height='0',
                fontsize="12"
               )
    if n.get_name() not in dotgraph.obj_dict['nodes'].keys():
        dotgraph.add_node(n)

    properties = [(p,o) for p,o in rdfgraph.predicate_objects(uri) if resourceType(tgraph,o) in RELATIONS]

    ## Add edges
    for p,o in properties:
        dotgraph.add_edge(
            pydot.Edge(
                (n.get_name(),rdfgraph.qname(o)),
                taillabel=rdfgraph.qname(p).split(":")[1],
                fontsize="9pt",
                arrowsize=.66
            )
        )


### Generate nodes and edges for subjects of type NaryRelation ###
def nary_nodes_edges(rdfgraph, uri, dotgraph):
    properties = list(rdfgraph.predicate_objects(uri))

    ## Generate dotgraph nodes for subjects of type NaryRelation
    nodes = []
    for prop in properties:
        if prop[0] in FOCUS_PROPERTIES and resourceType(tgraph,prop[1]) in RELATIONS:
            n = pydot.Node( rdfgraph.qname(prop[1]),
                        focus=True,
                        label=rdfgraph.qname(prop[1]),
                        height='0',
                        fontsize='12'
                       )
            nodes.append(n)
        elif resourceType(tgraph,prop[1]) in RELATIONS:
            n = pydot.Node( rdfgraph.qname(prop[1]),
                        label=rdfgraph.qname(prop[1]),
                        rdfprop=str(rdfgraph.qname(prop[0])).split(":")[1],
                        height='0',
                        fontsize='12'
                       )
            nodes.append(n)
                            
    for node in nodes:
        if node.get_name() not in dotgraph.obj_dict['nodes'].keys():
            dotgraph.add_node(node)
            
    
    ## Add edges
    focus_node = [n for n in nodes if 'focus' in n.get_attributes()] # this is going to fail when there's no focus node
    peripheral_nodes = [n for n in nodes if 'focus' not in n.get_attributes()]
    
    for node in peripheral_nodes:
        
        d.add_edge(
            pydot.Edge(
                (node, focus_node[0]),
                taillabel=node.get_attributes()['rdfprop'],
                fontsize="9pt",
                arrowsize=.66
            )
        )

###### Generate the Dot Graph ######

for sub in tgraph.subjects():
#     if resourceType(tgraph,sub) == NARYRELATION:
#         nary_nodes_edges(tgraph, sub, d)
#     if resourceType(tgraph,sub) in RELATIONS:
#         nodes_edges(tgraph, sub, d)

### or, just the resources in the result of walkGraph:
    if sub in set(walkGraph_resources):
        if resourceType(tgraph,sub) == NARYRELATION:
            nary_nodes_edges(tgraph, sub, d)
        if resourceType(tgraph,sub) in RELATIONS:
            nodes_edges(tgraph, sub, d)
            
##### manipulate dotgraph after generating: color nodes and set other properties:
for x in d.get_edges():
    x.set_minlen(1.5)
    x.set_labeldistance('2')
    x.set_labelangle('0')
    if x.get_taillabel() in ['hostageGiver','hostageHolder','pledgeGiver']:
        n = d.get_node(x.get_source())[0]
        n.set_style("filled")
        n.set_fillcolor("#99cccc")
        n = d.get_node(x.get_destination())[0]
        n.set_style("filled")
        n.set_fillcolor("red")
    if x.get_taillabel() in ['custodyHolder','hostageHolder']:
        x.set_fontcolor("#088000")
    if x.get_taillabel() in ['pledgeGiver','hostageGiver']:
        x.set_fontcolor("#880000")

# d.get_node("Henry_III")[0].set_fillcolor("#ff9500")
# d.set_comment("gives or recieves hostages or pledges")
# d.add_edge(pydot.Edge("Henry_III", "Ralph_fitz_Nicholas", color="blue", label="steward of the household"))
d.add_edge(pydot.Edge("Henry_III", "Segrave_Stephen_d_1241", color="blue", label="justiciar"))
# d.add_edge(pydot.Edge("Henry_III", "Peter_fitz_Herbert", color="blue", label="tenant in chief"))
# d.add_edge(pydot.Edge("Henry_III", "Corbet_Thomas", color="blue", label="tenant in chief"))
d.add_edge(pydot.Edge("Henry_III", "Mortimer_Ralph_d_1247", color="blue", label="tenant in chief"))
# d.add_edge(pydot.Edge("Henry_III", "Hugh_Despenser", color="blue", label="tenant in chief"))
# d.add_edge(pydot.Edge("Henry_III", "Lacy_Walter_de_d_1241", color="blue", label="tenant in chief"))
# d.add_edge(pydot.Edge("Henry_III", "Engelard_de_Cigogné", color="blue", label="mercenary captain"))


#### Output the dotgraph to string or dot or svg ####
#print d.to_string()
d.write_dot('/Users/jjc/ComputerInfo/Python/pythonCourse/HARE/propgraph-ralph.dot', prog='dot')
#d.write_svg('/Users/jjc/ComputerInfo/Python/pythonCourse/HARE/propgraph.svg')

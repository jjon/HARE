#!/opt/local/bin/python
# -*- coding: utf-8 -*- #

from rdflib import Graph, Namespace
from rdflib.description import Description
from rdflib.term import URIRef, Literal, BNode
from StringIO import StringIO
import pydot
from pprint import pprint
from hashlib import md5

####### Helper Functions #######
def pairs(lst):
    i = iter(lst)
    first = prev = i.next()
    for item in i:
        yield prev, item
        prev = item
    yield item, first

def isResource(graph, uri):
    return rdf['type'] in graph.predicates(uri)

def isResourceOfType(graph, uri, resource_type):
    """ graph is an rdflib graph, 
        uri is a resource that has rdf['type'], 
        resource_type is the resource type to test for, eg pome['Person']
    """
    return resource_type in graph.objects(uri,rdf['type'])

def resourceType(graph, uri, resource_type):
    return graph.objects(uri,rdf['type']).next()



#### Namespaces for RDFlib #####
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

#### RDFlib graph from local string ####
# tgraph = Graph()
# tgraph.parse(StringIO("""
#     @prefix : <&#> .
#     @prefix Place: <http://prosopOnto.medieval.england/2006/04/pome/Place#> .
#     @prefix Sou: <http://my.sourcenotes.org/2006/04/sourcenotes/SourceNote#> .
#     @prefix crm: <http://cidoc.ics.forth.gr/rdfs/cidoc_v4.2.rdfs#> .
#     @prefix pome: <http://prosopOnto.medieval.england/2006/04/pome#> .
#     @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
#     @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
#     @prefix rel: <http://purl.org/vocab/relationship#> .
#     @prefix snotes: <http://my.sourcenotes.org/2006/04/sourcenotes#> .
# 
#     :William_de_Stutevill     a pome:Person;
#          crm:participated_in :hostage_exchange_1233a,
#                 :hostage_exchange_1233b;
#          rel:parentOf :Stutevill_Osmund_de;
#          rdfs:label "Stutevill de, William";
#          <http://xmlns.com/foaf/0.1/name> "William de Stutevill" .
# 
#     :Mortimer_Ralph_d_1247     a pome:Person;
#          crm:participated_in :hostage_exchange_1233a;
#          pome:lordOf :Brompton_Brian_de_1215-1277;
#          rel:childOf :Ferrières_Isabella_de,
#                 :Mortimer_Roger_d_1214;
#          rel:spouseOf :Gwladys_Ddu;
#          rdfs:label "Mortimer, Ralph (d.1247)" .
#     
#     :Henry_de_Brompton     a pome:Person;
#          crm:participated_in :hostage_exchange_1233a;
#          rel:childOf :Brompton_Brian_de_1215-1277;
#          rdfs:label "Henry (son of Brian) de Brompton";
#          <http://xmlns.com/foaf/0.1/name> "Henry de Brompton" .
#          
#     :Segrave_Stephen_d_1241     a pome:Person;
#          crm:participated_in :hostage_exchange_1233b,
#                 :hostage_exchange_1233k;
#          rdfs:label "Segrave, Stephen de d.1241" .
# 
#     :Stutevill_Osmund_de     a pome:Person;
#          crm:participated_in :hostage_exchange_1233b;
#          rel:childOf :William_de_Stutevill;
#          rdfs:label "Stutevill, Osmund de" .
#          
#     
#     
#     :hostage_exchange_1233b     a pome:NaryRelation;
#          pome:attestedIn Sou:d1e13573;
#          pome:hostage :Stutevill_Osmund_de;
#          pome:hostageGiver :William_de_Stutevill;
#          pome:hostageHolder :Segrave_Stephen_d_1241;
#          pome:isDiscussedIn "R. C. Stacey <cite>Finance and Politics in the reign of Henry III</cite>";
#          <http://purl.org/dc/elements/1.1/date> "1233-06-10";
#          rdfs:label "1233 hostages: William de Stutevill gives son Osmund de Stutevill to Stephen Segrave" .
#     
# 
# 
# 
#     :hostage_exchange_1233a     a pome:NaryRelation;
#          pome:attestedIn Sou:d1e13573;
#          pome:hostage :Henry_de_Brompton;
#          pome:hostageGiver :Mortimer_Ralph_d_1247;
#          pome:hostageHolder :William_de_Stutevill;
#          pome:isDiscussedIn "R. C. Stacey <cite>Finance and Politics in the reign of Henry III</cite>";
#          <http://purl.org/dc/elements/1.1/date> "1233-06-10";
#          rdfs:comment "Complex hostage exchange involving nearly 30 people, intimates of the crown as well as marcher lords. Each ternary relation (guarantor, hostage, captor) is recorded in a separate resource.";
#          rdfs:label "1233 hostages: Ralph Mortimer gives Henry de Brompton to William de Stutevill" .
# """), format="n3")



#### create Dot graph via pydot ####
d = pydot.Dot(graph_name="testgraph", graph_type="digraph", strict=True, suppress_disconnected=False, rankdir="TB")
d.set_node_defaults(shape="box")


# people = list(tgraph.subjects(rdf['type'], pome['Person']))##not using this
exchanges = list(tgraph.subjects(rdf['type'],pome['NaryRelation']))


def addNodesAndSubgraphs(rdfgraph, relation, resource_type, focus, dotgraph):
    """
    This breaks when resource type is other than Person.
    Add try/except? and/or figure out how to make the third
    and fourth arguments sequences and do the right thing
    for any resource_type and property. use resourceType()
    """
    properties = list(rdfgraph.predicate_objects(relation))
    print properties
    ## Generate dotgraph nodes
    nodes = []
    for prop in properties:
        if isResourceOfType(rdfgraph, prop[1], resource_type):
            if prop[0] == focus:
                nodes.append(
                    pydot.Node( rdfgraph.qname(prop[1]).encode('utf-8'),
                                focus=True,
                                style="filled",
                                fillcolor="#cc99cc",
                                label=rdfgraph.qname(prop[1]).encode('utf-8')
                               )
                )
            else:
                nodes.append(
                    pydot.Node( rdfgraph.qname(prop[1]).encode('utf-8'),
                                style="filled",
                                fillcolor="#cccc99",
                                label=rdfgraph.qname(prop[1]).encode('utf-8'),
                                rdfprop=str(rdfgraph.qname(prop[0])).split(":")[1]
                               )
                )
    
    for node in nodes:
        if node.get_name() not in dotgraph.obj_dict['nodes'].keys():
            dotgraph.add_node(node)

    ## Add subgraph
    sg1 = pydot.Subgraph(graph_name="sg1")
    dotgraph.add_subgraph(sg1)
    
    ## Add edges
    focus_node = [n for n in nodes if 'focus' in n.get_attributes()][0]
    peripheral_nodes = [n for n in nodes if 'focus' not in n.get_attributes()]
    
    for node in peripheral_nodes:
        #print node.get_attributes()['rdfprop']
        sg1.add_edge(
            pydot.Edge(
                (node, focus_node),
                taillabel=node.get_attributes()['rdfprop'],
                fontsize="9pt"
            )
        )
    
for exchange in exchanges:
    addNodesAndSubgraphs(tgraph, exchange, pome['Person'], pome['hostage'], d)


#### Output ####
#print d.to_string()
d.write_dot('/Users/jjc/Desktop/propgraph.dot', prog='dot')
#d.write_svg('/Users/jjc/Desktop/propgraph.svg')

############# Notes ###############rdflib.term.URIRef('http://prosopOnto.medieval.england/2006/04/pome#hostage'
# for ex in exchanges:
#     if pome['hostage'] in tgraph.predicates(ex):
#         persons = tgraph.objects(ex) ## trying to identify the person objects and get person predicate objects for them to put in the tool tip
#         hostage = tgraph.objects(ex,pome['hostage']).next().encode('utf-8').split('#')[-1]
#         
#         d.add_node(
#             pydot.Node( hostage,
#                         style="filled",
#                         fillcolor="#cccc99"
#                        )
#         )
# 
#         
#         d.add_edge(
#             pydot.Edge(
#                 tgraph.objects(ex,pome['hostageGiver']).next().encode('utf-8').split('#')[-1],
#                 hostage
#             )
#         )
#         
#         d.add_edge(
#             pydot.Edge(
#                 hostage,
#                 tgraph.objects(ex,pome['hostageHolder']).next().encode('utf-8').split('#')[-1]
#             )
#         )
        
        

# d.add_node(pydot.Node("Henry_III"))
# d.add_edge(pydot.Edge("Henry_III", "Ralph_fitz_Nicholas", color="blue", label="steward of the household"))
# d.add_edge(pydot.Edge("Henry_III", "Segrave_Stephen_d_1241", color="blue", label="justiciar"))
# d.add_edge(pydot.Edge("Henry_III", "Peter_fitz_Herbert", color="blue", label="tenant in chief"))
# d.add_edge(pydot.Edge("Henry_III", "Thomas_Corbet", color="blue", label="tenant in chief"))
# d.add_edge(pydot.Edge("Henry_III", "Mortimer_Ralph_d_1247", color="blue", label="tenant in chief"))
# d.add_edge(pydot.Edge("Henry_III", "Hugh_Despenser", color="blue", label="tenant in chief"))
# d.add_edge(pydot.Edge("Henry_III", "Lacy_Walter_de_d_1241", color="blue", label="tenant in chief"))
# d.add_edge(pydot.Edge("Henry_III", "Engelard_de_Cigogné", color="blue", label="mercenary captain"))
# 

#print d.to_string()
#d.write_dot('/Users/jjc/Desktop/propgraph.dot', prog='dot')


# for ex in exchanges:
# 	if pome['hostage'] in g.predicates(ex):
# 		print (
# 			g.objects(ex,pome['hostageGiver']).next().encode('utf-8'),
# 			g.objects(ex,pome['hostage']).next().encode('utf-8'),
# 			g.objects(ex,pome['hostageHolder']).next().encode('utf-8')
# 		)

# exchange = Description(g, URIRef('file:///Users/jjc/Documents/Dissertation/Notes/1233HostageDeal/modelTesting/hostages8.n3#hostage_exchange_1233e'))
# list(exchange
#print list(g.triples((URIRef('file:///Users/jjc/Documents/Dissertation/Notes/1233HostageDeal/modelTesting/hostages8.n3#hostage_exchange_1233e'),None,None)))

### GENERATE DOT FILE ###
# d = pydot.Dot(graph_name="testgraph", graph_type="digraph", strict=True, suppress_disconnected=True)
# 
# for s, p, o in g.triples((None,None,None)):
# 	d.add_edge(
# 		pydot.Edge(
# 			s.encode('utf-8').split('#')[-1],
# 			o.encode('utf-8').split('#')[-1],
# 			label=p.encode('utf-8').split('#')[-1]
# 		)
# 	)
# 
# # exceeds the size limit for png, use svg
# d.write_svg('/Users/jjc/Desktop/temp1.svg')

# run it through graphviz dot to get strict?
# processed_dot = d.create(format='dot')
# print processed_dot

### for the dot file, both edge and node can take an attribute as follows:
### tooltip="some string"


################## INFO ###################
# directory of pydot looks like this:
# ['CLUSTER_ATTRIBUTES', 'Cluster', 'Common', 'Dot', 'EDGE_ATTRIBUTES', 'Edge', 'Error', 'GRAPH_ATTRIBUTES', 'Graph', 'InvocationException', 'NODE_ATTRIBUTES', 'Node', 'Subgraph', '__author__', '__builtins__', '__doc__', '__file__', '__find_executables', '__license__', '__name__', '__package__', '__revision__', '__version__', 'copy', 'dot_keywords', 'dot_parser', 'find_graphviz', 'frozendict', 'graph_from_adjacency_matrix', 'graph_from_dot_data', 'graph_from_dot_file', 'graph_from_edges', 'graph_from_incidence_matrix', 'id_re_alpha_nums', 'id_re_dbl_quoted', 'id_re_html', 'id_re_num', 'id_re_with_port', 'needs_quotes', 'os', 'quote_if_necessary', 're', 'subprocess', 'tempfile']


# directory of an instance of pydot.Dot looks like this:
# ['__class__', '__delattr__', '__dict__', '__doc__', '__format__', '__get_attribute__', '__getattribute__', '__getstate__', '__hash__', '__init__', '__module__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__setstate__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', 'add_edge', 'add_node', 'add_subgraph', 'create', 'create_attribute_methods', 'create_canon', 'create_cmap', 'create_cmapx', 'create_cmapx_np', 'create_dia', 'create_dot', 'create_fig', 'create_gd', 'create_gd2', 'create_gif', 'create_hpgl', 'create_imap', 'create_imap_np', 'create_ismap', 'create_jpe', 'create_jpeg', 'create_jpg', 'create_mif', 'create_mp', 'create_pcl', 'create_pdf', 'create_pic', 'create_plain', 'create_plain-ext', 'create_png', 'create_ps', 'create_ps2', 'create_svg', 'create_svgz', 'create_vml', 'create_vmlz', 'create_vrml', 'create_vtx', 'create_wbmp', 'create_xdot', 'create_xlib', 'del_edge', 'del_node', 'formats', 'get', 'get_Damping', 'get_K', 'get_URL', 'get_aspect', 'get_attributes', 'get_bb', 'get_bgcolor', 'get_center', 'get_charset', 'get_clusterrank', 'get_colorscheme', 'get_comment', 'get_compound', 'get_concentrate', 'get_defaultdist', 'get_dim', 'get_dimen', 'get_diredgeconstraints', 'get_dpi', 'get_edge', 'get_edge_defaults', 'get_edge_list', 'get_edges', 'get_epsilon', 'get_esep', 'get_fontcolor', 'get_fontname', 'get_fontnames', 'get_fontpath', 'get_fontsize', 'get_graph_defaults', 'get_graph_type', 'get_id', 'get_label', 'get_labeljust', 'get_labelloc', 'get_landscape', 'get_layers', 'get_layersep', 'get_layout', 'get_levels', 'get_levelsgap', 'get_lheight', 'get_lp', 'get_lwidth', 'get_margin', 'get_maxiter', 'get_mclimit', 'get_mindist', 'get_mode', 'get_model', 'get_mosek', 'get_name', 'get_next_sequence_number', 'get_node', 'get_node_defaults', 'get_node_list', 'get_nodes', 'get_nodesep', 'get_nojustify', 'get_normalize', 'get_nslimit', 'get_nslimit1', 'get_ordering', 'get_orientation', 'get_outputorder', 'get_overlap', 'get_overlap_scaling', 'get_pack', 'get_packmode', 'get_pad', 'get_page', 'get_pagedir', 'get_parent_graph', 'get_quadtree', 'get_quantum', 'get_rank', 'get_rankdir', 'get_ranksep', 'get_ratio', 'get_remincross', 'get_repulsiveforce', 'get_resolution', 'get_root', 'get_rotate', 'get_searchsize', 'get_sep', 'get_sequence', 'get_showboxes', 'get_simplify', 'get_size', 'get_smoothing', 'get_sortv', 'get_splines', 'get_start', 'get_strict', 'get_stylesheet', 'get_subgraph', 'get_subgraph_list', 'get_subgraphs', 'get_suppress_disconnected', 'get_target', 'get_top_graph_type', 'get_truecolor', 'get_type', 'get_viewport', 'get_voro_margin', 'obj_dict', 'prog', 'progs', 'set', 'set_Damping', 'set_K', 'set_URL', 'set_aspect', 'set_bb', 'set_bgcolor', 'set_center', 'set_charset', 'set_clusterrank', 'set_colorscheme', 'set_comment', 'set_compound', 'set_concentrate', 'set_defaultdist', 'set_dim', 'set_dimen', 'set_diredgeconstraints', 'set_dpi', 'set_edge_defaults', 'set_epsilon', 'set_esep', 'set_fontcolor', 'set_fontname', 'set_fontnames', 'set_fontpath', 'set_fontsize', 'set_graph_defaults', 'set_graphviz_executables', 'set_id', 'set_label', 'set_labeljust', 'set_labelloc', 'set_landscape', 'set_layers', 'set_layersep', 'set_layout', 'set_levels', 'set_levelsgap', 'set_lheight', 'set_lp', 'set_lwidth', 'set_margin', 'set_maxiter', 'set_mclimit', 'set_mindist', 'set_mode', 'set_model', 'set_mosek', 'set_name', 'set_node_defaults', 'set_nodesep', 'set_nojustify', 'set_normalize', 'set_nslimit', 'set_nslimit1', 'set_ordering', 'set_orientation', 'set_outputorder', 'set_overlap', 'set_overlap_scaling', 'set_pack', 'set_packmode', 'set_pad', 'set_page', 'set_pagedir', 'set_parent_graph', 'set_prog', 'set_quadtree', 'set_quantum', 'set_rank', 'set_rankdir', 'set_ranksep', 'set_ratio', 'set_remincross', 'set_repulsiveforce', 'set_resolution', 'set_root', 'set_rotate', 'set_searchsize', 'set_sep', 'set_sequence', 'set_shape_files', 'set_showboxes', 'set_simplify', 'set_size', 'set_smoothing', 'set_sortv', 'set_splines', 'set_start', 'set_strict', 'set_stylesheet', 'set_suppress_disconnected', 'set_target', 'set_truecolor', 'set_type', 'set_viewport', 'set_voro_margin', 'shape_files', 'to_string', 'write', 'write_canon', 'write_cmap', 'write_cmapx', 'write_cmapx_np', 'write_dia', 'write_dot', 'write_fig', 'write_gd', 'write_gd2', 'write_gif', 'write_hpgl', 'write_imap', 'write_imap_np', 'write_ismap', 'write_jpe', 'write_jpeg', 'write_jpg', 'write_mif', 'write_mp', 'write_pcl', 'write_pdf', 'write_pic', 'write_plain', 'write_plain-ext', 'write_png', 'write_ps', 'write_ps2', 'write_raw', 'write_svg', 'write_svgz', 'write_vml', 'write_vmlz', 'write_vrml', 'write_vtx', 'write_wbmp', 'write_xdot', 'write_xlib']

## See also:
# http://www.graphviz.org/doc/info/lang.html for the dot language
# http://dkbza.org/pydot/pydot.html for pydot docs
# http://code.google.com/p/pydot/ for pydot code
# http://dkbza.org/pydot.html for pydot homepage
#!/opt/local/bin/python

from codecs import getreader
from StringIO import StringIO
from pprint import pprint
from rdflib.term import URIRef
from rdflib.graph import Graph, Namespace

#"/Users/jjc/Documents/Dissertation/Notes/1233HostageDeal/modelTesting/hostages8.n3"

# rdf = open("/Users/jjc/Documents/Dissertation/Notes/1233HostageDeal/modelTesting/hostages8.n3", mode='r')

# rdf_utf8 = rdf.encode('utf-8')
# 
# rdf_reader = getreader('utf-8')(rdf.read())
# rdf_reader.encode('utf-8')

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


g = Graph()
g.parse("/Users/jjc/Documents/Dissertation/Notes/1233HostageDeal/modelTesting/hostages8.n3", format='n3')

exchanges = list(g.subjects(rdf['type'],crm['Event']))
people = list(g.subjects(rdf['type'], pome['Person']))
pdict = {}
for x in people:
    person = x.split('#')[1]
    if person not in pdict:
        pdict[person] = True

pprint(pdict)
# 
#         
# def test_a():
#     g = Graph()
#     g.parse(data=rdf, format='n3')
#     v = g.value(subject=URIRef("http://www.test.org/#CI"), predicate=URIRef("http://www.w3.org/2004/02/skos/core#prefLabel"))
#     assert v==u"C\u00f4te d'Ivoire"
# 
# def test_b():
#     g = Graph()
#     g.parse(data=rdf_utf8, format='n3')
#     v = g.value(subject=URIRef("http://www.test.org/#CI"), predicate=URIRef("http://www.w3.org/2004/02/skos/core#prefLabel"))
#     assert v==u"C\u00f4te d'Ivoire"
# 
# def test_c():
#     g = Graph()
#     g.parse(source=rdf_reader, format='n3')
#     v = g.value(subject=URIRef("http://www.test.org/#CI"), predicate=URIRef("http://www.w3.org/2004/02/skos/core#prefLabel"))
#     assert v==u"C\u00f4te d'Ivoire"
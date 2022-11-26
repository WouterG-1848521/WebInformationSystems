# Create rdf file
from rdflib import Graph, Literal, RDF, URIRef
from rdflib.namespace import FOAF

g = Graph()
g.parse("graph.ttl")

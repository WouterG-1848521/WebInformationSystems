from rdflib import Graph, Namespace
from rdflib.namespace import FOAF, RDF, RDFS

geonames = "https://sws.geonames.org/"
wikidata = "http://www.wikidata.org/entity/"
local = "http://localhost/"


GEONAMES        = Namespace(geonames + "")
WIKIDATA        = Namespace(wikidata + "")

LOCAL           = Namespace(local + "")
PERSON          = Namespace(local + "person/")
DIPLOMA         = Namespace(local + "diploma/")
DEGREE          = Namespace(local + "degree/")
ENTERPRISE      = Namespace(local + "enterprise/")
VACANCY         = Namespace(local + "vacancy/")
EXPERIENCE      = Namespace(local + "experience/")


def create_graph(file_path):
    g = Graph()
    g.parse(file_path)
    
    # Bind prefix to namespace (shortend in turtle)
    
    # Global prefix
    g.bind("foaf"   , FOAF)
    g.bind("rdf"    , RDF)
    g.bind("rdfs"   , RDFS)
    g.bind("gn"     , GEONAMES)
    g.bind("wd"     , WIKIDATA)
    
    # Local prefix
    g.bind("local"          , LOCAL)
    g.bind("degree"         , DEGREE)
    g.bind("person"         , PERSON)
    g.bind("enterprise"     , ENTERPRISE)
    g.bind("vacancy"        , VACANCY)
    g.bind("diploma"        , DIPLOMA)
    g.bind("experience"     , EXPERIENCE)
    
    return g
from rdflib import Graph, Namespace
from rdflib.namespace import FOAF, RDF, RDFS

geonames = "https://sws.geonames.org/"
local = "http://localhost/"


GEONAMES        = Namespace(geonames + "")
LOCAL           = Namespace(local + "")
PERSON          = Namespace(local + "person/")
DIPLOMA         = Namespace(local + "diploma/")
PROFESSION      = Namespace(local + "profession/")
DEGREE          = Namespace(local + "degree/")
ENTERPRISE      = Namespace(local + "enterprise/")
VACANCY         = Namespace(local + "vacancy/")
LANGUAGE        = Namespace(local + "language/")
SKILL           = Namespace(local + "skill/")
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
    
    # Local prefix
    g.bind("local"          , LOCAL)
    g.bind("profession"     , PROFESSION)
    g.bind("degree"         , DEGREE)
    g.bind("person"         , PERSON)
    g.bind("enterprise"     , ENTERPRISE)
    g.bind("vacancy"        , VACANCY)
    g.bind("diploma"        , DIPLOMA)
    g.bind("language"       , LANGUAGE)
    g.bind("skill"          , SKILL)
    g.bind("experience"     , EXPERIENCE)
    
    return g
from rdflib import Graph, Namespace
from rdflib.namespace import FOAF, RDF, RDFS

local = "http://localhost/"

LOCAL           = Namespace(local + "")
PERSON          = Namespace(local + "person/")
PERSONAL_INFO   = Namespace(local + "personalInfo/")
DIPLOMA         = Namespace(local + "diploma/")
PROFESSION      = Namespace(local + "profession/")
DEGREE          = Namespace(local + "degree/")
ENTPERISE       = Namespace(local + "enterprise/")
ENTERPRISE_INFO = Namespace(local + "enterpriseInfo/")
VACANCY         = Namespace(local + "vacancy/")
VACANCY_INFO    = Namespace(local + "vacancyInfo/")
LANGUAGE        = Namespace(local + "language/")


def create_graph(file_path):
    g = Graph()
    g.parse(file_path)
    
    # Bind prefix to namespace (shortend in turtle)
    
    # Global prefix
    g.bind("foaf"   , FOAF)
    g.bind("rdf"    , RDF)
    g.bind("rdfs"   , RDFS)
    
    # Local prefix
    g.bind("local"          , LOCAL)
    g.bind("profession"     , PROFESSION)
    g.bind("degree"         , DEGREE)
    g.bind("person"         , PERSON)
    g.bind("personalInfo"   , PERSONAL_INFO)
    g.bind("enterprise"     , ENTPERISE)
    g.bind("enterpriseInfo" , ENTERPRISE_INFO)
    g.bind("vacancy"        , VACANCY)
    g.bind("vacancyInfo"    , VACANCY_INFO)
    g.bind("diploma"        , DIPLOMA)
    g.bind("language"       , LANGUAGE)
    
    return g
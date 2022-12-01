from rdflib import Graph, URIRef
from rdflib.namespace import RDF, RDFS, FOAF, XSD, OWL
from backend_REST.graph import LOCAL, PERSON, PERSONAL_INFO, DIPLOMA, DEGREE, PROFESSION, LANGUAGE, VACANCY, ENTPERISE
import owlrl
from pandas import DataFrame

graph = Graph()

# Global prefix
graph.bind("foaf"   , FOAF)
graph.bind("rdf"    , RDF)
graph.bind("rdfs"   , RDFS)

# Local prefix
graph.bind("local"          , LOCAL)
graph.bind("profession"     , PROFESSION)
graph.bind("degree"         , DEGREE)
graph.bind("person"         , PERSON)
graph.bind("personalInfo"   , PERSONAL_INFO)
graph.bind("enterprise"     , ENTPERISE)
graph.bind("vacancy"        , VACANCY)
graph.bind("diploma"        , DIPLOMA)
graph.bind("language"       , LANGUAGE)

# add the test data

# graph.add((diploma_URI, RDF.type, LOCAL.diploma))

diploma_1_ref = URIRef(DIPLOMA + "informatica")
graph.add((diploma_1_ref, RDF.type, URIRef(LOCAL + "diploma")))
diploma_2_ref = URIRef(DIPLOMA + "computerScience")
graph.add((diploma_2_ref, RDF.type, URIRef(LOCAL + "diploma")))
diploma_3_ref = URIRef(DIPLOMA + "info2")
graph.add((diploma_3_ref, RDF.type, URIRef(LOCAL + "diploma")))

graph.add((diploma_1_ref, OWL.equivalentClass, diploma_2_ref))
graph.add((diploma_2_ref, OWL.equivalentClass, diploma_3_ref))

user_info_ref = URIRef(PERSON + str(0))
graph.add((user_info_ref, RDF.type, URIRef(LOCAL + "person")))
graph.add((user_info_ref, URIRef(LOCAL + "diploma"), diploma_1_ref))

# vacancy_1_ref = URIRef(VACANCY + "0")
# graph.add((vacancy_1_ref, RDF.type, URIRef(LOCAL + "Vacancy")))
# vacancy_2_ref = URIRef(VACANCY + "1")
# graph.add((vacancy_2_ref, RDF.type, URIRef(LOCAL + "Vacancy")))

# graph.add((vacancy_1_ref, URIRef(LOCAL + "diploma"), diploma_1_ref))

# query = """
#     SELECT ?diploma2
#     WHERE {
#         person:0 local:diploma ?diploma .
#         ?diploma owl:equivalentClass ?diploma2 .
#     }
# """

# result = graph.query(query)

# for row in result:
#     print(row)
#     graph.add((user_info_ref, URIRef(LOCAL + "diploma"), row[0]))

# df = DataFrame(result)

# output = df.to_json(orient='index', indent=2)
# print(output)


# owlrl.DeductiveClosure(owlrl.RDFS_OWLRL_Semantics, rdfs_closure = True, axiomatic_triples = True, datatype_axioms = True).expand(graph)
# owlrl.DeductiveClosure(owlrl.OWLRL_Semantics, rdfs_closure = True, axiomatic_triples = True, datatype_axioms = True).expand(graph)
owlrl.CombinedClosure.RDFS_OWLRL_Semantics(graph, axioms=True, daxioms=True).closure()
# owlrl.CombinedClosure.RDFS_OWLRL_Semantics(graph, axioms=True, daxioms=True).add_axioms()


# owlrl.DeductiveClosure(owlrl.OWLRL_Extension, rdfs_closure = True, axiomatic_triples = True, datatype_axioms = True).expand(graph)


graph.serialize("test.ttl")


# query the graph

query = '''
    SELECT ?person ?diploma
    WHERE {
        ?person a local:person .
        ?person local:diploma ?diploma .
        ?diploma owl:equivalentClass diploma:info2 .
        }
'''

query = '''
        SELECT ?diploma
        WHERE {
            ?diploma owl:equivalentClass diploma:info2 .
            }
'''

query = '''
    SELECT ?person ?diploma
    WHERE {
        ?person a local:person .
        ?person local:diploma diploma:info2 .
        }
'''

print(query)

result = graph.query(query)

df = DataFrame(result)

output = df.to_json(orient='index', indent=2)
print(output)


# https://stackoverflow.com/questions/20474862/using-sparql-for-limited-rdfs-and-owl-reasoning
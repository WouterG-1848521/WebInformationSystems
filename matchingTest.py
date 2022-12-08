from rdflib import Graph, URIRef
from rdflib.namespace import RDF, RDFS, FOAF, XSD, OWL
from backend_REST.graph import LOCAL, PERSON, PERSONAL_INFO, DIPLOMA, DEGREE, PROFESSION, LANGUAGE, VACANCY, ENTERPRISE
import owlrl
from pandas import DataFrame

graph = Graph()

# Global prefix
graph.bind("foaf", FOAF)
graph.bind("rdf", RDF)
graph.bind("rdfs", RDFS)

# Local prefix
graph.bind("local", LOCAL)
graph.bind("profession", PROFESSION)
graph.bind("degree", DEGREE)
graph.bind("person", PERSON)
graph.bind("personalInfo", PERSONAL_INFO)
graph.bind("enterprise", ENTERPRISE)
graph.bind("vacancy", VACANCY)
graph.bind("diploma", DIPLOMA)
graph.bind("language", LANGUAGE)

# add the test data

# graph.add((diploma_URI, RDF.type, LOCAL.diploma))

# graph.add((URIRef(LOCAL + "diploma"), RDF.type, OWL.Class))

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


user_info_ref1 = URIRef(PERSON + str(1))
graph.add((user_info_ref1, RDF.type, URIRef(LOCAL + "person")))
graph.add((user_info_ref1, URIRef(LOCAL + "diploma"), diploma_2_ref))


user_info_ref2 = URIRef(PERSON + str(2))
graph.add((user_info_ref2, RDF.type, URIRef(LOCAL + "person")))
graph.add((user_info_ref2, URIRef(LOCAL + "diploma"), diploma_3_ref))

graph.add((user_info_ref, FOAF.knows, user_info_ref1))
graph.add((user_info_ref1, FOAF.knows, user_info_ref2))
graph.add((user_info_ref2, FOAF.knows, user_info_ref1))


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
owlrl.CombinedClosure.RDFS_OWLRL_Semantics(
    graph, axioms=True, daxioms=True).closure()
# owlrl.CombinedClosure.RDFS_OWLRL_Semantics(graph, axioms=True, daxioms=True).add_axioms()


# owlrl.DeductiveClosure(owlrl.OWLRL_Extension, rdfs_closure = True, axiomatic_triples = True, datatype_axioms = True).expand(graph)


graph.serialize("test.ttl")


# query the graph

# query = '''
#     SELECT ?person ?diploma
#     WHERE {
#         ?person a local:person .
#         ?person local:diploma ?diploma .
#         ?diploma owl:equivalentClass diploma:info2 .
#         }
# '''

# query = '''
#         SELECT ?diploma
#         WHERE {
#             ?diploma owl:equivalentClass diploma:info2 .
#             }
# '''

# diploma
course = "informatica"
print(diploma_1_ref)


query = f"""
    SELECT ?guysh
    WHERE {{
        ?person a local:person .
        ?person local:diploma diploma:{course} .
        ?others owl:equivalentClass diploma:{course} .
        ?guysh local:diploma ?others .
    }}
"""

# person who knows and has similar diploma(s)

person_id = "1"

query = f"""
    SELECT ?person 
    WHERE {{
        person:{person_id} a local:person .
        ?person foaf:knows person:{person_id} .
        person:{person_id} local:diploma ?diploma .
        ?diplomas owl:equivalentClass ?diploma .
        ?person local:diploma ?diplomas .
    }}
"""


print(query)

result = graph.query(query)

df = DataFrame(result)

output = df.to_json(orient='index', indent=2)
print(output)


# https://stackoverflow.com/questions/20474862/using-sparql-for-limited-rdfs-and-owl-reasoning

# Create rdf file
from rdflib import Graph, Literal, RDF, URIRef
from rdflib.namespace import FOAF
import owlrl
from pandas import DataFrame

prefixes = '''
                prefix foaf: <http://xmlns.com/foaf/0.1/> 
                prefix geo: <http://www.w3.org/2003/01/geo/wgs84_pos#> 
                prefix owl: <http://www.w3.org/2002/07/owl#> 
                prefix owl2: <http://www.w3.org/2006/12/owl2#> 
                prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> 
                prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> 
                prefix xsd: <http://www.w3.org/2001/XMLSchema#> 
                prefix local: <http://localhost/> 
                prefix profession: <http://localhost/profession/> 
                prefix degree: <http://localhost/degree/> 
                prefix enterprise: <http://localhost/enterprise/>
                prefix person: <http://localhost/person/> 
                prefix vacancy: <http://localhost/vacancy/> 
                prefix skill: <http://localhost/skill/> 
                prefix diploma: <http://localhost/diploma/> 
                prefix language: <http://localhost/language/> 
                prefix experience: <http://localhost/experience/>
            '''


graph = Graph()
graph.parse("rdf_graph.ttl")

query = ""
        # owlrl.DeductiveClosure(owlrl.OWLRL_Semantics).expand(g)
# owlrl.DeductiveClosure(owlrl.RDFS_Semantics).expand(g)
owlrl.DeductiveClosure(owlrl.RDFS_OWLRL_Semantics, rdfs_closure = True, axiomatic_triples = True, datatype_axioms = True).expand(graph)

query = prefixes + "\n"
query += f'''
                SELECT ?vacancy
                WHERE {{
                    ?vacancy rdf:type local:vacancy .
                    ?vacancy local:jobTitle ?jobTitle .
                    ?vacancy local:startDate ?startDate .
                    ?vacancy local:endDate ?endDate .
                    ?vacancy local:enterprise ?owner .

                    ?vacancy local:jobDescription ?jobDescription .
                    ?vacancy local:jobResponsibilities ?jobResponsibilities .
                    ?vacancy local:jobSalary ?jobSalary .
                    ?vacancy local:location ?jobLocation .

                    OPTIONAL {{
                        ?vacancy local:diploma ?diploma .
                    }}
                    OPTIONAL {{
                        ?vacancy local:skill ?skills .
                    }}
                    OPTIONAL {{
                        ?vacancy local:language ?language .
                    }}
                    OPTIONAL {{
                        ?vacancy local:experience ?experience .
                    }}

                    FILTER (?vacancy = <http://localhost/vacancy/2>)
                }}
        '''                
print(query)
                    
#?p rdf:label enterprise:{id} .

# sparql sheetsheet : https://www.iro.umontreal.ca/~lapalme/ift6281/sparql-1_1-cheat-sheet.pdf
print("\nexecuting query\n")
result = graph.query(query)
df = DataFrame(result, columns=result.vars)
print(df.to_json(orient='index', indent=2))


graph.serialize(destination="outputgraph.ttl")

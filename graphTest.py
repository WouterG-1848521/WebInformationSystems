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
                SELECT ?uri
                WHERE {{
                    ?uri rdf:type foaf:Person .
                    ?uri foaf:name ?name .
                    ?uri foaf:surname ?surname .
                    ?uri local:email ?email .
                    ?uri local:skill ?skill .
                    ?skill rdf:type local:skill .
                    OPTIONAL {{
                        ?skill owl:equivalentClass ?input .
                    }}
                    FILTER (?skill = <http://localhost/skill/teamwork> || ?input = <http://localhost/skill/teamwork>)
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

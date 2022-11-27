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
                prefix local: <http://localhost/#> 
                prefix profession: <http://localhost/profession/> 
                prefix degree: <http://localhost/degree/#> 
                prefix enterprise: <http://localhost/enterprise/#>
                prefix person: <http://localhost/person/#> 
                prefix enterpriseInfo: <http://localhost/enterpriseInfo/#> 
                prefix vacancy: <http://localhost/vacancy/#> 
                prefix vacancyInfo: <http://localhost/vacancyInfo/#> 
                prefix personalInfo: <http://localhost/personalInfo/#> 
            '''

graph = Graph()
graph.parse("graph.ttl")

query = """
            prefix local: <http://localhost/#>
            SELECT ?userInfo ?diploma ?degree ?profession ?institution ?startDate ?endDate
            where {
                ?userInfo a local:personalInfo .
                ?userInfo local:diploma ?diploma .
                ?diploma local:degree ?degree .
                ?diploma local:profession ?profession .
                ?diploma local:institution ?institution .
                ?diploma local:startDate ?startDate .
                ?diploma local:endDate ?endDate .
            }
        """
        # owlrl.DeductiveClosure(owlrl.OWLRL_Semantics).expand(g)
# owlrl.DeductiveClosure(owlrl.RDFS_Semantics).expand(g)
owlrl.DeductiveClosure(owlrl.RDFS_OWLRL_Semantics, rdfs_closure = True, axiomatic_triples = True, datatype_axioms = True).expand(graph)

query2 = """
            prefix local: <http://localhost/#>
            SELECT ?name ?surname
            where {
                ?user a foaf:Person .
                ?user foaf:name ?name .
                ?user local:hasSurName ?surname .
                ?connections local:connections ?user .
                ?connections rdfs:member  ?John .
                ?John foaf:name "John" .
            }
        """

query3 = """
            prefix local: <http://localhost/#>
            prefix profession: <http://localhost/profession#>
            prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            prefix owl: <http://www.w3.org/2002/07/owl#>
            SELECT ?profession
            where {
                ?profession rdfs:subClassOf local:profession .
            } 
            """

query4 = """
            prefix local: <http://localhost/#>
            prefix profession: <http://localhost/profession/>
            prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            prefix owl: <http://www.w3.org/2002/07/owl#>
            SELECT ?profession
            where {
                ?profession rdfs:subClassOf profession:doctor .
            } 
            """

query5 = """
            prefix local: <http://localhost/#>
            prefix profession: <http://localhost/profession/>
            prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            prefix owl: <http://www.w3.org/2002/07/owl#>
            SELECT ?name ?surName
            where {
                ?personalInfo a local:personalInfo .
                ?personalInfo local:diploma ?diploma .
                ?diploma rdf:type local:diploma .
                ?diploma local:degree degree:bachelor .
                ?person local:personalInfo ?personalInfo .
                ?person foaf:name ?name .
                ?person local:hasSurName ?surName .
            } 
            """

query6 = prefixes + '''
        SELECT ?p ?name ?lat ?long ?location ?owner ?enterpriseInfo ?maintainerName ?maintainerSurName
        WHERE {
            ?p rdf:type local:enterprise .
            ?p foaf:name ?name .
            ?p geo:lat ?lat .
            ?p geo:long ?long  .
            ?p geo:location ?location .
            ?p local:owner ?owner .
            ?p local:enterpriseInfo ?enterpriseInfo .
            ?p local:maintainer ?maintainer .
            ?maintainer foaf:name ?maintainerName .
            ?maintainer local:hasSurName ?maintainerSurName .
        }
    '''

id = 1
query7 = prefixes + f'''
                        SELECT ?p
                        WHERE {{
                            ?p rdf:label enterprise:{id} .
                        }}              
                    '''
# sparql sheetsheet : https://www.iro.umontreal.ca/~lapalme/ift6281/sparql-1_1-cheat-sheet.pdf
print("\nexecuting query\n")
result = graph.query(query4)
df = DataFrame(result, columns=result.vars)
print(df.to_json(orient='index', indent=2))


graph.serialize(destination="outputgraph.ttl")

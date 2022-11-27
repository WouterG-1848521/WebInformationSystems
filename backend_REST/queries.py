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
                prefix enterprise: <http://localhost/enterprise/#> .
                prefix person: <http://localhost/person/#> 
                prefix enterpriseInfo: <http://localhost/enterpriseInfo/#> 
                prefix vacancy: <http://localhost/vacancy/#> 
                prefix vacancyInfo: <http://localhost/vacancyInfo/#> 
                prefix personalInfo: <http://localhost/personalInfo/#> 
            '''

# /enterprise/get/all
def query_enterpriseGetAll():
    query = prefixes + f'''
        SELECT ?p ?name ?lat ?long ?location ?owner ?enterpriseInfo ?maintainerName ?maintainerSurName
        WHERE {{
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
        }}
    '''
    # TODO: per maintainer wordt er nu een apart result teruggegeven, kan dit misschien samengevoegd worden?
    return query

def query_enterpriseGetById(id):
    query = prefixes + f'''
        SELECT ?name ?lat ?long ?location ?owner ?enterpriseInfo ?maintainerName ?maintainerSurName
        WHERE {{
            ?p rdf:label enterprise:{id}
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
        }}
    '''
    # TODO: per maintainer wordt er nu een apart result teruggegeven, kan dit misschien samengevoegd worden?
    return query
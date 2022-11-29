from rdflib import Graph, Literal, RDF, URIRef
from rdflib.namespace import RDF, FOAF, RDFS, GEO
import owlrl
from pandas import DataFrame

from .graph import LOCAL, ENTPERISE, ENTERPRISE_INFO, PERSON

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
                prefix degree: <http://localhost/degree/> 
                prefix enterprise: <http://localhost/enterprise/>
                prefix person: <http://localhost/person/> 
                prefix enterpriseInfo: <http://localhost/enterpriseInfo/#> 
                prefix vacancy: <http://localhost/vacancy/> 
                prefix vacancyInfo: <http://localhost/vacancyInfo/> 
                prefix personalInfo: <http://localhost/personalInfo/> 
            '''

#########################################################
# helper functions
#########################################################
def check_maintainer(graph, enterpriseID, maintainerID):
    query = prefixes + "\n"
    query += f'''
                SELECT ?maintainer
                WHERE {{
                    ?enterprise rdf:type local:enterprise .
                    ?enterprise local:maintainer ?maintainer .
                    FILTER (?enterprise = enterprise:{enterpriseID})
                    FILTER (?maintainer = person:{maintainerID})
                }}
            '''
    result = graph.query(query)

    if (len(result) == 0):
        return False
    else:
        return True

def check_owner(graph, enterpriseID, ownerID):
    query = prefixes + "\n"
    query += f'''
                SELECT ?owner
                WHERE {{
                    ?enterprise rdf:type local:enterprise .
                    ?enterprise local:owner ?owner .
                    FILTER (?enterprise = enterprise:{enterpriseID})
                    FILTER (?owner = person:{ownerID})
                }}
            '''
    result = graph.query(query)

    if (len(result) == 0):
        return False
    else:
        return True

def check_person(graph, personID):
    query = prefixes + "\n"
    query += f'''
                SELECT ?person
                WHERE {{
                    ?person rdf:type foaf:Person .
                    FILTER (?person = person:{personID})
                }}
            '''
    result = graph.query(query)

    if (len(result) == 0):
        return False
    else:
        return True


#########################################################
# create functions
#########################################################
def create_enterpriseInfoRDF(graph, description):
    # Get enterpriseInfoID
    enterpriseInfoID = 5000

    # Add enterpriseInfo to Graph
    ref = URIRef(ENTERPRISE_INFO + str(enterpriseInfoID))
    graph.add((ref, RDF.type, LOCAL.enterpriseInfo))

    graph.add((ref, LOCAL.description, Literal(description)))

    graph.serialize(destination="enterprise.ttl")   # TODO : moet dit nu al ge serialized worden naar de echte graaf, of kunnen we dit periodiek laten gebueren
                                                    # TODO : voor testen nog niet naar echte graaf

    return enterpriseInfoID

def create_enterpriseRDF(graph, name, lat, long, location, owner, enterpriseInfoID):
    # Get enterpriseID
    enterpriseID = 5000
    
    # Add enterprise to Graph
    ref = URIRef(ENTPERISE + str(enterpriseID))
    enterpriseInfoRef = URIRef(ENTERPRISE_INFO + str(enterpriseInfoID))

    graph.add((ref, RDF.type, LOCAL.enterprise))
    graph.add((ref, FOAF.name, Literal(name)))
    graph.add((ref, GEO.lat, Literal(lat)))
    graph.add((ref, GEO.long, Literal(long)))
    graph.add((ref, GEO.location, Literal(location)))
    graph.add((ref, LOCAL.owner, URIRef(PERSON + str(owner))))
    graph.add((ref, LOCAL.maintainer, URIRef(PERSON + str(owner))))
    graph.add((ref, LOCAL.enterpriseInfo, enterpriseInfoRef))
    
    graph.serialize(destination="enterprise.ttl")   # TODO : moet dit nu al ge serialized worden naar de echte graaf, of kunnen we dit periodiek laten gebueren
                                                    # TODO : voor testen nog niet naar echte graaf
    return enterpriseID

#########################################################
# enterprise queries
#########################################################
def query_enterpriseGetAll():
    query = prefixes + '''
                            SELECT ?uri ?name ?lat ?long ?location ?owner ?enterpriseInfo ?maintainerName ?maintainerSurName
                            WHERE {
                                    ?uri rdf:type local:enterprise .
                                    ?uri foaf:name ?name .
                                    ?uri geo:lat ?lat .
                                    ?uri geo:long ?long  .
                                    ?uri geo:location ?location .
                                    ?uri local:owner ?owner .
                                    ?uri local:enterpriseInfo ?enterpriseInfo .
                                    ?uri local:maintainer ?maintainer .
                                    ?maintainer foaf:name ?maintainerName .
                                    ?maintainer foaf:surname ?maintainerSurName .
                                }
                        '''
    # TODO: per maintainer wordt er nu een apart result teruggegeven, kan dit misschien samengevoegd worden?
    return query

def query_enterpriseGetById(id):
    query = prefixes + f'''
                            SELECT ?uri ?name ?lat ?long ?location ?owner ?enterpriseInfo ?maintainerName ?maintainerSurName
                            WHERE {{
                                ?uri rdf:type local:enterprise .
                                ?uri foaf:name ?name .
                                ?uri geo:lat ?lat .
                                ?uri geo:long ?long  .
                                ?uri geo:location ?location .
                                ?uri local:owner ?owner .
                                ?uri local:enterpriseInfo ?enterpriseInfo .
                                ?uri local:maintainer ?maintainer .
                                ?maintainer foaf:name ?maintainerName .
                                ?maintainer foaf:surname ?maintainerSurName .
                                FILTER (?uri = enterprise:{id}) 
                            }}
                    '''
    # TODO: per maintainer wordt er nu een apart result teruggegeven, kan dit misschien samengevoegd worden?
    return query

def query_enterpriseGetByName(name):
    query = prefixes + f'''
                        SELECT ?uri ?lat ?long ?location ?owner ?enterpriseInfo ?maintainerName ?maintainerSurName
                        WHERE {{
                            ?uri rdf:type local:enterprise .
                            ?uri foaf:name "{name}" .
                            ?uri geo:lat ?lat .
                            ?uri geo:long ?long  .
                            ?uri geo:location ?location .
                            ?uri local:owner ?owner .
                            ?uri local:enterpriseInfo ?enterpriseInfo .
                            ?uri local:maintainer ?maintainer .
                            ?maintainer foaf:name ?maintainerName .
                            ?maintainer foaf:surname ?maintainerSurName
                        }}
                '''
    # TODO: per maintainer wordt er nu een apart result teruggegeven, kan dit misschien samengevoegd worden?
    return query

def query_enterpriseGetByLocation(location):
    query = prefixes + f'''
                        SELECT ?uri ?name ?lat ?long ?location ?owner ?enterpriseInfo ?maintainerName ?maintainerSurName
                        WHERE {{
                            ?uri rdf:type local:enterprise .
                            ?uri foaf:name ?name .
                            ?uri geo:lat ?lat .
                            ?uri geo:long ?long  .
                            ?uri geo:location "{location}" .
                            ?uri local:owner ?owner .
                            ?uri local:enterpriseInfo ?enterpriseInfo .
                            ?uri local:maintainer ?maintainer .
                            ?maintainer foaf:name ?maintainerName .
                            ?maintainer foaf:surname ?maintainerSurName
                        }}
                '''
    # TODO: per maintainer wordt er nu een apart result teruggegeven, kan dit misschien samengevoegd worden?
    return query

def query_update_enterpriseRDF(graph, name, lat, long, location, enterpriseInfoID, enterpriseID):
    query = prefixes + "\n"
    deletes = ""
    inserts = ""
    if (name != ""):
        deletes += "?enterprise foaf:name ?name .\n"
        inserts += f"?enterprise foaf:name \"{name}\" .\n"
    if (lat != ""):
        lat = float(lat)
        deletes += "?enterprise geo:lat ?lat .\n"
        inserts += f"?enterprise geo:lat {lat} .\n"
    if (long != ""):
        long = float(long)
        deletes += "?enterprise geo:long ?long .\n"
        inserts += f"?enterprise geo:long {long} .\n"
    if (location != ""):
        deletes += "?enterprise geo:location ?location .\n"
        inserts += f"?enterprise geo:location \"{location}\" .\n"
    if (enterpriseInfoID != ""):
        enterpriseInfoID = int(enterpriseInfoID)
        deletes += "?enterprise local:enterpriseInfo ?enterpriseInfo .\n"
        inserts += f"?enterprise local:enterpriseInfo enterpriseInfo:{enterpriseInfoID} .\n"

    query += ' DELETE { ' + "\n" + deletes + ' } ' + "\n"
    query += ' INSERT { ' + "\n" + inserts + ' } ' + "\n"
    query += f'''
                WHERE {{
                    ?enterprise rdf:type local:enterprise .
                    ?enterprise foaf:name ?name .
                    ?enterprise geo:lat ?lat .
                    ?enterprise geo:long ?long .
                    ?enterprise geo:location ?location .
                    ?enterprise local:enterpriseInfo ?enterpriseInfo .
                    FILTER (?enterprise = enterprise:{enterpriseID})
                }}
            '''
    return query

# deletes the enterprise, the enterpriseInfo and the connected vacancies, vacancyInfo
def query_delete_enterpriseRDF(graph, enterpriseID):
    query = prefixes + "\n"
    query += f'''
                DELETE {{
                    ?enterprise rdf:type local:enterprise .
                    ?enterprise foaf:name ?name .
                    ?enterprise geo:lat ?lat .
                    ?enterprise geo:long ?long .
                    ?enterprise geo:location ?location .
                    ?enterprise local:owner ?owner .
                    ?enterprise local:maintainer ?maintainer .
                    ?enterprise local:enterpriseInfo ?enterpriseInfo .
                    ?enterpriseInfo rdf:type local:enterpriseInfo .
                    ?enterpriseInfo local:enterpriseInfoDescription ?description .
                    ?vacancy rdf:type local:Vacancy .
                    ?vacancy local:available ?available .
                    ?vacancy local:creator ?enterprise .
                    ?vacancy local:endDate ?endDate .
                    ?vacancy local:startDate ?startDate .
                    ?vacancy local:vacancyInfo ?vacancyInfo .
                    ?vacancy geo:lat ?lat .
                    ?vacancy geo:long ?long .
                    ?vacancy geo:location ?location .
                    ?vacancyInfo rdf:type local:vacancyInfo .
                    ?vacancyInfo local:degree ?degree .
                    ?vacancyInfo local:jobDescription ?jobDescription .
                    ?vacancyInfo local:profession ?profession .
                }}
                WHERE {{
                    ?enterprise rdf:type local:enterprise .
                    ?enterprise foaf:name ?name .
                    ?enterprise geo:lat ?lat .
                    ?enterprise geo:long ?long .
                    ?enterprise geo:location ?location .
                    ?enterprise local:owner ?owner .
                    ?enterprise local:maintainer ?maintainer .
                    ?enterprise local:enterpriseInfo ?enterpriseInfo .
                    ?enterpriseInfo rdf:type local:enterpriseInfo .
                    ?enterpriseInfo local:enterpriseInfoDescription ?description .
                    OPTIONAL {{
                        ?vacancy rdf:type local:Vacancy .
                        ?vacancy local:available ?available .
                        ?vacancy local:creator ?enterprise .
                        ?vacancy local:endDate ?endDate .
                        ?vacancy local:startDate ?startDate .
                        ?vacancy local:vacancyInfo ?vacancyInfo .
                        ?vacancy geo:lat ?lat .
                        ?vacancy geo:long ?long .
                        ?vacancy geo:location ?location .
                        ?vacancyInfo rdf:type local:vacancyInfo .
                        ?vacancyInfo local:degree ?degree .
                        ?vacancyInfo local:jobDescription ?jobDescription .
                        ?vacancyInfo local:profession ?profession .
                    }}
                    FILTER (?enterprise = enterprise:{enterpriseID})
                }}
            '''
    return query

def query_transfer_ownershipRDF(graph, enterpriseID, newOwnerID):
    query = prefixes + "\n"
    query += f'''
                DELETE {{
                    ?enterprise local:owner ?owner .
                }}
                INSERT {{
                    ?enterprise local:owner person:{newOwnerID} .
                }}
                WHERE {{
                    ?enterprise rdf:type local:enterprise .
                    ?enterprise local:owner ?owner .
                    FILTER (?enterprise = enterprise:{enterpriseID})
                }}
            '''
    return query

def query_add_maintainerRDF(graph, enterpriseID, newMaintainerID):
    query = prefixes + "\n"
    query += f'''
                INSERT {{
                    ?enterprise local:maintainer person:{newMaintainerID} .
                }}
                WHERE {{
                    ?enterprise rdf:type local:enterprise .
                    FILTER (?enterprise = enterprise:{enterpriseID})
                }}
            '''
    return query

def query_remove_maintainerRDF(graph, enterpriseID, maintainerID):
    query = prefixes + "\n"
    query += f'''
                DELETE {{
                    ?enterprise local:maintainer person:{maintainerID} .
                }}
                WHERE {{
                    ?enterprise rdf:type local:enterprise .
                    FILTER (?enterprise = enterprise:{enterpriseID})
                }}
            '''
    return query

#########################################################
# enterprise page queries
#########################################################
def get_enterprisePageRDF(graph, enterprisePageID):
    query = prefixes + "\n"
    query += f'''
                SELECT ?description
                WHERE {{
                    ?enterpriseInfo local:enterpriseInfoDescription ?description .
                    FILTER (?enterprise = enterprise:{enterprisePageID})
                }}
            '''
    print(query)
    results = graph.query(query)
    return results


from rdflib import Graph, Literal, RDF, URIRef
from rdflib.namespace import RDF, FOAF, RDFS, GEO
import owlrl
from pandas import DataFrame

from backend_REST.graph import LOCAL, ENTPERISE, ENTERPRISE_INFO, PERSON

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
                prefix enterpriseInfo: <http://localhost/enterpriseInfo/> 
                prefix vacancy: <http://localhost/vacancy/> 
                prefix vacancyInfo: <http://localhost/vacancyInfo/> 
                prefix personalInfo: <http://localhost/personalInfo/> 
            '''

#########################################################
# helper functions
#########################################################
def check_maintainer(graph, enterpriseID, maintainerID):
    print("checking maintainer, enterpriseID: " + str(enterpriseID) + ", maintainerID: " + str(maintainerID))
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

def create_enterpriseRDF(graph, name, owner, lat, long, address, phone, email, website, description):
    # Get enterpriseID
    enterpriseID = 5000 # TODO: get from database
    
    # Add enterprise to Graph
    ref = URIRef(ENTPERISE + str(enterpriseID))

    graph.add((ref, RDF.type, LOCAL.enterprise))
    graph.add((ref, FOAF.name, Literal(name)))
    graph.add((ref, LOCAL.owner, URIRef(PERSON + str(owner))))
    graph.add((ref, LOCAL.maintainer, URIRef(PERSON + str(owner))))

    graph.add((ref, GEO.lat, Literal(lat)))
    graph.add((ref, GEO.long, Literal(long)))
    graph.add((ref, GEO.location, Literal(address)))
    graph.add((ref, LOCAL.description, Literal(description)))
    graph.add((ref, LOCAL.phone, Literal(phone)))
    graph.add((ref, LOCAL.email, Literal(email)))
    graph.add((ref, LOCAL.website, Literal(website)))
    
    graph.serialize(destination="graoh.ttl")   # TODO : moet dit nu al ge serialized worden naar de echte graaf, of kunnen we dit periodiek laten gebueren
    # TODO : hoe weten we zeker dat graph is aangepast
    return enterpriseID

#########################################################
# enterprise queries
#########################################################
def query_enterpriseGetAll():
    query = prefixes + '''
                            SELECT ?uri ?name ?owner  ?maintainerName ?maintainerSurName ?lat ?long ?address ?description ?phone ?email ?website
                            WHERE {
                                    ?uri rdf:type local:enterprise .
                                    ?uri foaf:name ?name .
                                    ?uri geo:lat ?lat .
                                    ?uri geo:long ?long  .
                                    ?uri geo:address ?address .
                                    ?uri local:owner ?owner .
                                    ?uri local:description ?description .
                                    ?uri local:phone ?phone .
                                    ?uri local:email ?email .
                                    ?uri local:website ?website .
                                    ?uri local:maintainer ?maintainer .
                                    ?maintainer foaf:name ?maintainerName .
                                    ?maintainer foaf:surname ?maintainerSurName .
                                }
                        '''
    # TODO: per maintainer wordt er nu een apart result teruggegeven, kan dit misschien samengevoegd worden?
    return query

def query_enterpriseGetById(id):
    query = prefixes + f'''
                            SELECT ?uri ?name ?lat ?long ?address ?owner ?maintainerName ?maintainerSurName
                            WHERE {{
                                ?uri rdf:type local:enterprise .
                                ?uri foaf:name ?name .
                                ?uri geo:lat ?lat .
                                ?uri geo:long ?long  .
                                ?uri geo:address ?address .
                                ?uri local:owner ?owner .
                                ?uri local:description ?description .
                                ?uri local:phone ?phone .
                                ?uri local:email ?email .
                                ?uri local:website ?website .
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
                        SELECT ?uri ?lat ?long ?address ?owner ?maintainerName ?maintainerSurName
                        WHERE {{
                                ?uri rdf:type local:enterprise .
                                ?uri foaf:name "{name}" .
                                ?uri geo:lat ?lat .
                                ?uri geo:long ?long  .
                                ?uri geo:address ?address .
                                ?uri local:owner ?owner .
                                ?uri local:description ?description .
                                ?uri local:phone ?phone .
                                ?uri local:email ?email .
                                ?uri local:website ?website .
                                ?uri local:maintainer ?maintainer .
                                ?maintainer foaf:name ?maintainerName .
                                ?maintainer foaf:surname ?maintainerSurName .
                        }}
                '''
    # TODO: per maintainer wordt er nu een apart result teruggegeven, kan dit misschien samengevoegd worden?
    return query

def query_enterpriseGetByLocation(location):
    query = prefixes + f'''
                        SELECT ?uri ?name ?lat ?long ?address ?owner ?maintainerName ?maintainerSurName
                        WHERE {{
                                ?uri rdf:type local:enterprise .
                                ?uri foaf:name ?name .
                                ?uri geo:lat ?lat .
                                ?uri geo:long ?long  .
                                ?uri geo:address "{location}" .
                                ?uri local:owner ?owner .
                                ?uri local:description ?description .
                                ?uri local:phone ?phone .
                                ?uri local:email ?email .
                                ?uri local:website ?website .
                                ?uri local:maintainer ?maintainer .
                                ?maintainer foaf:name ?maintainerName .
                                ?maintainer foaf:surname ?maintainerSurName .
                        }}
                '''
    # TODO: per maintainer wordt er nu een apart result teruggegeven, kan dit misschien samengevoegd worden?
    return query

def query_update_enterpriseRDF(name, lat, long, address, phone, email, website, description, enterpriseID):
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
    if (address != ""):
        deletes += "?enterprise geo:address ?location .\n"
        inserts += f"?enterprise geo:address \"{address}\" .\n"
    if (phone != ""):
        deletes += "?enterprise local:phone ?phone .\n"
        inserts += f"?enterprise local:phone \"{phone}\" .\n"
    if (email != ""):
        deletes += "?enterprise local:email ?email .\n"
        inserts += f"?enterprise local:email \"{email}\" .\n"
    if (website != ""):
        deletes += "?enterprise local:website ?website .\n"
        inserts += f"?enterprise local:website \"{website}\" .\n"
    if (description != ""):
        deletes += "?enterprise local:description ?description .\n"
        inserts += f"?enterprise local:description \"{description}\" .\n"

    query += ' DELETE { ' + "\n" + deletes + ' } ' + "\n"
    query += ' INSERT { ' + "\n" + inserts + ' } ' + "\n"
    query += f'''
                WHERE {{
                    ?enterprise rdf:type local:enterprise .
                    ?enterprise foaf:name ?name .
                    ?enterprise geo:lat ?lat .
                    ?enterprise geo:long ?long .
                    ?enterprise geo:address ?location .
                    ?enterprise local:phone ?phone .
                    ?enterprise local:email ?email .
                    ?enterprise local:website ?website .
                    ?enterprise local:description ?description .
                    FILTER (?enterprise = enterprise:{enterpriseID})
                }}
            '''
    return query

# deletes the enterprise, the enterpriseInfo and the connected vacancies, vacancyInfo
def query_delete_enterpriseRDF(enterpriseID):   # TODO : vacancies willen nog niet verwijdert worden
    query = prefixes + "\n"
    query += f'''
                DELETE {{
                    ?enterprise rdf:type local:enterprise .
                    ?enterprise foaf:name ?name .
                    ?enterprise geo:lat ?lat .
                    ?enterprise geo:long ?long .
                    ?enterprise geo:address ?location .
                    ?enterprise local:owner ?owner .
                    ?enterprise local:maintainer ?maintainer .
                    ?enterprise local:description ?description .
                    ?enterprise local:phone ?phone .
                    ?enterprise local:email ?email .
                    ?enterprise local:website ?website .

                    ?vacancy rdf:type local:Vacancy .
                    ?vacancy local:availability ?availability .
                    ?vacancy local:diploma ?diploma .
                    ?vacancy local:endDate ?endDate .
                    ?vacancy local:jobDescription ?jobDescription .
                    ?vacancy local:jobLocation ?jobLocation .
                    ?vacancy local:jobResponsibilities ?jobResponsibilities .
                    ?vacancy local:jobSalary ?jobSalary .
                    ?vacancy local:jobTitle ?jobTitle .
                    ?vacancy local:langauage ?longauage .
                    ?vacancy local:owner ?enterprise .
                    ?vacancy local:skills ?skills .
                    ?vacancy local:startDate ?startDate .
                }}
                WHERE {{
                    ?enterprise rdf:type local:enterprise .
                    ?enterprise foaf:name ?name .
                    ?enterprise geo:lat ?lat .
                    ?enterprise geo:long ?long .
                    ?enterprise geo:address ?location .
                    ?enterprise local:owner ?owner .
                    ?enterprise local:maintainer ?maintainer .
                    ?enterprise local:description ?description .
                    ?enterprise local:phone ?phone .
                    ?enterprise local:email ?email .
                    ?enterprise local:website ?website .
                    OPTIONAL {{
                        ?vacancy rdf:type local:Vacancy .
                        ?vacancy local:availability ?availability .
                        ?vacancy local:diploma ?diploma .
                        ?vacancy local:endDate ?endDate .
                        ?vacancy local:jobDescription ?jobDescription .
                        ?vacancy local:jobLocation ?jobLocation .
                        ?vacancy local:jobResponsibilities ?jobResponsibilities .
                        ?vacancy local:jobSalary ?jobSalary .
                        ?vacancy local:jobTitle ?jobTitle .
                        ?vacancy local:langauage ?longauage .
                        ?vacancy local:owner ?enterprise .
                        ?vacancy local:skills ?skills .
                        ?vacancy local:startDate ?startDate .
                    }}
                    FILTER (?enterprise = enterprise:{enterpriseID})
                }}
            '''
    print(query)
    return query

def query_transfer_ownershipRDF(enterpriseID, newOwnerID):
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

def query_add_maintainerRDF(enterpriseID, newMaintainerID):
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

def query_remove_maintainerRDF(enterpriseID, maintainerID):
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

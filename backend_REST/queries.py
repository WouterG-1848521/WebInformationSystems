from rdflib import Graph, Literal, RDF, URIRef
from rdflib.namespace import RDF, FOAF, RDFS
import owlrl
from pandas import DataFrame

from backend_REST.graph import LOCAL, PERSON, EXPERIENCE, VACANCY, DIPLOMA, GEO, ENTERPRISE
from config import GRAPH_FILE

graphFile = GRAPH_FILE

#########################################################
# helper functions
#########################################################

def check_maintainer(graph, enterpriseID, maintainerID):
    query = f'''
                SELECT ?maintainer
                WHERE {{
                    ?enterprise rdf:type foaf:Organization .
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
    query = f'''
                SELECT ?owner
                WHERE {{
                    ?enterprise rdf:type foaf:Organization .
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
    query = f'''
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

def check_enterprise(graph, enterpriseID):
    query = f'''
                SELECT ?enterprise
                WHERE {{
                    ?enterprise rdf:type foaf:Organization .
                    FILTER (?enterprise = enterprise:{enterpriseID})
                }}
            '''
    result = graph.query(query)

    if (len(result) == 0):
        return False
    else:
        return True

def check_valid_vacancy(graph, vacancyID):
    query = f'''
                SELECT ?vacancy
                WHERE {{
                    ?vacancy rdf:type local:vacancy .
                    FILTER (?vacancy = vacancy:{vacancyID})
                }}
            '''
    result = graph.query(query)

    if (len(result) == 0):
        return False
    else:
        return True

def check_diploma(graph, diplomaID):
    query = f'''
                SELECT ?diploma
                WHERE {{
                    ?diploma rdf:type local:diploma .
                    FILTER (?diploma = diploma:{diplomaID})
                }}
            '''
    result = graph.query(query)

    if (len(result) == 0):
        return False
    else:
        return True

def check_skill(graph, skillID):
    query = f'''
                SELECT ?skill
                WHERE {{
                    ?skill rdf:type local:skill .
                    FILTER (?skill = skill:{skillID})
                }}
            '''
    result = graph.query(query)

    if (len(result) == 0):
        return False
    else:
        return True

def check_language(graph, languageID):
    query = f'''
                SELECT ?language
                WHERE {{
                    ?language rdf:type local:language .
                    FILTER (?language = language:{languageID})
                }}
            '''
    result = graph.query(query)

    if (len(result) == 0):
        return False
    else:
        return True

def check_experience(graph, experienceID):
    query = f'''
                SELECT ?experience
                WHERE {{
                    ?experience rdf:type local:experience .
                    FILTER (?experience = experience:{experienceID})
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
# DEPRECATED
def create_enterpriseRDF(graph, name, owner, lat, long, address, phone, email, website, description, enterpriseID, location):
    # Add enterprise to Graph
    ref = URIRef(ENTERPRISE + str(enterpriseID))

    graph.add((ref, RDF.type, FOAF.Organization))
    graph.add((ref, FOAF.name, Literal(name)))
    graph.add((ref, LOCAL.owner, URIRef(PERSON + str(owner))))
    graph.add((ref, LOCAL.maintainer, URIRef(PERSON + str(owner))))

    graph.add((ref, GEO.lat, Literal(lat)))
    graph.add((ref, GEO.long, Literal(long)))
    graph.add((ref, GEO.address, Literal(address)))
    graph.add((ref, LOCAL.location, Literal("gn:" + location)))
    graph.add((ref, LOCAL.description, Literal(description)))
    graph.add((ref, LOCAL.phone, Literal(phone)))
    graph.add((ref, LOCAL.email, Literal(email)))
    graph.add((ref, LOCAL.website, Literal(website)))
    
    graph.serialize(destination=graphFile)
    return enterpriseID

#########################################################
# enterprise queries
#########################################################
def query_enterpriseGetAll():
    query = '''
                            SELECT ?uri ?name ?owner ?maintainer ?lat ?long ?address ?description ?phone ?email ?website ?location
                            WHERE {
                                    ?uri rdf:type foaf:Organization .
                                    ?uri foaf:name ?name .
                                    ?uri geo:lat ?lat .
                                    ?uri geo:long ?long  .
                                    ?uri geo:address ?address .
                                    ?uri local:location ?location .
                                    ?uri local:owner ?owner .
                                    ?uri local:description ?description .
                                    ?uri local:phone ?phone .
                                    ?uri local:email ?email .
                                    ?uri local:website ?website .
                                    ?uri local:maintainer ?maintainer .
                                }
                        '''
    return query

def query_enterpriseGetById(id):
    query =  f'''
                            SELECT ?uri ?name ?owner ?maintainer ?lat ?long ?address ?description ?phone ?email ?website ?location
                            WHERE {{
                                ?uri rdf:type foaf:Organization .
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
                                ?uri local:location ?location .
                                FILTER (?uri = enterprise:{id}) 
                            }}
                    '''
    return query

def query_enterpriseGetByName(name):
    query =  f'''
                        SELECT ?uri ?name ?owner ?maintainer ?lat ?long ?address ?description ?phone ?email ?website ?location
                        WHERE {{
                                ?uri rdf:type foaf:Organization .
                                ?uri foaf:name "{name}" .
                                ?uri foaf:name ?name .
                                ?uri geo:lat ?lat .
                                ?uri geo:long ?long  .
                                ?uri geo:address ?address .
                                ?uri local:location ?location .
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
    return query

def query_enterpriseGetByLocation(location):
    query =  f'''
                        SELECT ?uri ?name ?lat ?long ?address ?owner ?maintainerName ?maintainerSurName ?description ?phone ?email ?website
                        WHERE {{
                                ?uri rdf:type foaf:Organization .
                                ?uri foaf:name ?name .
                                ?uri geo:lat ?lat .
                                ?uri geo:long ?long  .
                                ?uri geo:address "{location}" .
                                ?uri local:location ?location .
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
    return query

def query_update_enterpriseRDF(name, lat, long, address, phone, email, website, description, enterpriseID, location):
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
        deletes += "?enterprise geo:address ?address .\n"
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
    if (location != ""):
        deletes += "?enterprise local:location ?location .\n"
        inserts += f"?enterprise local:location \"gn:{location}\" .\n"

    query = ' DELETE { ' + "\n" + deletes + ' } ' + "\n"
    query += ' INSERT { ' + "\n" + inserts + ' } ' + "\n"
    query += f'''
                WHERE {{
                    ?enterprise rdf:type foaf:Organization .
                    ?enterprise foaf:name ?name .
                    ?enterprise geo:lat ?lat .
                    ?enterprise geo:long ?long .
                    ?enterprise geo:address ?address .
                    ?enterprise local:phone ?phone .
                    ?enterprise local:email ?email .
                    ?enterprise local:website ?website .
                    ?enterprise local:description ?description .
                    ?enterprise local:location ?location .
                    FILTER (?enterprise = enterprise:{enterpriseID})
                }}
            '''
    return query

# deletes the enterprise, the enterpriseInfo and the connected vacancies, vacancyInfo
# DEPRECATED
def query_delete_enterpriseRDF(enterpriseID):
    query = f'''
                DELETE {{
                    ?enterprise rdf:type foaf:Organization .
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
                    ?vacancy local:diploma ?diploma .
                    ?vacancy local:endDate ?endDate .
                    ?vacancy local:jobDescription ?jobDescription .
                    ?vacancy local:location ?jobLocation .
                    ?vacancy local:jobResponsibilities ?jobResponsibilities .
                    ?vacancy local:jobSalary ?jobSalary .
                    ?vacancy local:jobTitle ?jobTitle .
                    ?vacancy local:langauage ?longauage .
                    ?vacancy local:owner ?enterprise .
                    ?vacancy local:skill ?skills .
                    ?vacancy local:startDate ?startDate .
                }}
                WHERE {{
                    ?enterprise rdf:type foaf:Organization .
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
                        ?vacancy local:diploma ?diploma .
                        ?vacancy local:endDate ?endDate .
                        ?vacancy local:jobDescription ?jobDescription .
                        ?vacancy local:location ?jobLocation .
                        ?vacancy local:jobResponsibilities ?jobResponsibilities .
                        ?vacancy local:jobSalary ?jobSalary .
                        ?vacancy local:jobTitle ?jobTitle .
                        ?vacancy local:langauage ?longauage .
                        ?vacancy local:owner ?enterprise .
                        ?vacancy local:skill ?skills .
                        ?vacancy local:startDate ?startDate .
                    }}
                    FILTER (?enterprise = enterprise:{enterpriseID})
                }}
            '''
    return query

def query_transfer_ownershipRDF(enterpriseID, newOwnerID):
    query = f'''
                DELETE {{
                    ?enterprise local:owner ?owner .
                }}
                INSERT {{
                    ?enterprise local:owner person:{newOwnerID} .
                }}
                WHERE {{
                    ?enterprise rdf:type foaf:Organization .
                    ?enterprise local:owner ?owner .
                    FILTER (?enterprise = enterprise:{enterpriseID})
                }}
            '''
    return query

def query_add_maintainerRDF(enterpriseID, newMaintainerID):
    query = f'''
                INSERT {{
                    ?enterprise local:maintainer person:{newMaintainerID} .
                }}
                WHERE {{
                    ?enterprise rdf:type foaf:Organization .
                    FILTER (?enterprise = enterprise:{enterpriseID})
                }}
            '''
    return query

def query_remove_maintainerRDF(enterpriseID, maintainerID):
    query = f'''
                DELETE {{
                    ?enterprise local:maintainer person:{maintainerID} .
                }}
                WHERE {{
                    ?enterprise rdf:type foaf:Organization .
                    FILTER (?enterprise = enterprise:{enterpriseID})
                }}
            '''
    return query

def query_enterpriseGetByAddress(address):
    query = f'''
        SELECT ?uri ?name ?owner ?maintainer ?lat ?long ?address ?description ?phone ?email ?website ?location
        WHERE {{
            ?uri rdf:type foaf:Organization .
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
            ?uri local:location ?location .
            FILTER (?address = "{address}") 
        }}
    '''
    return query

def query_enterpriseGetByLocation(location):
    query = f'''
            SELECT ?uri ?name ?owner ?maintainer ?lat ?long ?address ?description ?phone ?email ?website ?location
            WHERE {{
                ?uri rdf:type foaf:Organization .
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
                ?uri local:location ?location .
                FILTER (?location = "gn:{location}") 
            }}
    '''
    return query

def query_getVacanciesOfEnterprise(enterpriseID):
    query = f'''
            SELECT ?vacancy
            WHERE {{
                ?vacancy rdf:type local:vacancy .
                ?vacancy local:enterprise ?owner .
                FILTER (?owner = enterprise:{enterpriseID})
            }}
    '''
    return query

def query_enterpriseGetByOwner(personURI):
    query = f'''
            SELECT ?uri
            WHERE {{
                ?uri rdf:type foaf:Organization .
                ?uri local:owner ?owner .
                FILTER (?owner = {personURI}) 
            }}
    '''
    return query

#########################################################
# vacancy queries
#########################################################
def query_getVacancy(vacancyURI):
    query = f'''
                SELECT ?vacancy ?jobTitle ?startDate ?endDate ?owner ?diploma ?skills ?language ?experience ?jobDescription ?jobResponsibilities ?jobSalary ?jobLocation
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

                    FILTER (?vacancy = {vacancyURI})
                }} 
            '''
    return query

# def query_match_byVacancy(vacancyID):
#     query = prefixes + "\n"
#     query += f'''
#                 SELECT ?name ?surname ?email ?phone ?skill ?diploma ?language ?experience
#                 WHERE {{
#                     ?person rdf:type foaf:Person .
#                     ?person foaf:name ?name .
#                     ?person foaf:surname ?surname .
#                     ?person local:email ?email .
#                     ?vacancy rdf:type local:vacancy .
#                     ?person local:getVacancies ?g .
#                     OPTIONAL {{
#                         ?person local:skill ?skill .
#                         ?person local:diploma ?diploma .
#                         ?person local:languague ?languague .
#                         ?person local:experience ?experience .
#                         ?vacancy local:skill ?skill .
#                         ?vacancy local:diploma ?diploma .
#                         ?vacancy local:langauage ?languague .
#                     }}
#                     FILTER (?vacancy = vacancy:{vacancyID} && ?g = true)
#                 }}
#             '''
#     return query

def query_getDiplomasFromVacancy(vacancyID):
    query = f'''
                SELECT ?diploma
                WHERE {{
                    ?vacancy rdf:type local:vacancy .
                    ?vacancy local:diploma ?diploma .
                    FILTER (?vacancy = vacancy:{vacancyID})
                }}
            '''
    return query

def query_getDisciplinesFromVacancy(vacancyID):
    query = f'''
                SELECT ?discipline
                WHERE {{
                    ?vacancy rdf:type local:vacancy .
                    ?vacancy local:diploma ?diploma .
                    ?diploma local:discipline ?discipline .
                    FILTER (?vacancy = vacancy:{vacancyID})
                }}
            '''
    return query

def query_getSkillsFromVacancy(vacancyID):
    query = f'''
                SELECT ?skill
                WHERE {{
                    ?vacancy rdf:type local:vacancy .
                    ?vacancy local:skill ?skill .
                    FILTER (?vacancy = vacancy:{vacancyID})
                }}
            '''
    return query

def query_getLanguagesFromVacancy(vacancyID):
    query = f'''
                SELECT ?lang
                WHERE {{
                    ?vacancy rdf:type local:vacancy .
                    ?vacancy local:language ?lang .
                    FILTER (?vacancy = vacancy:{vacancyID})
                }}
            '''
    return query

# deprecated
def query_getExperienceFromVacancy(vacancyID):
    query = f'''
                SELECT ?exp
                WHERE {{
                    ?vacancy rdf:type local:vacancy .
                    ?vacancy local:experience ?exp .
                    FILTER (?vacancy = vacancy:{vacancyID})
                }}
            '''
    return query

# deprecated
def query_getSkillsFromexperiencesOfVacancy(vacancyID):
    query = f'''
                SELECT ?skill
                WHERE {{
                    ?vacancy rdf:type local:vacancy .
                    ?vacancy local:experience ?exp .
                    ?exp local:skill ?skill .
                    FILTER (?vacancy = vacancy:{vacancyID})
                }}
            '''
    return query

def query_vacancyByDiploma(diplomaURI):
    query = f'''
                SELECT ?vacancy
                WHERE {{
                    ?vacancy rdf:type local:vacancy .
                    ?vacancy local:diploma ?diploma .
                    ?vacancy local:available ?v .
                    OPTIONAL {{
                        ?diploma owl2:equivalentClass ?input .
                    }}
                    OPTIONAL {{
                        ?input owl2:equivalentClass ?diploma .
                    }}
                    FILTER ((?input = {diplomaURI} || ?diploma = {diplomaURI}) && ?v = true)
                }}
            '''
    return query

def query_vacancyByDiscipline(disciplineURI):
    query = f'''
                SELECT ?vacancy
                WHERE {{
                    ?vacancy rdf:type local:vacancy .
                    ?vacancy local:diploma ?diploma .
                    ?diploma local:discipline ?discipline .
                    ?vacancy local:available ?v .
                    OPTIONAL {{
                        ?discipline owl2:equivalentClass ?input .
                    }}
                    OPTIONAL {{
                        ?input owl2:equivalentClass ?discipline .
                    }}
                    FILTER ((?input = {disciplineURI} || ?discipline = {disciplineURI}) && ?v = true)
                }}
            '''
    return query

def query_vacancyBySkill(skillURI):
    query = f'''
                SELECT ?vacancy
                WHERE {{
                    ?vacancy rdf:type local:vacancy .
                    ?vacancy local:skill ?skill .
                    ?vacancy local:available ?v .
                    OPTIONAL {{
                        ?skill owl2:equivalentClass ?input .
                    }}
                    OPTIONAL {{
                        ?input owl2:equivalentClass ?skill .
                    }}
                    FILTER ((?input = {skillURI} || ?skill = {skillURI}) && ?v = true)
                }}
            '''
    return query

def query_vacancyByLanguage(languageURI):
    query = f'''
                SELECT ?vacancy
                WHERE {{
                    ?vacancy rdf:type local:vacancy .
                    ?vacancy local:language ?language .
                    ?vacancy local:available ?v .
                    OPTIONAL {{
                        ?language owl2:equivalentClass ?input .
                    }}
                    OPTIONAL {{
                        ?input owl2:equivalentClass ?language .
                    }}
                    FILTER ((?input = {languageURI} || ?language = {languageURI}) && ?v = true)
                }}
            '''
    return query

def query_vacancyByExperience(experienceURI):
    query = f'''
                SELECT ?vacancy
                WHERE {{
                    ?vacancy rdf:type local:vacancy .
                    ?vacancy local:experience ?experience .
                    ?vacancy local:available ?v .
                    OPTIONAL {{
                        ?experience owl2:equivalentClass ?input .
                    }}
                    OPTIONAL {{
                        ?input owl2:equivalentClass ?experience .
                    }}
                    FILTER ((?input = {experienceURI} || ?experience = {experienceURI}) && ?v = true)
                }}
            '''
    return query

#########################################################
# person queries
#########################################################
# returnen enkel de personen die aanstaan hebben dat ze vacancies willen

def query_personByDiploma(diplomas):
    query = f'''
                SELECT ?uri ?name ?surname ?email
                WHERE {{
                    ?uri rdf:type foaf:Person .
                    ?uri foaf:name ?name .
                    ?uri foaf:surname ?surname .
                    ?uri local:email ?email .
                    ?uri local:diploma ?diploma .
                    ?diploma rdf:type local:diploma .
                    ?uri local:getVacancies ?v
                    OPTIONAL {{
                        ?diploma owl2:equivalentClass ?input .
                    }}
                    OPTIONAL {{
                        ?input owl2:equivalentClass ?diploma .
                    }}
                    FILTER ((?diploma = {diplomas} || ?input = {diplomas}) && ?v = true)
                }}
            '''
    return query

def query_personByDiscipline(disciplines):
    query = f'''
                SELECT ?uri ?name ?surname ?email
                WHERE {{
                    ?uri rdf:type foaf:Person .
                    ?uri foaf:name ?name .
                    ?uri foaf:surname ?surname .
                    ?uri local:email ?email .
                    ?uri local:diploma ?diploma .
                    ?diploma rdf:type local:diploma .
                    ?diploma local:discipline ?discipline .
                    ?uri local:getVacancies ?v
                    OPTIONAL {{
                        ?discipline owl2:equivalentClass ?input .
                    }}
                    OPTIONAL {{
                        ?input owl2:equivalentClass ?discipline .
                    }}
                    FILTER ((?discipline = {disciplines} || ?input = {disciplines}) && ?v = true)
                }}
            '''
    return query

def query_personBySkill(skill):
    query = f'''
                SELECT ?uri ?name ?surname ?email
                WHERE {{
                    ?uri rdf:type foaf:Person .
                    ?uri foaf:name ?name .
                    ?uri foaf:surname ?surname .
                    ?uri local:email ?email .
                    ?uri local:skill ?skill .
                    ?uri local:getVacancies ?v
                    OPTIONAL {{
                        ?skill owl:equivalentClass ?input .
                    }}
                    OPTIONAL {{
                        ?input owl:equivalentClass ?skill .
                    }}
                    FILTER (?skill = {skill} || ?input = {skill})
                    FILTER (?v = true)
                }}
            '''
    return query

def query_personByLanguage(language):
    query = f'''
                SELECT ?uri ?name ?surname ?email
                WHERE {{
                    ?uri rdf:type foaf:Person .
                    ?uri foaf:name ?name .
                    ?uri foaf:surname ?surname .
                    ?uri local:email ?email .
                    ?uri local:language ?language .
                    ?uri local:getVacancies ?v
                    OPTIONAL {{
                        ?language owl:equivalentClass ?input .
                    }}
                    OPTIONAL {{
                        ?input owl:equivalentClass ?language .
                    }}
                    FILTER ((?input = {language} || ?language = {language}) && ?v = true)
                }}
            '''
    return query

def query_personByExperience(experience):
    query = f'''
                SELECT ?uri ?name ?surname ?email
                WHERE {{
                    ?uri rdf:type foaf:Person .
                    ?uri foaf:name ?name .
                    ?uri foaf:surname ?surname .
                    ?uri local:email ?email .
                    ?uri local:experience ?experience .
                    ?experience rdf:type local:experience .
                    ?uri local:getVacancies ?v
                    OPTIONAL {{
                        ?experience owl2:equivalentClass ?input .
                    }}
                    OPTIONAL {{
                        ?input owl2:equivalentClass ?experience .
                    }}
                    FILTER ((?input = {experience} || ?experience = {experience}) && ?v = true)
                }}
            '''
    return query

def query_getDiplomasFromPerson(personID):
    query = f'''
                SELECT ?diploma
                WHERE {{
                    ?person rdf:type foaf:Person .
                    ?person local:diploma ?diploma .
                    FILTER (?person = person:{personID})
                }}
            '''
    return query

def query_getDisciplinessFromPerson(personID):
    query = f'''
                SELECT ?discipline
                WHERE {{
                    ?person rdf:type foaf:Person .
                    ?person local:diploma ?diploma .
                    ?diploma local:discipline ?discipline .
                    FILTER (?person = person:{personID})
                }}
            '''
    return query

def query_getSkillsFromPerson(personID):
    query = f'''
                SELECT ?skill
                WHERE {{
                    ?person rdf:type foaf:Person .
                    ?person local:skill ?skill .
                    FILTER (?person = person:{personID})
                }}
            '''
    return query

def query_getLanguagesFromPerson(personID):
    query = f'''
                SELECT ?lang
                WHERE {{
                    ?person rdf:type foaf:Person .
                    ?person local:language ?lang .
                    FILTER (?person = person:{personID})
                }}
            '''
    return query

def query_getExperiencesFromPerson(personID):
    query = f'''
                SELECT ?exp
                WHERE {{
                    ?person rdf:type foaf:Person .
                    ?person local:experience ?exp .
                    FILTER (?person = person:{personID})
                }}
            '''
    return query

def query_getSkillsFromexperiencesOfPerson(personID):
    query = f'''
                SELECT ?skill
                WHERE {{
                    ?person rdf:type foaf:Person .
                    ?person local:experience ?exp .
                    ?exp local:skill ?skill .
                    FILTER (?person = person:{personID})
                }}
            '''
    return query


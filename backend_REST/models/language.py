from backend_REST.graph import LOCAL, PERSON, VACANCY, LANGUAGE

from rdflib import Literal, RDF, URIRef
from rdflib.namespace import RDF, RDFS, FOAF, XSD

from pandas import DataFrame


class Language():
    ########################################
    # USER SECTION
    ########################################
    def add_to_user(graph, user_id, language):
        user_URI = URIRef(PERSON + str(user_id))
        language_ref = URIRef(LANGUAGE + str(language))

        graph.add((user_URI, LOCAL.language, language_ref))
        graph.serialize(destination="user.ttl")

    def get_all_by_user_id(graph, user_id):
        user_URI = URIRef(PERSON + str(user_id))

        q = f'''
            SELECT ?language
            WHERE {{
                ?p rdf:type foaf:Person .
                ?p local:language ?language
            }}
        '''
        result = graph.query(q, initBindings={'p': user_URI})
        df = DataFrame(result, columns=result.vars)
        return df.to_json()

    def remove_from_user(graph, user_id, language):
        user_URI = URIRef(PERSON + str(user_id))
        language_ref = URIRef(LANGUAGE + str(language))

        graph.remove((user_URI, LOCAL.language, language_ref))
        graph.serialize(destination="user.ttl")

    ########################################
    # VACANCY SECTION
    ########################################
    def add_to_vacancy(graph, vacancy_id, language):
        vacancy_URI = URIRef(VACANCY + str(vacancy_id))
        language_ref = URIRef(LANGUAGE + str(language))

        graph.add((vacancy_URI, LOCAL.language, language_ref))
        graph.serialize(destination="user.ttl")

    def get_all_by_vacancy_id(graph, vacancy_id):
        vacancy_URI = URIRef(VACANCY + str(vacancy_id))

        q = f'''
            SELECT ?language
            WHERE {{
                ?v rdf:type loval:vacancy .
                ?v local:language ?language
            }}
        '''
        result = graph.query(q, initBindings={'v': vacancy_URI})
        df = DataFrame(result, columns=result.vars)
        return df.to_json()

    def remove_from_vacancy(graph, vacancy_id, language):
        vacancy_URI = URIRef(VACANCY + str(vacancy_id))
        language_ref = URIRef(LANGUAGE + str(language))

        graph.remove((vacancy_URI, LOCAL.language, language_ref))
        graph.serialize(destination="user.ttl")

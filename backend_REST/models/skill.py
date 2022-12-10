from pandas import DataFrame
from rdflib import Literal, RDF, URIRef
from rdflib.namespace import RDF, RDFS, FOAF, XSD

from config import GRAPH_FILE

from backend_REST.graph import WIKIDATA, LOCAL, PERSON, VACANCY

class Skill():
    ########################################
    # USER SECTION
    ########################################
    def add_to_user(graph, user_id, skill_id):
        user_URI = URIRef(PERSON + str(user_id))
        skill_URI = URIRef(WIKIDATA + str(skill_id))
    
        graph.add((user_URI, LOCAL.skill, skill_URI))
        graph.serialize(destination=GRAPH_FILE)

    def get_all_by_user_id(graph, user_id):
        user_URI = URIRef(PERSON + str(user_id))

        print(user_URI)

        q = f'''
            SELECT ?skill
            WHERE {{
                ?p rdf:type foaf:Person .
                ?p local:skill ?skill
            }}
        '''
        result = graph.query(q, initBindings={'p': user_URI})
        df = DataFrame(result, columns=result.vars)
        return df.to_json()

    def remove_from_user(graph, user_id, skill_id):
        user_URI = URIRef(PERSON + str(user_id))
        skill_URI = URIRef(WIKIDATA + str(skill_id))

        graph.remove((user_URI, LOCAL.skill, skill_URI))
        graph.serialize(destination=GRAPH_FILE)

    ########################################
    # VACANCY SECTION
    ########################################
    def add_to_vacancy(graph, vacancy_id, skill_id):
        vacancy_URI = URIRef(VACANCY + str(vacancy_id))
        skill_URI = URIRef(WIKIDATA + str(skill_id))

        graph.add((vacancy_URI, LOCAL.skill, skill_URI))
        graph.serialize(destination=GRAPH_FILE)

    def get_all_by_vacancy_id(graph, user_id):
        vacancy_URI = URIRef(VACANCY + str(user_id))

        q = f'''
            SELECT ?skill
            WHERE {{
                ?v rdf:type local:vacancy .
                ?v local:skill ?local
             }}
        '''
        result = graph.query(q, initBindings={'v': vacancy_URI})
        df = DataFrame(result, columns=result.vars)
        return df.to_json()

    def remove_from_vacancy(graph, user_id, skill_id):
        vacancy_URI = URIRef(VACANCY + str(user_id))
        skill_URI = URIRef(WIKIDATA + str(skill_id))

        graph.remove((vacancy_URI, LOCAL.skill, skill_URI))
        graph.serialize(destination=GRAPH_FILE)

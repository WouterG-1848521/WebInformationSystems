from backend_REST.graph import LOCAL, PERSON, LANGUAGE

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
        
        graph.add((user_URI, LOCAL.languages, language_ref))
        graph.serialize(destination="user.ttl")
    
    
    def get_all_by_user_id(graph, user_id):
        user_URI = URIRef(PERSON + str(user_id))
        
        q = f'''
            SELECT ?language
            WHERE {{
                ?i rdf:type local:personalInfo .
                ?i local:languages ?language
            }}
        '''
        result = graph.query(q, initBindings={'i': user_URI})
        df = DataFrame(result, columns=result.vars)
        return df.to_json()
    
    
    def remove_from_user(graph, user_id, language):
        user_URI = URIRef(PERSON + str(user_id))
        language_ref = URIRef(LANGUAGE + str(language))
                
        graph.remove((user_URI, LOCAL.languages, language_ref))
        graph.serialize(destination="user.ttl")


    ########################################
    # VACANCY SECTION
    ########################################
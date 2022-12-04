from backend_REST.graph import LOCAL, PERSON, SKILL

from rdflib import Literal, RDF, URIRef
from rdflib.namespace import RDF, RDFS, FOAF, XSD

from pandas import DataFrame

class Skill():
    ########################################
    # USER SECTION
    ########################################
    def add_to_user(graph, user_id, skill):
        user_URI = URIRef(PERSON + str(user_id))
        skill_ref = URIRef(SKILL + str(skill))
        
        graph.add((user_URI, LOCAL.skill, skill_ref))
        graph.serialize(destination="user.ttl")
    
    
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
    
    
    def remove_from_user(graph, user_id, skill):
        user_URI = URIRef(PERSON + str(user_id))
        skill_ref = URIRef(SKILL + str(skill))
        
        graph.remove((user_URI, LOCAL.skill, skill_ref))
        graph.serialize(destination="user.ttl")
    
    
    
    ########################################
    # VACANCY SECTION
    ########################################
    
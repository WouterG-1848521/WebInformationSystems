from backend_REST.graph import LOCAL

from rdflib import Literal, RDF, URIRef
from rdflib.namespace import RDF, RDFS, FOAF, XSD

from backend_REST.graph import LOCAL, PERSON

from pandas import DataFrame

class Connection():
    def add_to_user(graph, user1_id, user2_id):

        # TODO : Check if users exist

        graph.add((URIRef(PERSON + str(user1_id)), FOAF.knows, URIRef(PERSON + str(user2_id))))
        graph.serialize(destination="user.ttl")
    
    def get_all_by_user_id(graph, user_id):
        
        q = f'''
            SELECT ?p 
            WHERE {{
                person:{user_id} foaf:knows ?p .
            }}
        '''
        
        result = graph.query(q)
        df = DataFrame(result, columns=result.vars)
        print(df)
        return df.to_json()
    
    def remove_from_user():
        pass
from pandas import DataFrame
from rdflib import Literal, RDF, URIRef
from rdflib.namespace import RDF, RDFS, FOAF, XSD
from backend_REST.graph import LOCAL, PERSON

from backend_REST import db
from config import GRAPH_FILE

from backend_REST.models.database import DBConnectionRequest


class Connection():
    def send_request(from_user_id, to_user_id):
        # check if already exists
        requests = db.session.query(DBConnectionRequest).filter(DBConnectionRequest.fromUser==from_user_id, DBConnectionRequest.toUser==to_user_id).first()
        if (requests != None):
            return -1
        
        # Add to DB
        request = DBConnectionRequest()
        request.fromUser = from_user_id
        request.toUser = to_user_id
        
        db.session.add(request)
        db.session.commit()
        
        return request.id
        
    def get_by_id(request_id):
        request = DBConnectionRequest.query.get(request_id)
        
        return request
    
    def cancel_request(request_id):
        # Delete from DB
        request = DBConnectionRequest.query.get(request_id)

        if (request != None):
            db.session.delete(request)
            db.session.commit()
            
    
    def accept_request(request_id):
        Connection.cancel_request(request_id)
        
        
    def deny_request(request_id):
        Connection.cancel_request(request_id)
    
    
    def get_pending_requests_by_user(user_id):
        requests = db.session.query(DBConnectionRequest).filter(DBConnectionRequest.toUser==user_id).all()
        
        pending_requests = []
        for request in requests:
            pending_requests.append(request.id)
        return pending_requests
        
        
        
        
    def add_to_user(graph, user1_id, user2_id):

        graph.add((URIRef(PERSON + str(user1_id)), FOAF.knows, URIRef(PERSON + str(user2_id))))
        graph.serialize(destination=GRAPH_FILE)
    
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
    
    def remove_from_user(graph, user1_id, user2_id):

        user1_URI = URIRef(PERSON + str(user1_id))
        user2_URI = URIRef(PERSON + str(user2_id))
        
                
        graph.remove((user1_URI, FOAF.knows, user2_URI))
        graph.serialize(destination=GRAPH_FILE)
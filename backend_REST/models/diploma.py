from backend_REST import db
from backend_REST.graph import LOCAL, PERSON, DIPLOMA, DEGREE, PROFESSION

from rdflib import Literal, RDF, URIRef
from rdflib.namespace import RDF, RDFS, FOAF, XSD

from pandas import DataFrame

from backend_REST.models.database import DBDiploma

class Diploma():
    def add(graph, diploma_URI, degree, profession, institiution, startDate, endDate):
        degree_URI = URIRef(DEGREE + degree)
        profession_URI = URIRef(PROFESSION + profession)
        
        graph.add((diploma_URI, RDF.type, LOCAL.diploma))
        graph.add((diploma_URI, LOCAL.degree, degree_URI))
        graph.add((diploma_URI, LOCAL.profession, profession_URI))
        graph.add((diploma_URI, LOCAL.institution, Literal(institiution)))
        graph.add((diploma_URI, LOCAL.startDate, Literal(startDate, datatype=XSD.date)))
        graph.add((diploma_URI, LOCAL.endDate, Literal(endDate, datatype=XSD.date)))
              
    
    def create(graph, degree, profession, institiution, startDate, endDate):
        diploma = DBDiploma()
        db.session.add(diploma)
        db.session.commit()

        diploma_id = diploma.id
        diploma_URI = URIRef(DIPLOMA + str(diploma_id))
        
        # Add diploma
        Diploma.add(graph, diploma_URI, degree, profession, institiution, startDate, endDate)
    
        return diploma_URI
    
    
    def update(graph, diploma_id, degree, profession, institiution, startDate, endDate):
        diploma_URI = URIRef(DIPLOMA + str(diploma_id))
        
        # Remove previous diploma
        graph.remove((diploma_URI, None, None))
        
        # Add new diploma
        Diploma.add(graph, degree, profession, institiution, startDate, endDate)
        
        graph.serialize(destination="user.ttl")


    def delete(graph, diploma_id):
         # Delete from DB
        diploma = DBDiploma.query.get(diploma_id)

        if (diploma != None):
            db.session.delete(diploma)
            db.session.commit()
            
        diploma_URI = URIRef(DIPLOMA + str(diploma_id))
        
        # Delete diploma
        graph.remove((diploma_URI, None, None))

    def get_by_id(graph, diploma_id):
        diploma_URI = URIRef(DIPLOMA + str(diploma_id))
        
        q = f'''
            SELECT ?d ?degree ?profession ?institution ?startDate ?endDate
            WHERE {{
                ?d rdf:type local:diploma .
                ?d local:degree ?degree .
                ?d local:profession ?profession .
                ?d local:institution ?institution .
                ?d local:startDate ?startDate .
                ?d local:endDate ?endDate .
            }}
        '''
        
        result = graph.query(q, initBindings={'d': diploma_URI})
        df = DataFrame(result, columns=result.vars)
        return df.to_json()    
    

    ########################################
    # USER SECTION
    ########################################
    def create_for_user(graph, user_id, degree, profession, institiution, startDate, endDate):
        user_URI = URIRef(PERSON + str(user_id))
        diploma_URI = Diploma.create(graph, degree, profession, institiution, startDate, endDate)
        
        # Link diploma to user info
        graph.add((user_URI, LOCAL.diploma, diploma_URI))
        graph.serialize(destination="user.ttl")
        
        return diploma_URI
    
    
    def get_all_by_user_id(graph, user_id):
        user_URI = URIRef(PERSON + str(user_id))
        
        q = f'''
            SELECT ?d ?degree ?profession ?institution ?startDate ?endDate
            WHERE {{
                ?p rdf:type foaf:Person .
                ?p local:diploma ?d .
                ?d rdf:type local:diploma .
                ?d local:degree ?degree .
                ?d local:profession ?profession .
                ?d local:institution ?institution .
                ?d local:startDate ?startDate .
                ?d local:endDate ?endDate .
            }}
        '''
        result = graph.query(q, initBindings={'p': user_URI})
        df = DataFrame(result, columns=result.vars)
        return df.to_json()
        
        
    def delete_from_user(graph, user_id, diploma_id):
        # Delete from DB
        diploma = DBDiploma.query.get(diploma_id)

        if (diploma != None):
            db.session.delete(diploma)
            db.session.commit()
        
        user_URI = URIRef(PERSON + str(user_id))
        diploma_URI = URIRef(DIPLOMA + str(diploma_id))
        
        # Unlink diploma from user info
        graph.remove((user_URI, LOCAL.diploma, diploma_URI))
        
        Diploma.delete()
        
        graph.serialize(destination="user.ttl")
        
    ########################################
    # VACANCY SECTION
    ########################################
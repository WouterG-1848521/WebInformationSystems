from backend_REST import db
from backend_REST.graph import LOCAL, PERSON, PERSONAL_INFO, DIPLOMA, DEGREE, PROFESSION

from rdflib import Literal, RDF, URIRef, Variable
from rdflib.namespace import RDF, RDFS, FOAF, XSD

from pandas import DataFrame

def reset_DB(app):
    app.logger.info("Resetting DB...")
    
    # Drop all tables
    db.drop_all()
    
    # Create all tables
    db.create_all()
    

class DBUser(db.Model):
    """'LinkedIn' User.

    :param str email: email address of user
    :param str password: encrypted password for the user

    """
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100))
    password = db.Column(db.String(30))
    authenticated = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return '<User %r>' % self.email

    def is_active(self):
        """True, as all users are active."""
        return True

    def get_id(self):
        """Return the id to satisfy Flask-Login's requirements."""
        return self.id

    def is_authenticated(self):
        """Return True if the user is authenticated."""
        return self.authenticated

    def is_anonymous(self):
        """False, as anonymous users aren't supported."""
        return False
    
    
class User():
    def is_user_available(email):
        user = DBUser.query.filter_by(email=email).first()
        print(user)
        return user == None
    
    
    # TODO: password encryption
    def create(graph, name, surname, email, password):
        
        # Add user to DB
        user = DBUser(email=email, password=password)
        db.session.add(user)
        db.session.commit()
        
        # Get user_id
        user = DBUser.query.filter_by(email=email).first()
        user_id = user.id
        
        # Add user to Graph
        user_ref = URIRef(PERSON + str(user_id))
        user_info_ref = URIRef(PERSONAL_INFO + str(user_id))

        # User
        graph.add((user_ref, RDF.type, FOAF.Person))
        graph.add((user_ref, FOAF.name, Literal(name)))
        graph.add((user_ref, FOAF.surname, Literal(surname)))
        
        # User Info
        graph.add((user_info_ref, RDF.type, LOCAL.personalInfo))
        
        # Link user info to user
        graph.add((user_ref, LOCAL.personalInfo, user_info_ref))
        
        graph.serialize(destination="user.ttl")
        
        return user_id
        
    
    def get_all_users(graph):
        print("Getting all users...")
        q = f'''
                SELECT ?p
                WHERE {{
                    ?p rdf:type foaf:Person .
                }}
            '''
        result = graph.query(q)
        df = DataFrame(result, columns=result.vars)
        return df.to_json()
             
      
    def get_user_by_id(graph, id):
        user_URI = URIRef(PERSON + str(id))
        
        print("Searching: " + PERSON + str(id))
        q = f'''
            SELECT ?p ?name ?surname
            WHERE {{
                ?p rdf:type foaf:Person .
                ?p foaf:name ?name .
                ?p foaf:surname ?surname .
            }}
        '''
        
        result = graph.query(q, initBindings={'p': user_URI})
        df = DataFrame(result, columns=result.vars)
        return df.to_json()
        
   
    def get_user_profile_by_id(graph, id):
        user_URI = URIRef(PERSON + str(id))
        user_info_URI = URIRef(PERSONAL_INFO + str(id))
        
        q = f"""
                SELECT ?p ?i ?surName ?email
                WHERE {{
                    ?p rdf:type foaf:Person .
                    ?i rdf:type local:personalInfo .
                    OPTIONAL {{ ?p foaf:surname ?surName . }}
                    OPTIONAL {{ ?i local:email ?email . }}    
                }}
            """
        
        result = graph.query(q, initBindings={'p': user_URI, 'i': user_info_URI})
        df = DataFrame(result, columns=result.vars)
        return df.to_json(orient="records")
   
        
    def delete_user_by_id(graph, id):
        # Delete user from DB
        user = DBUser.query.get(id)
        
        # If user still in DB
        if (user != None):
            db.session.delete(user)
            db.session.commit()
        
        user_URI = URIRef(PERSON + str(id))
        userInfo_URI = URIRef(PERSONAL_INFO + str(id))
        
        # TODO: Delete all diploma's
        User.delete_diploma(graph, id, 0)
        
        # Delete user info
        print("Deleting: " + userInfo_URI)
        graph.remove((userInfo_URI, None, None))
        
        # Delete user
        print("Deleting: " + user_URI)
        graph.remove((user_URI, None, None))
        
        graph.serialize(destination="user.ttl")


    def update_email(graph, id, email):
        user_info_ref = URIRef(PERSONAL_INFO + str(id))

        # Delete previous email
        graph.remove((user_info_ref, LOCAL.email, None))
        
        # Add new email
        graph.add((user_info_ref, LOCAL.email, Literal(email)))
        
        graph.serialize(destination="user.ttl")
        
        
    def update_phone(graph, id, phone):
        user_info_ref = URIRef(PERSONAL_INFO + str(id))
    
        # Delete previous phone
        graph.remove((user_info_ref, LOCAL.phone, None))
            
        # Add new phone
        graph.add((user_info_ref, LOCAL.phone, Literal(phone)))
        
        graph.serialize(destination="user.ttl")
        
        
    def create_diploma(graph, user_id, degree, profession, institiution, startDate, endDate):
        user_info_ref = URIRef(PERSONAL_INFO + str(user_id))
        
        # TODO: get new diploma id
        diploma_id = 1
        diploma_URI = URIRef(DIPLOMA + str(diploma_id))
        
        degree_URI = URIRef(DEGREE + degree);
        profession_URI = URIRef(PROFESSION + profession);
        
        # Create diploma
        graph.add((diploma_URI, RDF.type, LOCAL.diploma))
        graph.add((diploma_URI, LOCAL.degree, degree_URI))
        graph.add((diploma_URI, LOCAL.profession, profession_URI))
        graph.add((diploma_URI, LOCAL.institution, Literal(institiution)))
        graph.add((diploma_URI, LOCAL.startDate, Literal(startDate, datatype=XSD.date)))
        graph.add((diploma_URI, LOCAL.endDate, Literal(endDate, datatype=XSD.date)))
        
        # Link diploma to user info
        graph.add((user_info_ref, LOCAL.diploma, diploma_URI))
        
        graph.serialize(destination="user.ttl")
        
        return diploma_id
    
    
    def get_all_diplomas_by_user(graph, user_id):
        userInfo_URI = URIRef(PERSONAL_INFO + str(user_id))
        
        q = f'''
            SELECT ?d ?degree ?profession ?institution ?startDate ?endDate
            WHERE {{
                ?i rdf:type local:personalInfo .
                ?i local:diploma ?d .
                ?d rdf:type local:diploma .
                ?d local:degree ?degree .
                ?d local:profession ?profession .
                ?d local:institution ?institution .
                ?d local:startDate ?startDate .
                ?d local:endDate ?endDate .
            }}
        '''
        result = graph.query(q, initBindings={'i': userInfo_URI})
        df = DataFrame(result, columns=result.vars)
        return df.to_json()
        

    def get_diploma_by_id(graph, diploma_id):
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
    
    
    def update_diploma(graph, user_id, diploma_id, degree, profession, institiution, startDate, endDate):
        diploma_URI = URIRef(DIPLOMA + str(diploma_id))
        
        degree_URI = URIRef(DEGREE + degree);
        profession_URI = URIRef(PROFESSION + profession);
        
        # Remove previous diploma
        graph.remove((diploma_URI, None, None))
        
        # Add new diploma
        graph.add((diploma_URI, RDF.type, LOCAL.diploma))
        graph.add((diploma_URI, LOCAL.degree, degree_URI))
        graph.add((diploma_URI, LOCAL.profession, profession_URI))
        graph.add((diploma_URI, LOCAL.institution, Literal(institiution)))
        graph.add((diploma_URI, LOCAL.startDate, Literal(startDate, datatype=XSD.date)))
        graph.add((diploma_URI, LOCAL.endDate, Literal(endDate, datatype=XSD.date)))
        
        graph.serialize(destination="user.ttl")
    
    
    def delete_diploma(graph, user_id, diploma_id):
        user_info_ref = URIRef(PERSONAL_INFO + str(user_id))
        diploma_URI = URIRef(DIPLOMA + str(diploma_id))
        
        # Unlink diploma to user info
        graph.remove((user_info_ref, LOCAL.diploma, diploma_URI))
        
        # Delete diploma
        graph.remove((diploma_URI, None, None))
        
        graph.serialize(destination="user.ttl")
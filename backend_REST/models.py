from backend_REST import db
from backend_REST.graph import LOCAL, PERSON, PERSONAL_INFO

from rdflib import Graph, Literal, RDF, URIRef, Namespace
from rdflib.namespace import RDF, RDFS, FOAF

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
        
        
    def getUserById(graph, id):
        print("Searching: " + PERSON + str(id))
        q = f'''
            PREFIX foaf: <http://xmlns.com/foaf/0.1/>
            SELECT ?p ?name ?surname
            WHERE {{
                ?p rdf:type foaf:Person .
                ?p foaf:name ?name .
                ?p foaf:surname ?surname .
            }}
        '''
        
        result = graph.query(q, initBindings={'p': URIRef(PERSON + str(id))})
        df = DataFrame(result, columns=result.vars)
        return df.to_json()
        
        
    def deleteUserById(graph, id):
        # Delete user from DB
        user = DBUser.query.get(id)
        
        # If user still in DB
        if (user != None):
            db.session.delete(user)
            db.session.commit()
        
        print("Deleting: " + PERSON + str(id))
        
        # Delete user from graph
        q = f'''
            PREFIX foaf: <http://xmlns.com/foaf/0.1/>
            PREFIX local: <http://localhost/> 
            
            DELETE {{
                ?p rdf:type foaf:Person .
                ?p foaf:name ?name .
                ?p foaf:surname ?surname .
                ?p local:personalInfo ?i .
            }}
            WHERE {{
                ?p rdf:type foaf:Person .
                ?p foaf:name ?name .
                ?p foaf:surname ?surname .
                ?p local:personalInfo ?i .
            }}
        '''
        graph.update(q, initBindings={'p': URIRef(PERSON + str(id))})
        
        print("Deleting: " + PERSONAL_INFO + str(id))
        
        # Delete userInfo from graph
        q = f'''
            PREFIX foaf: <http://xmlns.com/foaf/0.1/>
            PREFIX local: <http://localhost/> 
            
            DELETE {{
                ?i rdf:type local:personalInfo .
            }}
            WHERE {{
                ?i rdf:type local:personalInfo .
            }}
        '''
        graph.update(q, initBindings={'i': URIRef(PERSONAL_INFO + str(id))})
        
        graph.serialize(destination="user.ttl")
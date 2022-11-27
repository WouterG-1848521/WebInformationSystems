from backend_REST import db
from backend_REST.graph import LOCAL, PERSON, PERSONAL_INFO

from rdflib import Graph, Literal, RDF, URIRef, Namespace
from rdflib.namespace import RDF, RDFS, FOAF

def reset_DB(app):
    app.logger.info("Resetting DB...")
    
    # Drop all tables
    db.drop_all()
    
    # Create all tables
    db.create_all()

def setup_DB_DEBUG(app):
    app.logger.info("Setting up DB debug...")
    user = DBUser(email="email", password="password")
    app.logger.info("User id: " + str(user.id))
    db.session.add(user)
    db.session.commit()


def test_DB_DEBUG(app):
    app.logger.info("Testing DB...")
    user = DBUser.query.filter_by(email='email').first()
    app.logger.info("User id: " +  str(user.id))
    
def remove_DB_DEBUG(app):
    app.logger.info("Removing DB debug...")
    user = DBUser.query.filter_by(email='email').first()
    db.session.delete(user)
    db.session.commit()
    
    # To delete all: 
    DBUser.query.delete()
    


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

    def is_user_available(email):
        user = DBUser.query.filter_by(email=email).first()
        print(user)
        return user == None
        
        
        

from flask import jsonify, request
from flask_login import login_user, logout_user, login_required
from rdflib import Literal, RDF, URIRef

from backend_REST import db
from backend_REST.models import User

from backend_REST.graph import LOCAL, LANGUAGE

def create_test_routes(app, g):
    
    @app.route("/db/add", methods=['GET'], endpoint='func1')
    def add_user():
        app.logger.info("Add user to DB...")
        user = User(email="email", password="password")
        db.session.add(user)
        db.session.commit()
        
        return "Added user."
    
    
    @app.route("/db/login", methods=['GET'], endpoint='func2')
    def login():
        app.logger.info("Logging in...")
        user = User.query.filter_by(email='email').first()        
        login_user(user)
        
        return "Logged in."
    
    
    @app.route("/db/logout", methods=['GET'], endpoint='func3')
    def logout():
        app.logger.info("Logging out...")
        logout_user()
        
        return "Logged out."

    
    @app.route("/db/get", methods=['GET'], endpoint='func4')
    @login_required
    def get_user():
        app.logger.info("Testing login required...")
        user = User.query.filter_by(email='email').first()
        app.logger.info(user.id)
        
        return str(user.id);
        
    
    @app.route("/db/remove", methods=['GET'], endpoint='func5')
    def remove_user(): 
        app.logger.info("Removing user from DB...")
        user = User.query.filter_by(email='email').first()
        db.session.delete(user)
        db.session.commit()
        
        # To delete all: 
        User.query.delete()
        
        return "Removed user."
    
    
    @app.route("/fill/languages", methods=['GET'])
    def fill_languages():
        # Add Nederlands
        g.add((URIRef(LANGUAGE + str(1)), RDF.type, LOCAL.language))
        g.add((URIRef(LANGUAGE + str(1)), LOCAL.name, Literal("Nederlands", lang="nl")))
        
        # Add English
        g.add((URIRef(LANGUAGE + str(2)), RDF.type, LOCAL.language))
        g.add((URIRef(LANGUAGE + str(2)), LOCAL.name, Literal("English", lang="en")))
        
        # Add Francais
        g.add((URIRef(LANGUAGE + str(3)), RDF.type, LOCAL.language))
        g.add((URIRef(LANGUAGE + str(3)), LOCAL.name, Literal("Francais", lang="fr")))
        
        g.serialize(destination="user.ttl")
        
        return "Filled graph with the following languages: Nederlands, English and Francais."
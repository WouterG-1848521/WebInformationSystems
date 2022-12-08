from backend_REST import db
from backend_REST.graph import LOCAL, PERSON

from rdflib import Literal, RDF, URIRef
from rdflib.namespace import RDF, RDFS, FOAF, XSD

from pandas import DataFrame

from backend_REST.models.database import DBUser


class User():
    def is_available(email):
        user = DBUser.query.filter_by(email=email).first()
        return user == None

    ########################################
    # CREATE
    ########################################
    # TODO: password encryption
    def create(graph, name, surname, email, password, is_admin=False):

        # Add user to DB
        user = DBUser(email=email, password=password, isAdmin=is_admin)
        db.session.add(user)
        db.session.commit()

        # Get user_id
        user_id = user.id

        # Add user to Graph
        user_ref = URIRef(PERSON + str(user_id))

        # User
        graph.add((user_ref, RDF.type, FOAF.Person))
        graph.add((user_ref, FOAF.name, Literal(name)))
        graph.add((user_ref, FOAF.surname, Literal(surname)))

        graph.serialize(destination="user.ttl")

        return user_id

    ########################################
    # GETTERS
    ########################################

    def get_all(graph):
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

    def get_by_id(graph, user_id):
        user_URI = URIRef(PERSON + str(user_id))

        print("Searching: " + PERSON + str(user_id))
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

    def get_profile_by_id(graph, user_id):
        user_URI = URIRef(PERSON + str(user_id))

        q = f"""
                SELECT ?p ?i ?surName ?email
                WHERE {{
                    ?p rdf:type foaf:Person .
                    OPTIONAL {{ ?p foaf:surname ?surName . }}
                    OPTIONAL {{ ?p local:email ?email . }}    
                }}
            """

        result = graph.query(q, initBindings={'p': user_URI})
        df = DataFrame(result, columns=result.vars)
        return df.to_json(orient="records")

    ########################################
    # UPDATE
    ########################################

    # def update_main_data(graph, user_id, name, surname, email, password):

    # Main update function (called by all others)

    def update(graph, user_id, term, literal, literal_type=None):
        user_URI = URIRef(PERSON + str(user_id))

        # Remove old, add new
        graph.remove((user_URI, term, None))
        graph.add((user_URI, term, Literal(literal, datatype=literal_type)))

        graph.serialize(destination="user.ttl")

    # ----- BASIC UPDATES -----#
    def update_name(graph, user_id, name):
        User.update(graph, user_id, FOAF.name, name)

    def update_surname(graph, user_id, surname):
        User.update(graph, user_id, FOAF.surname, surname)

    def update_email(graph, user_id, email):
        User.update(graph, user_id, LOCAL.email, email)

    def update_phone(graph, user_id, phone):
        User.update(graph, user_id, LOCAL.phone, phone)

    def update_graduation_date(graph, user_id, date):
        User.update(graph, user_id, LOCAL.date, date, XSD.date)

    ########################################
    # DELETE
    ########################################

    def delete(graph, user_id):
        # Delete user from DB
        user = DBUser.query.get(user_id)

        # If user still in DB
        if (user != None):
            db.session.delete(user)
            db.session.commit()

        user_URI = URIRef(PERSON + str(user_id))

        # TODO: Delete all diplomas
        # TODO: Delete all work experiences

        # Delete user
        print("Deleting: " + user_URI)
        graph.remove((user_URI, None, None))

        graph.serialize(destination="user.ttl")

    def is_admin(user_id):
        user = DBUser.query.get(user_id)

        return user.isAdmin

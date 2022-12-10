from pandas import DataFrame
from rdflib import Literal, RDF, URIRef, Variable
from rdflib.namespace import RDF, RDFS, FOAF, XSD
from backend_REST.graph import LOCAL, PERSON, GEONAMES

from backend_REST import db
from config import GRAPH_FILE

from backend_REST.models.database import DBUser


class User():
    def exists(user_id):
        user = DBUser.query.get(user_id)
        return user != None

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
        user_URI = URIRef(PERSON + str(user_id))

        # User
        graph.add((user_URI, RDF.type, FOAF.Person))
        graph.add((user_URI, FOAF.name, Literal(name)))
        graph.add((user_URI, FOAF.surname, Literal(surname)))
        graph.add((user_URI, LOCAL.getVacancies, Literal(
            user.getVacancies, datatype=XSD.boolean)))

        graph.serialize(destination=GRAPH_FILE)

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

    def update(graph, user_id, name, surname, email):
        user_URI = URIRef(PERSON + str(user_id))

        # Remove old, add new
        graph.remove((user_URI, FOAF.name, None))
        graph.add((user_URI, FOAF.name, Literal(name)))

        graph.remove((user_URI, FOAF.surname, None))
        graph.add((user_URI, FOAF.surname, Literal(surname)))

        graph.remove((user_URI, LOCAL.email, None))
        graph.add((user_URI, LOCAL.email, Literal(email)))

        graph.serialize(destination=GRAPH_FILE)


    def update_literal(graph, user_id, term, literal, literal_type=None):
        user_URI = URIRef(PERSON + str(user_id))

        # Remove old, add new
        graph.remove((user_URI, term, None))
        graph.add((user_URI, term, Literal(literal, datatype=literal_type)))

        graph.serialize(destination=GRAPH_FILE)

    def update_URI(graph, user_id, term, URI):
        user_URI = URIRef(PERSON + str(user_id))

        # Remove old, add new
        graph.remove((user_URI, term, None))
        graph.add((user_URI, term, URI))

        graph.serialize(destination=GRAPH_FILE)

    # ----- BASIC UPDATES -----#
    def update_name(graph, user_id, name):
        User.update_literal(graph, user_id, FOAF.name, name)

    def update_surname(graph, user_id, surname):
        User.update_literal(graph, user_id, FOAF.surname, surname)

    def update_email(graph, user_id, email):
        User.update_literal(graph, user_id, LOCAL.email, email)

    def update_phone(graph, user_id, phone):
        User.update_literal(graph, user_id, LOCAL.phone, phone)

    def update_graduation_date(graph, user_id, date):
        User.update_literal(
            graph, user_id, LOCAL.graduationDate, date, XSD.date)

    def update_location(graph, user_id, location_id):
        location_URI = URIRef(GEONAMES + location_id)
        User.update_URI(graph, user_id, LOCAL.location, location_URI)

    def get_all_diploma_URIs(graph, user_id):
        user_URI = URIRef(PERSON + str(user_id))
        q = f'''
            SELECT ?diploma
            WHERE {{
                ?p rdf:type foaf:Person .
                ?p local:diploma ?diploma .
            }}
        '''

        result = graph.query(q, initBindings={'p': user_URI})
        df = DataFrame(result, columns=result.vars)
        return df[Variable('diploma')].values.tolist()

    def get_all_work_experience_URIs(graph, user_id):
        user_URI = URIRef(PERSON + str(user_id))
        q = f'''
            SELECT ?experience
            WHERE {{
                ?p rdf:type foaf:Person .
                ?p local:experience ?experience .
            }}
        '''

        result = graph.query(q, initBindings={'p': user_URI})
        df = DataFrame(result, columns=result.vars)
        return df[Variable('experience')].values.tolist()

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

        diploma_URIs = User.get_all_diploma_URIs(graph, user_id)
        experience_URIs = User.get_all_work_experience_URIs(graph, user_id)

        # Delete all diplomas of user
        for diploma_URI in diploma_URIs:
            graph.remove((diploma_URI, None, None))

        # Delete all experiences of user
        for experience_URI in experience_URIs:
            graph.remove((experience_URI, None, None))

        # Delete user
        print("Deleting: " + user_URI)
        graph.remove((user_URI, None, None))

        graph.serialize(destination=GRAPH_FILE)

    def is_admin(user_id):
        user = DBUser.query.get(user_id)

        return user.isAdmin

    def toggle_get_vacancies(graph, user_id):
        # Update DB
        user = DBUser.query.get(user_id)
        user.getVacancies = not user.getVacancies
        db.session.commit()

        # Update RDF
        User.update_literal(graph, user_id, LOCAL.getVacancies,
                            user.getVacancies, XSD.boolean)

        return user.getVacancies

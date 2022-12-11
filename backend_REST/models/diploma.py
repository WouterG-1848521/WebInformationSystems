import pandas as pd
from pandas import DataFrame
from rdflib import Literal, RDF, URIRef
from rdflib.namespace import RDF, RDFS, FOAF, XSD
from backend_REST.graph import WIKIDATA, LOCAL, PERSON, VACANCY, DIPLOMA, DEGREE

from backend_REST import db
from config import GRAPH_FILE

from backend_REST.models.database import DBDiploma


class Diploma():
    def add(graph, diploma_URI, degree, discipline_id, institiution, startDate, endDate):
        degree_URI = URIRef(DEGREE + degree)
        discipline_URI = URIRef(WIKIDATA + discipline_id)

        graph.add((diploma_URI, RDF.type, LOCAL.diploma))
        graph.add((diploma_URI, LOCAL.degree, degree_URI))
        graph.add((diploma_URI, LOCAL.discipline, discipline_URI))
        graph.add((diploma_URI, LOCAL.institution, Literal(institiution)))
        graph.add((diploma_URI, LOCAL.startDate,
                  Literal(startDate, datatype=XSD.date)))
        graph.add((diploma_URI, LOCAL.endDate,
                  Literal(endDate, datatype=XSD.date)))

    def create(graph, degree, discipline_id, institiution, startDate, endDate):
        diploma = DBDiploma()
        db.session.add(diploma)
        db.session.commit()

        diploma_id = diploma.id
        diploma_URI = URIRef(DIPLOMA + str(diploma_id))

        # Add diploma
        Diploma.add(graph, diploma_URI, degree, discipline_id,
                    institiution, startDate, endDate)

        return diploma_URI

    def update(graph, diploma_id, degree, discipline_id, institiution, startDate, endDate):
        diploma_URI = URIRef(DIPLOMA + str(diploma_id))

        # Remove previous diploma
        graph.remove((diploma_URI, None, None))

        # Add new diploma
        Diploma.add(graph, diploma_URI, degree, discipline_id,
                    institiution, startDate, endDate)

        graph.serialize(destination=GRAPH_FILE)

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
            SELECT ?d ?degree ?discipline ?institution ?startDate ?endDate
            WHERE {{
                ?d rdf:type local:diploma .
                ?d local:degree ?degree .
                ?d local:discipline ?discipline .
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

    def create_for_user(graph, user_id, degree, discipline_id, institiution, startDate, endDate):
        user_URI = URIRef(PERSON + str(user_id))
        diploma_URI = Diploma.create(
            graph, degree, discipline_id, institiution, startDate, endDate)

        # Link diploma to user
        graph.add((user_URI, LOCAL.diploma, diploma_URI))
        graph.serialize(destination=GRAPH_FILE)

        return diploma_URI

    def get_all_by_user_id(graph, user_id):
        user_URI = URIRef(PERSON + str(user_id))

        q = f'''
            SELECT ?d ?degree ?discipline ?institution ?startDate ?endDate
            WHERE {{
                ?p rdf:type foaf:Person .
                ?p local:diploma ?d .
                ?d rdf:type local:diploma .
                ?d local:degree ?degree .
                ?d local:discipline ?discipline .
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

        # Unlink diploma from user
        graph.remove((user_URI, LOCAL.diploma, diploma_URI))

        Diploma.delete(graph, diploma_id)

        graph.serialize(destination=GRAPH_FILE)

    ########################################
    # VACANCY SECTION
    ########################################
    def create_for_vacancy(graph, vacancy_id, degree, discipline_id, institiution, startDate, endDate):
        vacancy_URI = URIRef(VACANCY + str(vacancy_id))
        diploma_URI = Diploma.create(
            graph, degree, discipline_id, institiution, startDate, endDate)

        # Link diploma to vacancy
        graph.add((vacancy_URI, LOCAL.diploma, diploma_URI))
        graph.serialize(destination=GRAPH_FILE)

        return diploma_URI

    def get_all_by_vacancy_id(graph, vacancy_id):
        vacancy_URI = URIRef(VACANCY + str(vacancy_id))

        q = f'''
            SELECT ?d ?degree ?discipline ?institution ?startDate ?endDate
            WHERE {{
                ?v rdf:type local:vacancy .
                ?v local:diploma ?d .
                ?d rdf:type local:diploma .
                ?d local:degree ?degree .
                ?d local:discipline ?discipline .
                ?d local:institution ?institution .
                ?d local:startDate ?startDate .
                ?d local:endDate ?endDate .
            }}
        '''
        result = graph.query(q, initBindings={'v': vacancy_URI})
        df = DataFrame(result, columns=result.vars)
        return df.to_json()

    def delete_from_vacany(graph, vacancy_id, diploma_id):
        # Delete from DB
        diploma = DBDiploma.query.get(diploma_id)

        if (diploma != None):
            db.session.delete(diploma)
            db.session.commit()

        vacancy_URI = URIRef(VACANCY + str(vacancy_id))
        diploma_URI = URIRef(DIPLOMA + str(diploma_id))

        # Unlink diploma from vacancy
        graph.remove((vacancy_URI, LOCAL.diploma, diploma_URI))

        Diploma.delete(graph, diploma_id)

        graph.serialize(destination=GRAPH_FILE)

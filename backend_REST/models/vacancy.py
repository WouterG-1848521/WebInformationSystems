from pandas import DataFrame
from rdflib import Literal, RDF, URIRef
from rdflib.namespace import RDF, RDFS, FOAF, XSD
from backend_REST.graph import LOCAL, VACANCY, ENTERPRISE, PERSON, GEONAMES

from backend_REST import db
from config import GRAPH_FILE

from backend_REST.models.database import DBVacancy


# Vacancy (id) :
#     id has a jobTitle
#     id has a startDate
#     id has a endDate
#     id has a availability
#     id has a owner (enterprise)

#     id has a Diploma
#     id has Skills[]
#     id has Languages[]
#     id has a jobDescription
#     id has a jobResponsibilities
#     id has a jobSalary
#     id has a jobLocation


class Vacancy():

    def create(graph, enterprise_id, maintainer_id, job_title, start_date, end_date, location_id):
        # Add vacancy to DB
        vacancy = DBVacancy()
        db.session.add(vacancy)
        db.session.commit()

        vacancy_id = vacancy.id

        vacancy_URI = URIRef(VACANCY + str(vacancy_id))
        enterprise_URI = URIRef(ENTERPRISE + str(enterprise_id))
        maintainer_URI = URIRef(PERSON + str(maintainer_id))
        location_URI = URIRef(GEONAMES + str(location_id))

        graph.add((vacancy_URI, RDF.type, LOCAL.vacancy))
        graph.add((vacancy_URI, LOCAL.enterprise, enterprise_URI))
        graph.add((vacancy_URI, LOCAL.postedBy, maintainer_URI))
        graph.add((vacancy_URI, LOCAL.jobTitle, Literal(job_title)))
        graph.add((vacancy_URI, LOCAL.startDate,
                  Literal(start_date, datatype=XSD.date)))
        graph.add((vacancy_URI, LOCAL.endDate,
                  Literal(end_date,  datatype=XSD.date)))
        graph.add((vacancy_URI, LOCAL.location, location_URI))

        graph.serialize(destination=GRAPH_FILE)

        return vacancy_id

    def update_literal(graph, vacancy_id, term, literal, literal_type=None):
        vacancy_URI = URIRef(VACANCY + str(vacancy_id))

        # Remove old, add new
        graph.remove((vacancy_URI, term, None))
        graph.add((vacancy_URI, term, Literal(literal, datatype=literal_type)))

        graph.serialize(destination=GRAPH_FILE)

    def update_URI(graph, vacancy_id, term, URI):
        vacancy_URI = URIRef(VACANCY + str(vacancy_id))

        # Remove old, add new
        graph.remove((vacancy_URI, term, None))
        graph.add((vacancy_URI, term, URI))

        graph.serialize(destination=GRAPH_FILE)

    def update_posted_by(graph, vacancy_id, maintainer_id):
        maintainer_URI = URIRef(PERSON + str(maintainer_id))
        Vacancy.update_URI(graph, vacancy_id, LOCAL.postedBy, maintainer_URI)

    def update_job_title(graph, vacancy_id, job_title):
        Vacancy.update_literal(graph, vacancy_id, LOCAL.jobTitle, job_title)

    def update_start_date(graph, vacancy_id, start_date):
        Vacancy.update_literal(graph, vacancy_id, LOCAL.startDate,
                               start_date, XSD.date)

    def update_end_date(graph, vacancy_id, end_date):
        Vacancy.update_literal(graph, vacancy_id, LOCAL.endDate,
                               end_date, XSD.date)

    def update_location(graph, vacancy_id, location_id):
        location_URI = URIRef(GEONAMES + str(location_id))
        Vacancy.update_URI(graph, vacancy_id, LOCAL.location, location_URI)

    def delete(graph, vacancy_id):
        # Delete from DB
        vacancy = DBVacancy.query.get(vacancy_id)

        if (vacancy != None):
            db.session.delete(vacancy)
            db.session.commit()

        vacancy_URI = URIRef(VACANCY + str(vacancy_id))
        graph.remove((vacancy_URI, None, None))
        graph.serialize(destination=GRAPH_FILE)

    def get_by_enterprise_id(graph, enterprise_id):
        enterprise_URI = URIRef(ENTERPRISE + str(enterprise_id))

        print("Searching: " + ENTERPRISE + str(enterprise_id))
        q = f'''
            SELECT ?v ?maintainerId ?jobTitle ?startDate ?endDate ?location
            WHERE {{
                ?v  rdf:type local:vacancy .
                ?v local:enterprise ?e .
                ?v local:postedBy ?maintainerId .
                ?v local:jobTitle ?jobTitle .
                ?v local:startDate ?startDate .
                ?v local:endDate ?endDate .
                ?v local:location ?location .
            }}
        '''

        result = graph.query(q, initBindings={'e': enterprise_URI})
        df = DataFrame(result, columns=result.vars)
        return df.to_json()

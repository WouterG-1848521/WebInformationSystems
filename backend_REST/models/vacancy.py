from backend_REST import db
from backend_REST.graph import LOCAL, VACANCY, ENTERPRISE, PERSON

from rdflib import Literal, RDF, URIRef
from rdflib.namespace import RDF, RDFS, FOAF, XSD

from backend_REST.models.database import DBVacancy

from pandas import DataFrame

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

    def create(graph, enterprise_id, maintainer_id, job_title, start_date, end_date):
        # Add vacancy to DB
        vacancy = DBVacancy()
        db.session.add(vacancy)
        db.session.commit()

        vacancy_id = vacancy.id

        vacancy_URI = URIRef(VACANCY + str(vacancy_id))
        enterprise_URI = URIRef(ENTERPRISE + str(enterprise_id))
        maintainer_URI = URIRef(PERSON + str(maintainer_id))

        graph.add((vacancy_URI, RDF.type, LOCAL.vacancy))
        graph.add((vacancy_URI, LOCAL.enterprise, enterprise_URI))
        graph.add((vacancy_URI, LOCAL.postedBy, maintainer_URI))
        graph.add((vacancy_URI, LOCAL.jobTitle, Literal(job_title)))
        graph.add((vacancy_URI, LOCAL.startDate,
                  Literal(start_date, datatype=XSD.date)))
        graph.add((vacancy_URI, LOCAL.endDate,
                  Literal(end_date,  datatype=XSD.date)))

        graph.serialize(destination="user.ttl")

        return vacancy_id

    # Main update function (called by others)
    def update(graph, vacancy_id, term, literal, literal_type=None):
        vacancy_URI = URIRef(VACANCY + str(vacancy_id))

        # Remove old, add new
        graph.remove((vacancy_URI, term, None))
        graph.add((vacancy_URI, term, Literal(literal, datatype=literal_type)))

        graph.serialize(destination="user.ttl")

    def update_posted_by(graph, vacancy_id, maintainer_id):
        Vacancy.update(graph, vacancy_id, LOCAL.postedBy, maintainer_id)

    def update_job_title(graph, vacancy_id, job_title):
        Vacancy.update(graph, vacancy_id, LOCAL.jobTitle, job_title)

    def update_start_date(graph, vacancy_id, start_date):
        Vacancy.update(graph, vacancy_id, LOCAL.startDate, start_date)

    def update_end_date(graph, vacancy_id, end_date):
        Vacancy.update(graph, vacancy_id, LOCAL.endDate, end_date)

    def delete(graph, vacancy_id):
        # Delete from DB
        vacancy = DBVacancy.query.get(vacancy_id)

        if (vacancy != None):
            db.session.delete(vacancy)
            db.session.commit()

        vacancy_URI = URIRef(VACANCY + str(vacancy_id))
        graph.remove((vacancy_URI, None, None))
        graph.serialize(destination="user.ttl")

    def get_by_enterprise_id(graph, enterprise_id):
        enterprise_URI = URIRef(ENTERPRISE + str(enterprise_id))

        print("Searching: " + ENTERPRISE + str(enterprise_id))
        q = f'''
            SELECT ?v ?maintainerId ?jobTitle ?startDate ?endDate
            WHERE {{
                ?v  rdf:type local:vacancy .
                ?v local:enterprise ?e .
                ?v local:postedBy ?maintainerId .
                ?v local:jobTitle ?jobTitle .
                ?v local:startDate ?startDate .
                ?v local:endDate ?endDate .
            }}
        '''

        result = graph.query(q, initBindings={'e': enterprise_URI})
        df = DataFrame(result, columns=result.vars)
        return df.to_json()

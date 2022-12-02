from backend_REST import db
from backend_REST.graph import LOCAL, VACANCY

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

    # TODO : Add other parameters required according to schema
    def create(graph):
        # Add vacancy to DB
        vacancy = DBVacancy()
        db.session.add(vacancy)
        db.session.commit()

        vacancy_id = vacancy.id

        vacancy_ref = URIRef(VACANCY + str(vacancy_id))
        

        graph.add((vacancy_ref, RDF.type, LOCAL.vacancy))

        graph.serialize(destination="user.ttl")

        return vacancy_id


    def delete(graph, vacancy_id):
        # Delete from DB
        vacancy = DBVacancy.query.get(vacancy_id)

        if (vacancy != None):
            db.session.delete(vacancy)
            db.session.commit()

        vacancy_URI = URIRef(VACANCY + str(vacancy_id))
        graph.remove((vacancy_URI, None, None))
        graph.serialize(destination="user.ttl")




    def get_by_enterprise_id():
        pass
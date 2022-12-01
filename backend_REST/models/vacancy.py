from backend_REST.graph import LOCAL

from rdflib import Literal, RDF, URIRef
from rdflib.namespace import RDF, RDFS, FOAF, XSD

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
    def add():
        pass

    def delete():
        pass

    def get_by_enterprise_id():
        pass
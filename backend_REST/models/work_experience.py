from backend_REST.graph import LOCAL

from rdflib import Literal, RDF, URIRef, Variable
from rdflib.namespace import RDF, RDFS, FOAF, XSD

from pandas import DataFrame

class WorkExperience():
    def create(graph):
        pass
        
    def update(graph):
        pass
    
    def delete(graph):
        pass
    
    ########################################
    # USER SECTION
    ########################################
    def create_for_user(graph, user_id):
        WorkExperience.create(graph)
        # TODO: link to user
        pass
    
    def get_all_by_user_id():
        pass
    
    def delete_from_user(graph, user_id):
        # TODO: unlink from user
        WorkExperience.delete(graph)
        pass

    ########################################
    # VACANCY SECTION
    ########################################
from rdflib import Literal, RDF, URIRef, Variable
from rdflib.namespace import RDF, RDFS, FOAF, XSD
from pandas import DataFrame
from backend_REST.graph import WIKIDATA, LOCAL, EXPERIENCE, PERSON

from backend_REST import db
from config import GRAPH_FILE

from backend_REST.models.database import DBWorkExperience

class WorkExperience():
    def add(graph, experience_URI, job_title, profession_URI, skills, start_date, end_date):
        graph.add((experience_URI, RDF.type, LOCAL.experience))
        graph.add((experience_URI, LOCAL.jobTitle, Literal(job_title)))
        graph.add((experience_URI, LOCAL.profession, profession_URI))
        
        for skill_id in skills:
            skill_URI = URIRef(WIKIDATA + str(skill_id))
            graph.add((experience_URI, LOCAL.skill, skill_URI))
        
        graph.add((experience_URI, LOCAL.startDate, Literal(start_date, datatype=XSD.date)))
        graph.add((experience_URI, LOCAL.endDate, Literal(end_date, datatype=XSD.date)))
    
    
    def create(graph, job_title, profession_id, skills, start_date, end_date):
        # Add vacancy to DB
        experience = DBWorkExperience()
        db.session.add(experience)
        db.session.commit()

        experience_id = experience.id
        experience_URI = URIRef(EXPERIENCE + str(experience_id))
        profession_URI = URIRef(WIKIDATA + str(profession_id))
        
        # Add work experience
        WorkExperience.add(graph, experience_URI, job_title, profession_URI, skills, start_date, end_date)
        
        return experience_URI
        
        
    def update(graph, experience_id, job_title, profession_id, skills, start_date, end_date):
        experience_URI = URIRef(EXPERIENCE + str(experience_id))
        profession_URI = URIRef(WIKIDATA + str(profession_id))
        
        # Remove previous work experience
        graph.remove((experience_URI, None, None))
    
        # Add new work experience
        WorkExperience.add(graph, experience_URI, job_title, profession_URI, skills, start_date, end_date)
        
        graph.serialize(destination=GRAPH_FILE)
    
    
    def delete(graph, experience_id):
        # TODO: delete from db
        experience_URI = URIRef(EXPERIENCE + str(experience_id))
        
        # Remove work experience
        graph.remove((experience_URI, None, None))
        
    def get_by_id(graph, experience_id):
        experience_URI = URIRef(EXPERIENCE + str(experience_id))
        
        q = f'''
            SELECT ?e ?jobTitle ?profession ?skill ?startDate ?endDate
            WHERE {{
                ?e rdf:type local:experience .
                ?e local:jobTitle ?jobTitle .
                ?e local:profession ?profession
                ?e local:skill ?skill .
                ?e local:startDate ?startDate .
                ?e local:endDate ?endDate .
            }}
        '''
        
        result = graph.query(q, initBindings={'e': experience_URI})
        df = DataFrame(result, columns=result.vars)
        return df.to_json()
        
    
    ########################################
    # USER SECTION
    ########################################
    def create_for_user(graph, user_id, job_title, profession_id, skills, start_date, end_date):
        user_URI = URIRef(PERSON + str(user_id))
        experience_URI = WorkExperience.create(graph, job_title, profession_id, skills, start_date, end_date)
        
        # Link experience to user
        graph.add((user_URI, LOCAL.experience, experience_URI))
        graph.serialize(destination=GRAPH_FILE)
        
        return experience_URI
    
    
    def get_all_by_user_id(graph, user_id):
        user_URI = URIRef(PERSON + str(user_id))
        
        q = f'''
            SELECT ?e ?jobTitle ?profession ?skill ?startDate ?endDate
            WHERE {{
                ?p rdf:type foaf:Person .
                ?p local:experience ?d .
                ?e rdf:type local:experience .
                ?e local:jobTitle ?jobTitle .
                ?e local:profession ?profession
                ?e local:skill ?skill .
                ?e local:startDate ?startDate .
                ?e local:endDate ?endDate .
            }}
        '''
        result = graph.query(q, initBindings={'p': user_URI})
        df = DataFrame(result, columns=result.vars)
        return df.to_json()
    
    
    def delete_from_user(graph, user_id, experience_id):
        # Delete from DB
        experience = DBWorkExperience.query.get(experience_id)

        if (experience != None):
            db.session.delete(experience)
            db.session.commit()
        
        user_URI = URIRef(PERSON + str(user_id))
        experience_URI = URIRef(EXPERIENCE + str(experience_id))
        
        # Unlink experience from user
        graph.remove((user_URI, LOCAL.experience, experience_URI))
        
        WorkExperience.delete(graph, experience_id)
        graph.serialize(destination=GRAPH_FILE)
        

    ########################################
    # VACANCY SECTION
    ########################################
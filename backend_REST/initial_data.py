import hashlib
from rdflib.namespace import FOAF, RDF, OWL

from config import GRAPH_FILE

from backend_REST.models.user import User
from backend_REST.models.enterprise import Enterprise
from backend_REST.models.vacancy import Vacancy
from backend_REST.models.diploma import Diploma
from backend_REST.models.work_experience import WorkExperience
from backend_REST.models.skill import Skill
from backend_REST.models.language import Language

def clear_graph(app, graph):
    app.logger.info("Resetting GRAPH: " + GRAPH_FILE + "...")
    
    # Clear graph
    graph.remove((None, None, None))
    # Clear file
    open(GRAPH_FILE, 'w').close()

def set_initial_graph_properties(graph):
    # TODO : Add more?
    graph.add((FOAF.knows, RDF.type, OWL.SymmetricProperty))


def set_initial_graph_data(graph):
    set_users(graph)
    set_enterprises(graph)
    set_vacancies(graph)
    set_diplomas(graph)
    set_experiences(graph)
    set_skills(graph)
    set_languages(graph)


def set_users(graph):
    secret_password = hashlib.sha256("123".encode('utf-8')).hexdigest()

    User.create(graph, "Joris", "Bertram", "joris@gmail.com", secret_password)
    User.create(graph, "Brent", "Zoomers", "brent@gmail.com", secret_password)
    User.create(graph, "Wouter", "Grootjans", "wouter@gmail.com", secret_password)
    User.create(graph, "Gwendoline", "Nijssen", "gwennie@gmail.com", secret_password)


def set_enterprises(graph):
    pass


def set_vacancies(graph):
    # TODO: after enterprise are done set enterprise URI to one in 'set_enterprise'
    Vacancy.create(graph, 1, 1, "software_developer", "2022-12-12", "2023-01-12", 2796491)
    Vacancy.create(graph, 1, 1, "data_engineer", "2022-12-12", "2023-01-12", 2796491)
    Vacancy.create(graph, 1, 1, "data_analyst", "2022-12-12", "2023-01-12", 2796491)
    Vacancy.create(graph, 1, 1, "data_scientist", "2022-12-12", "2023-01-12", 2796491)


def set_diplomas(graph):
    Diploma.create_for_user(graph, 1, "bachelor", "computer_science", "uHasselt", "2018-09-01", "2022-06-30")
    Diploma.create_for_user(graph, 2, "bachelor", "architect", "uHasselt", "2018-09-01", "2022-06-30")
    Diploma.create_for_user(graph, 3, "bachelor", "biology", "uHasselt", "2018-09-01", "2022-06-30")
    Diploma.create_for_user(graph, 4, "bachelor", "chemistry", "uHasselt", "2018-09-01", "2022-06-30")
    
    Diploma.create_for_vacancy(graph, 1, "bachelor", "computer_science", "uHasselt", "2018-09-01", "2022-06-30")
    Diploma.create_for_vacancy(graph, 2, "bachelor", "computer_science", "uHasselt", "2018-09-01", "2022-06-30")
    Diploma.create_for_vacancy(graph, 3, "bachelor", "computer_science", "uHasselt", "2018-09-01", "2022-06-30")
    Diploma.create_for_vacancy(graph, 4, "bachelor", "computer_science", "uHasselt", "2018-09-01", "2022-06-30")


def set_experiences(graph):
    WorkExperience.create_for_user(graph, 1, "Web Developer", ["leadership", "teamwork"], "2018-09-01", "2022-06-30")


def set_skills(graph):
    Skill.add_to_user(graph, 1, "leadership")
    Skill.add_to_user(graph, 1, "teamwork")
    
    Skill.add_to_vacancy(graph, 1, "teamwork")
    Skill.add_to_vacancy(graph, 2, "teamwork")
    Skill.add_to_vacancy(graph, 3, "teamwork")
    Skill.add_to_vacancy(graph, 4, "teamwork")


def set_languages(graph):
    Language.add_to_user(graph, 1, "english")
    Language.add_to_user(graph, 1, "dutch")

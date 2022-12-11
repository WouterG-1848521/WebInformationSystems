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
    Enterprise.create(graph, "CS Enterprise", 23, 30, "Hasselt", 123, "cs.enterprise@gmail.com", "cs.com", 1, "Computer Science Agency", "2796491")


def set_vacancies(graph):
    Vacancy.create(graph, 1, 1, "Q593644", "2022-12-12", "2023-01-12", "2796491", "Description", "Responsibilities", 3100)
    Vacancy.create(graph, 1, 1, "Q901", "2022-12-12", "2023-01-12", "2796491", "Description", "Responsibilities", 3100)
    Vacancy.create(graph, 1, 1, "Q9402", "2022-12-12", "2023-01-12", "2796491", "Description", "Responsibilities", 3100)
    Vacancy.create(graph, 1, 1, "Q11063", "2022-12-12", "2023-01-12", "2796491", "Description", "Responsibilities", 3100)


def set_diplomas(graph):
    Diploma.create_for_user(graph, 1, "bachelor", "Q21198", "uHasselt", "2018-09-01", "2022-06-30")
    Diploma.create_for_user(graph, 2, "bachelor", "Q431", "uHasselt", "2018-09-01", "2022-06-30")
    Diploma.create_for_user(graph, 3, "bachelor", "Q420", "uHasselt", "2018-09-01", "2022-06-30")
    Diploma.create_for_user(graph, 4, "bachelor", "Q2329", "uHasselt", "2018-09-01", "2022-06-30")
    
    Diploma.create_for_vacancy(graph, 1, "bachelor", "Q21198", "uHasselt", "2018-09-01", "2022-06-30")
    Diploma.create_for_vacancy(graph, 2, "bachelor", "Q431", "uHasselt", "2018-09-01", "2022-06-30")
    Diploma.create_for_vacancy(graph, 3, "bachelor", "Q420", "uHasselt", "2018-09-01", "2022-06-30")
    Diploma.create_for_vacancy(graph, 4, "bachelor", "Q2329", "uHasselt", "2018-09-01", "2022-06-30")


def set_experiences(graph):
    WorkExperience.create_for_user(graph, 1, "Computer Science Student", "Q9402", ["Q24288", "Q80006"], "2018-09-01", "2022-06-30")


def set_skills(graph):
    Skill.add_to_user(graph, 1, "Q24288")
    Skill.add_to_user(graph, 1, "Q80006")
    
    Skill.add_to_vacancy(graph, 1, "Q24288")
    Skill.add_to_vacancy(graph, 2, "Q80006")
    Skill.add_to_vacancy(graph, 3, "Q102066")
    Skill.add_to_vacancy(graph, 4, "Q167612")


def set_languages(graph):
    Language.add_to_user(graph, 1, "Q1860")
    Language.add_to_user(graph, 1, "Q7411")

import hashlib
from rdflib.namespace import FOAF, RDF, OWL
from backend_REST.graph import LOCAL

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
    graph.add((LOCAL.enterprise, OWL.equivalentClass, FOAF.Organization))
    graph.add((LOCAL.person, OWL.equivalentClass, FOAF.Person))


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
    # create(graph, name, lat, long, address, phone, email, website, owner, description, location)
    Enterprise.create(graph, "WEB Enterprise", 23, 30, "Hasselt straat 2", "123", "web.enterprise@gmail.com", "https://web.com", 1, "Enterpise", "2796491")
    Enterprise.create(graph, "KU Leuven", 50, 30, "Leuven straat 7", "0478521632", "kul@gmail.com", "https://kul.be", 2, "Universiteit", "2792482")
    Enterprise.create(graph, "Aldi", 25, 31, "Aarschot straat 1", "013558899", "aldi.aarschot@gmail.com", "https://aldi.be", 3, "Winkel", "2793406")
    Enterprise.create(graph, "Colruyt", 30, 20, "Scherpenheuvel straat 8", "0475654789", "colruyt.scherp@gmail.com", "https://colruyt.be", 3, "Winkel", "2802865")


def set_vacancies(graph):
    # create(graph, enterprise_id, maintainer_id, job_title, start_date, end_date, location_id, job_desciption, job_responsibilities, job_salary)
    Vacancy.create(graph, 1, 1, "Web Developer", "2022-12-12", "2023-01-12", "2796491", "Develop for the web", "Developing web applicaties", 3100)
    Vacancy.create(graph, 2, 2, "Teaching assistant", "2022-12-12", "2023-01-12", "2796492", "Teaching assistant", "Examens maken", 2800)
    Vacancy.create(graph, 3, 3, "Kassa medewerker", "2022-12-12", "2023-01-12", "2796493", "Kassa medewerker", "Werken met klanten", 2300)
    # Vacancy.create(graph, 3, 3, "Q11063", "2022-12-12", "2023-01-12", "2796494", "kassamedewerker", "Werken met klanten", 2200)
    Vacancy.create(graph, 4, 3, "Manager", "2022-12-12", "2023-01-12", "2796494", "Manager", "Managen", 2900)


def set_diplomas(graph):
    # create_for_user(graph, user_id, degree, discipline_id, institiution, startDate, endDate)
    Diploma.create_for_user(graph, 1, "bachelor", "Q21198", "uHasselt", "2018-09-01", "2022-06-30")
    Diploma.create_for_user(graph, 2, "master", "Q21198", "KUL", "2018-09-01", "2022-06-30")
    # Diploma.create_for_user(graph, 2, "bachelor", "Q431", "uHasselt", "2018-09-01", "2022-06-30")
    Diploma.create_for_user(graph, 3, "bachelor", "Q420", "uHasselt", "2018-09-01", "2022-06-30")
    Diploma.create_for_user(graph, 4, "bachelor", "Q2329", "uHasselt", "2018-09-01", "2022-06-30")
    
    # create_for_vacancy(graph, vacancy_id, degree, discipline_id, institiution, startDate, endDate)
    Diploma.create_for_vacancy(graph, 1, "bachelor", "Q21198", "uHasselt", "2018-09-01", "2022-06-30")
    Diploma.create_for_vacancy(graph, 2, "bachelor", "Q431", "uHasselt", "2018-09-01", "2022-06-30")
    Diploma.create_for_vacancy(graph, 3, "bachelor", "Q420", "uHasselt", "2018-09-01", "2022-06-30")
    Diploma.create_for_vacancy(graph, 4, "bachelor", "Q2329", "uHasselt", "2018-09-01", "2022-06-30")
    Diploma.create_for_vacancy(graph, 5, "master", "Q21198", "ANYWHERE", "000-00-00", "000-00-00")


def set_experiences(graph):
    # create_for_user(graph, user_id, job_title, profession_id, skills, start_date, end_date)
    WorkExperience.create_for_user(graph, 1, "Computer Science Student", "Q9402", ["Q24288"], "2018-09-01", "2022-06-30")


def set_skills(graph):
    Skill.add_to_user(graph, 1, "Q24288")
    Skill.add_to_user(graph, 1, "Q80006")
    
    Skill.add_to_vacancy(graph, 1, "Q24288")
    Skill.add_to_vacancy(graph, 2, "Q80006")
    Skill.add_to_vacancy(graph, 3, "Q102066")
    Skill.add_to_vacancy(graph, 4, "Q167612")


def set_languages(graph):
    Language.add_to_user(graph, 1, "Q1860")
    Language.add_to_user(graph, 3, "Q7411")

    Language.add_to_vacancy(graph, 1, "Q1860")
    Language.add_to_vacancy(graph, 2, "Q7411")

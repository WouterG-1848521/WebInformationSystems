from flask import request
from pandas import DataFrame

from backend_REST.models.user import User

from backend_REST.matching import matchOnVacancy_allParameters, matchOnVacancy_anyParameters, matchOnPerson
from backend_REST.matching import matchVacancy_discipline, matchVacancy_language, matchVacancy_skill, matchVacancy_experience
from backend_REST.matching import matchPerson_discipline, matchPerson_language, matchPerson_skill, matchPerson_experience


def create_matching_routes(app, graph):
    ########################################
    # MATCHING ROUTES - USER -> VACANCIES
    ########################################

    @app.route("/users/<int:user_id>/matches", methods=['GET'])
    def get_all_vacancy_matches_for_user(user_id):
        personID = user_id
        personID = int(personID)
        
        return matchOnPerson(graph, personID)

    @app.route("/users/<int:user_id>/matches/skills", methods=['GET'])
    def get_all_vacancy_matches_for_user_by_skills(user_id):
        personID = user_id
        personID = int(personID)
        
        return matchPerson_skill(graph, personID)

    @app.route("/users/<int:user_id>/matches/discipline", methods=['GET'])
    def get_all_vacancy_matches_for_user_by_discipline(user_id):
        personID = user_id
        personID = int(personID)
        
        return matchPerson_discipline(graph, personID)

    @app.route("/users/<int:user_id>/matches/languages", methods=['GET'])
    def get_all_vacancy_matches_for_user_by_languages(user_id):
        personID = user_id
        personID = int(personID)
        
        return matchPerson_language(graph, personID)
    
    @app.route("/users/<int:user_id>/matches/experience", methods=['GET'])
    def get_all_vacancy_matches_for_user_by_experiences(user_id):
        personID = user_id
        personID = int(personID)
        
        return matchPerson_experience(graph, personID)

    ########################################
    # MATCHING ROUTES - VACANCY -> USERS
    ########################################

    @app.route("/vacancies/<int:vacancy_id>/matches", methods=['GET'])
    def get_all_user_matches_for_vacancy(vacancy_id):
        vacancyID = vacancy_id
        vacancyID = int(vacancyID)

        return matchOnVacancy_anyParameters(graph, vacancyID)

    @app.route("/vacancies/<int:vacancy_id>/matchesAll", methods=['GET'])
    def get_all_user_matches_for_vacancyall(vacancy_id):
        vacancyID = vacancy_id
        vacancyID = int(vacancyID)

        return matchOnVacancy_allParameters(graph, vacancyID)

    @app.route("/vacancies/<int:vacancy_id>/matches/skills", methods=['GET'])
    def get_all_user_matches_for_vacancy_by_skills(vacancy_id):
        vacancyID = vacancy_id
        vacancyID = int(vacancyID)

        return matchVacancy_skill(graph, vacancyID)

    @app.route("/vacancies/<int:vacancy_id>/matches/discipline", methods=['GET'])
    def get_all_user_matches_for_vacancy_by_discipline(vacancy_id):
        vacancyID = vacancy_id
        vacancyID = int(vacancyID)

        return matchVacancy_discipline(graph, vacancyID)

    @app.route("/vacancies/<int:vacancy_id>/matches/languages", methods=['GET'])
    def get_all_user_matches_for_vacancy_by_languages(vacancy_id):
        vacancyID = vacancy_id
        vacancyID = int(vacancyID)

        return matchVacancy_language(graph, vacancyID)

    # @app.route("/vacancies/<int:vacancy_id>/matches/experience", methods=['GET'])
    # def get_all_user_matches_for_vacancy_by_exps(vacancy_id):
    #     vacancyID = vacancy_id
    #     vacancyID = int(vacancyID)

    #     return matchVacancy_experience(graph, vacancyID)

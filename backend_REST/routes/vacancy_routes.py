from flask_login import login_required
from flask import request
from pandas import DataFrame
import json

from backend_REST.queries import query_getVacancy, check_enterprise, check_maintainer, check_valid_vacancy, check_person, query_personByDiploma
from backend_REST.queries import query_getDiplomasFromVacancy, query_getSkillsFromVacancy, query_personBySkill, query_getLanguagesFromVacancy, query_personByLanguage
from backend_REST.queries import query_getExperiencesFromPerson, query_getDiplomasFromPerson, query_getSkillsFromPerson, query_getLanguagesFromPerson, query_getExperienceFromVacancy
from backend_REST.queries import query_personByExperience, query_vacancyByDiploma, query_vacancyBySkill, query_vacancyByLanguage, query_vacancyByExperience

from backend_REST import session

from backend_REST.models.vacancy import Vacancy
from backend_REST.models.enterprise import Enterprise

from backend_REST.models.skill import Skill
from backend_REST.models.language import Language
from backend_REST.models.diploma import Diploma

from backend_REST.models.validator import Validator
from backend_REST.models.response import Response

from backend_REST.matching import matchOnVacancy_allParameters, matchOnVacancy_anyParameters, matchOnPerson

def create_vacancy_routes(app, graph):
    ########################################
    # VACANCY ROUTES - BASICS
    ########################################
    @app.route("/enterprises/<int:enterprise_id>/vacancies/", methods=['POST'])
    def add_vacancy(enterprise_id):
        data = request.form

        if not (check_maintainer(graph, session['_user_id'], enterprise_id)):
            return "only maintainer of enterprise can add vacancies"

        if not Validator.valid_date(data["startDate"]):
            return Response.start_date_not_valid()
        if not Validator.valid_date(data["endDate"]):
            return Response.end_date_not_valid()

        vacancy_id = Vacancy.create(graph, enterprise_id, session["_user_id"],
                                    data["jobTitle"], data["startDate"], data["endDate"], data["location_id"])

        return f"Created vacancy {vacancy_id}."

    @app.route("/enterprises/<int:enterprise_id>/vacancies/<int:vacancy_id>", methods=['PUT'])
    def update_vacancy(enterprise_id, vacancy_id):
        data = request.form

        if not (check_maintainer(graph, session['_user_id'], enterprise_id)):
            return "only maintainer of enterprise can update vacancies"

        if not Validator.valid_date(data["startDate"]):
            return Response.start_date_not_valid()
        if not Validator.valid_date(data["endDate"]):
            return Response.end_date_not_valid()

        Vacancy.update_posted_by(graph, vacancy_id, session["_user_id"])
        Vacancy.update_job_title(graph, vacancy_id, data["jobTitle"])
        Vacancy.update_start_date(graph, vacancy_id, data["startDate"])
        Vacancy.update_end_date(graph, vacancy_id, data["endDate"])

        return f"Updated vacancy {vacancy_id}"

    @app.route("/enterprises/<int:enterprise_id>/vacancies/<int:vacancy_id>", methods=['DELETE'])
    def remove_vacancy(enterprise_id, vacancy_id):
        data = request.form

        if not (check_maintainer(graph, session['_user_id'], enterprise_id)):
            return "only maintainer of enterprise can delete vacancies"

        Vacancy.delete(graph, vacancy_id)

        return f"Removed vacancy {vacancy_id}"

    @app.route("/enterprises/<int:enterprise_id>/vacancies/", methods=['GET'])
    def get_all_vacancies_of_enterprise(enterprise_id):
        return Vacancy.get_by_enterprise_id(graph, enterprise_id)

    ########################################
    # VACANCY ROUTES - DIPLOMA
    ########################################

    @app.route("/enterprises/<int:enterprise_id>/vacancies/<int:vacancy_id>/diplomas", methods=["POST"])
    def create_vacancy_diploma(enterprise_id, vacancy_id):
        data = request.form

        if not (check_maintainer(graph, session['_user_id'], enterprise_id)):
            return "only maintainer of enterprise can create vacancy diploma"

        if not Validator.valid_degree(data["degree"]):
            return Response.degree_not_valid()

        if not Validator.valid_date(data["startDate"]):
            return Response.start_date_not_valid()
        if not Validator.valid_date(data["endDate"]):
            return Response.end_date_not_valid()

        # TODO: check if profession in list

        diploma_id = Diploma.create_for_vacancy(graph, vacancy_id, data["degree"], data["profession"],
                                                data["institution"], data["startDate"], data["endDate"], data["location_id"])
        return f"Created diploma {diploma_id } for vacancy {vacancy_id}."

    @app.route("/enterprises/<int:enterprise_id>/vacancies/<int:vacancy_id>/diplomas", methods=["GET"])
    def get_vacancy_diplomas(enterprise_id, vacancy_id):
        return Diploma.get_all_by_vacancy_id(graph, vacancy_id)

    @app.route("/enterprises/<int:enterprise_id>/vacancies/<int:vacancy_id>/diplomas/<int:diploma_id>", methods=["GET"])
    def get_vacancy_diploma(enterprise_id, vacancy_id, diploma_id):
        return Diploma.get_by_id(graph, diploma_id)

    @app.route("/enterprises/<int:enterprise_id>/vacancies/<int:vacancy_id>/diplomas/<int:diploma_id>", methods=["PUT"])
    def update_vacancy_diploma(enterprise_id, vacancy_id, diploma_id):
        data = request.form

        if not (check_maintainer(graph, session['_user_id'], enterprise_id)):
            return "only maintainer of enterprise can update vacancy diploma"

        if not Validator.valid_degree(data["degree"]):
            return Response.degree_not_valid()

        if not Validator.valid_date(data["startDate"]):
            return Response.start_date_not_valid()
        if not Validator.valid_date(data["endDate"]):
            return Response.end_date_not_valid()

        # TODO: check if profession in list

        Diploma.update(graph, diploma_id, data["degree"], data["profession"],
                       data["institution"], data["startDate"], data["endDate"])
        return f"Updated diploma {diploma_id}."

    @app.route("/enterprises/<int:enterprise_id>/vacancies/<int:vacancy_id>/diplomas/<int:diploma_id>", methods=["DELETE"])
    @login_required
    def delete_vacancy_diploma(enterprise_id, vacancy_id, diploma_id):

        # if session['_user_id'] != user_id:
        #     return Response.unauthorized_access_wrong_user()

        # maintainerID = data["maintainerID"]
        # maintainerID = int(maintainerID)

        if not (check_maintainer(graph, session['_user_id'], enterprise_id)):
            return "only maintainer of enterprise can delete vacancy diploma"

        Diploma.delete_from_vacany(graph, vacancy_id, diploma_id)
        return f"Deleted diploma {diploma_id} from vacancy {vacancy_id}."

    ########################################
    # VACANCY ROUTES - SKILLS
    ########################################

    @app.route("/enterprises/<int:enterprise_id>/vacancies/<int:vacancy_id>/skills", methods=['POST'])
    def add_skill_to_vacancy(enterprise_id, vacancy_id):
        data = request.form

        if not (check_maintainer(graph, session['_user_id'], enterprise_id)):
            return "only maintainer of enterprise can add skill to vacancy"

        # TODO: check if skill in list

        Skill.add_to_vacancy(graph, vacancy_id, data["skill"])

        return f"Added skill {data['skill']} to vacancy {vacancy_id}."

    @app.route("/enterprises/<int:enterprise_id>/vacancies/<int:vacancy_id>/skills", methods=['GET'])
    def get_all_skills_by_vacancy_id(enterprise_id, vacancy_id):

        return Skill.get_all_by_vacancy_id(graph, vacancy_id)

    @app.route("/enterprises/<int:enterprise_id>/vacancies/<int:vacancy_id>/skills/<string:skill>", methods=['DELETE'])
    def remove_skill_from_vacancy(enterprise_id, vacancy_id, skill):

        if not (check_maintainer(graph, session['_user_id'], enterprise_id)):
            return "only maintainer of enterprise can delete skill from vacancy"

        Skill.remove_from_vacancy(graph, vacancy_id, skill)

        return f"Removed skill {skill} from vacancy {vacancy_id}."

    ########################################
    # VACANCY ROUTES - LANGUAGES
    ########################################

    @app.route("/enterprises/<int:enterprise_id>/vacancies/<int:vacancy_id>/languages", methods=['POST'])
    def add_language_to_vacancy(enterprise_id, vacancy_id):
        data = request.form

        if not (check_maintainer(graph, session['_user_id'], enterprise_id)):
            return "only maintainer of enterprise can delete vacancy diploma"
        # TODO: check if language in list

        Language.add_to_vacancy(graph, vacancy_id, data["language"])

        return f"Added language {data['language']} to vacancy {vacancy_id}."

    @app.route("/enterprises/<int:enterprise_id>/vacancies/<int:vacancy_id>/languages", methods=['GET'])
    def get_all_languages_by_vacancy_id(enterprise_id, vacancy_id):

        return Language.get_all_by_vacancy_id(graph, vacancy_id)

    @app.route("/enterprises/<int:enterprise_id>/vacancies/<int:vacancy_id>/languages/<string:language>", methods=['DELETE'])
    def remove_language_from_vacancy(enterprise_id, vacancy_id, language):

        if not (check_maintainer(graph, session['_user_id'], enterprise_id)):
            return f'only maintainer of enterprise can delete language from vacancy'

        Language.remove_from_vacancy(graph, vacancy_id, language)

        return f"Removed language {language} from vacancy {vacancy_id}."


    # find persons that have minimum 1 match with the given vacancy
    @app.route("/vacancy/match1", methods=['POST'])
    def match_vacancy():
        data = request.form

        if not ("vacancyID" in data):   # search people that match the given vacancy
            return "Missing vacancyID parameter", 400

        vacancyID = data["vacancyID"]
        vacancyID = int(vacancyID)

        return matchOnVacancy_anyParameters(graph, vacancyID)

    @app.route("/vacancy/matchall", methods=['POST'])
    def match_vacancyAll():
        data = request.form

        if not ("vacancyID" in data):   # search people that match the given vacancy
            return "Missing vacancyID parameter", 400

        vacancyID = data["vacancyID"]
        vacancyID = int(vacancyID)

        return matchOnVacancy_allParameters(graph, vacancyID)

    # find vacancies for a given person that matches with any of the qualifications of the person
    @app.route("/vacancy/find", methods=['POST'])
    def find_vacancy():
        data = request.form

        if not ("personID" in data):
            return "Missing personID parameter", 400
        personID = data["personID"]
        personID = int(personID)
        
        return matchOnPerson(graph, personID)

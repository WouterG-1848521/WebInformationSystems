from flask_login import login_required
from flask import request, make_response, jsonify
from pandas import DataFrame
import json

from backend_REST.queries import check_maintainer

from backend_REST import session

from backend_REST.models.vacancy import Vacancy
from backend_REST.models.enterprise import Enterprise

from backend_REST.models.skill import Skill
from backend_REST.models.language import Language
from backend_REST.models.diploma import Diploma

from backend_REST.models.validator import Validator
from backend_REST.models.response import Response


def create_vacancy_routes(app, graph):
    ########################################
    # VACANCY ROUTES - BASICS
    ########################################
    @app.route("/enterprises/<int:enterprise_id>/vacancies/", methods=['POST'])
    def add_vacancy(enterprise_id):
        data = request.form

        if not (check_maintainer(graph, enterprise_id, session['_user_id'])):
            return Response.make_response_for_content_type('application/json', message="Only maintainer of enterprise can add vacancies")
            return "only maintainer of enterprise can add vacancies"

        if not Validator.valid_date(data["startDate"]):
            return Response.start_date_not_valid()
        if not Validator.valid_date(data["endDate"]):
            return Response.end_date_not_valid()


        vacancy_id = Vacancy.create(graph, enterprise_id, session["_user_id"],
                                    data["jobTitle"], data["startDate"], data["endDate"], data["profession"], data["location_id"], 
                                    data["jobDescription"], data["jobResponsibilities"], data["jobSalary"])

        vacancyJSON = json.loads(Vacancy.get_by_id(graph, vacancy_id))
        return Response.format_vacancies_json(vacancyJSON)

    @app.route("/enterprises/<int:enterprise_id>/vacancies/<int:vacancy_id>", methods=['PUT'])
    def update_vacancy(enterprise_id, vacancy_id):
        data = request.form

        if not (check_maintainer(graph, enterprise_id, session['_user_id'])):
            return Response.make_response_for_content_type("application/json", "Only maintainer of enterprise can update vacancies", 401)
            return "only maintainer of enterprise can update vacancies"

        if not Validator.valid_date(data["startDate"]):
            return Response.start_date_not_valid()
        if not Validator.valid_date(data["endDate"]):
            return Response.end_date_not_valid()

        Vacancy.update_posted_by(graph, vacancy_id, session["_user_id"])
        Vacancy.update_job_title(graph, vacancy_id, data["jobTitle"])
        Vacancy.update_start_date(graph, vacancy_id, data["startDate"])
        Vacancy.update_end_date(graph, vacancy_id, data["endDate"])
        Vacancy.update_location(graph, vacancy_id, data["location_id"])
        Vacancy.update_job_description(graph, vacancy_id, data["jobDescription"])
        Vacancy.update_job_responsibilities(graph, vacancy_id, data["jobResponsibilities"])
        Vacancy.update_job_salary(graph, vacancy_id, data["jobSalary"])
        

        vacancyJSON = json.loads(Vacancy.get_by_id(graph, vacancy_id))
        return Response.format_vacancies_json(vacancyJSON)

    @app.route("/enterprises/<int:enterprise_id>/vacancies/<int:vacancy_id>", methods=['DELETE'])
    def remove_vacancy(enterprise_id, vacancy_id):
        data = request.form

        if not (check_maintainer(graph, enterprise_id, session['_user_id'])):
            return Response.make_response_for_content_type('application/json', message="Only maintainer of enterprise can delete vacancies")
            return "only maintainer of enterprise can delete vacancies"

        Vacancy.delete(graph, vacancy_id)
        
        return Response.make_response_for_content_type('application/json', message=f"Delete vacancy {vacancy_id}.")

    @app.route("/enterprises/<int:enterprise_id>/vacancies/", methods=['GET'])
    def get_all_vacancies_of_enterprise(enterprise_id):
        vacanciesJson = json.loads(Vacancy.get_by_enterprise_id(graph, enterprise_id))
        vacanciesJson = Response.format_vacancies_json(vacanciesJson)
        return Response.make_response_for_content_type_and_data(request.headers.get("Accept", "text/html"), data=vacanciesJson, template="vacancies.html")

    ########################################
    # VACANCY ROUTES - DIPLOMA
    ########################################

    @app.route("/enterprises/<int:enterprise_id>/vacancies/<int:vacancy_id>/diplomas", methods=["POST"])
    def create_vacancy_diploma(enterprise_id, vacancy_id):
        data = request.form

        if not (check_maintainer(graph, enterprise_id, session['_user_id'])):
            return Response.make_response_for_content_type('application/json', message="Only maintainer of enterprise can create vacancy diploma")
            return "only maintainer of enterprise can create vacancy diploma"

        if not Validator.valid_degree(data["degree"]):
            return Response.degree_not_valid()

        if not Validator.valid_date(data["startDate"]):
            return Response.start_date_not_valid()
        if not Validator.valid_date(data["endDate"]):
            return Response.end_date_not_valid()

        if not Validator.valid_discipline(data["discipline"]):
            return Response.discipline_not_valid()

        diploma_id = Diploma.create_for_vacancy(graph, vacancy_id, data["degree"], data["discipline"],
                                                data["institution"], data["startDate"], data["endDate"])
        
        return Response.make_response_for_content_type('application/json', message=f"Created diploma {diploma_id } for vacancy {vacancy_id}.")

    @app.route("/enterprises/<int:enterprise_id>/vacancies/<int:vacancy_id>/diplomas", methods=["GET"])
    def get_vacancy_diplomas(enterprise_id, vacancy_id):
        diplomasJSON = json.loads(Diploma.get_all_by_vacancy_id(graph, vacancy_id))
        diplomasJSON = Response.format_diplomas_json(diplomasJSON)
        
        return Response.make_response_for_content_type_and_data(request.headers.get("Accept", "text/html"), data=diplomasJSON, template="diplomas.html")

    @app.route("/enterprises/<int:enterprise_id>/vacancies/<int:vacancy_id>/diplomas/<int:diploma_id>", methods=["GET"])
    def get_vacancy_diploma(enterprise_id, vacancy_id, diploma_id):
        diplomasJSON = json.loads(Diploma.get_by_id(graph, diploma_id))
        diplomasJSON = Response.format_diplomas_json(diplomasJSON)
        
        return Response.make_response_for_content_type_and_data(request.headers.get("Accept", "text/html"), data=diplomasJSON, template="diploma.html")

    @app.route("/enterprises/<int:enterprise_id>/vacancies/<int:vacancy_id>/diplomas/<int:diploma_id>", methods=["PUT"])
    def update_vacancy_diploma(enterprise_id, vacancy_id, diploma_id):
        data = request.form

        if not (check_maintainer(graph, enterprise_id, session['_user_id'])):
            return Response.make_response_for_content_type('application/json', message="Only maintainer of enterprise can update vacancy diploma")

        if not Validator.valid_degree(data["degree"]):
            return Response.degree_not_valid()

        if not Validator.valid_date(data["startDate"]):
            return Response.start_date_not_valid()
        if not Validator.valid_date(data["endDate"]):
            return Response.end_date_not_valid()

        if not Validator.valid_discipline(data["discipline"]):
            return Response.discipline_not_valid()

        Diploma.update(graph, diploma_id, data["degree"], data["discipline"],
                       data["institution"], data["startDate"], data["endDate"])
        
        diplomasJSON = json.loads(Diploma.get_by_id(graph, diploma_id))
        return Response.format_diplomas_json(diplomasJSON)
        # return f"Updated diploma {diploma_id}."

    @app.route("/enterprises/<int:enterprise_id>/vacancies/<int:vacancy_id>/diplomas/<int:diploma_id>", methods=["DELETE"])
    @login_required
    def delete_vacancy_diploma(enterprise_id, vacancy_id, diploma_id):

        # if session['_user_id'] != user_id:
        #     return Response.unauthorized_access_wrong_user()

        # maintainerID = data["maintainerID"]
        # maintainerID = int(maintainerID)

        if not (check_maintainer(graph, enterprise_id, session['_user_id'])):
            return Response.make_response_for_content_type('application/json', message="Only maintainer of enterprise can delete vacancy diploma")

        Diploma.delete_from_vacany(graph, vacancy_id, diploma_id)

        return Response.make_response_for_content_type('application/json', message=f"Deleted diploma {diploma_id} from vacancy {vacancy_id}.")

    ########################################
    # VACANCY ROUTES - SKILLS
    ########################################

    @app.route("/enterprises/<int:enterprise_id>/vacancies/<int:vacancy_id>/skills", methods=['POST'])
    def add_skill_to_vacancy(enterprise_id, vacancy_id):
        data = request.form

        if not (check_maintainer(graph, enterprise_id, session['_user_id'])):
            return Response.make_response_for_content_type('application/json', message="Only maintainer of enterprise can add skill to vacancy")
            return "only maintainer of enterprise can add skill to vacancy"

        if not Validator.valid_skill(data["skill"]):
            return Response.skill_not_valid()

        Skill.add_to_vacancy(graph, vacancy_id, data["skill"])

        skillsJSON = json.loads(Skill.get_all_by_vacancy_id(graph, vacancy_id))
        return Response.format_skills_json(skillsJSON)

    @app.route("/enterprises/<int:enterprise_id>/vacancies/<int:vacancy_id>/skills", methods=['GET'])
    def get_all_skills_by_vacancy_id(enterprise_id, vacancy_id):
        skillsJSON = json.loads(Skill.get_all_by_vacancy_id(graph, vacancy_id))
        skillsJSON = Response.format_skills_json(skillsJSON)
        
        return Response.make_response_for_content_type_and_data(request.headers.get("Accept", "text/html"), data=skillsJSON, template="skills.html")

    @app.route("/enterprises/<int:enterprise_id>/vacancies/<int:vacancy_id>/skills/<string:skill>", methods=['DELETE'])
    def remove_skill_from_vacancy(enterprise_id, vacancy_id, skill):

        if not (check_maintainer(graph, enterprise_id, session['_user_id'])):
            return Response.make_response_for_content_type('application/json', message="Only maintainer of enterprise can delete skill from vacancy")
            return "only maintainer of enterprise can delete skill from vacancy"

        Skill.remove_from_vacancy(graph, vacancy_id, skill)

        return Response.make_response_for_content_type('application/json', message=f"Removed skill {skill} from vacancy {vacancy_id}.")    
        return f"Removed skill {skill} from vacancy {vacancy_id}."

    ########################################
    # VACANCY ROUTES - LANGUAGES
    ########################################

    @app.route("/enterprises/<int:enterprise_id>/vacancies/<int:vacancy_id>/languages", methods=['POST'])
    def add_language_to_vacancy(enterprise_id, vacancy_id):
        data = request.form

        if not (check_maintainer(graph, enterprise_id, session['_user_id'])):
            return Response.make_response_for_content_type('application/json', message="Only maintainer of enterprise can add language to vacancy")
            return "only maintainer of enterprise can delete vacancy diploma"

        if not Validator.valid_language(data["language"]):
            return Response.language_not_valid()

        Language.add_to_vacancy(graph, vacancy_id, data["language"])
        
        languagesJSON = json.loads(Language.get_all_by_vacancy_id(graph, vacancy_id))
        return Response.format_languages_json(languagesJSON)
    
    @app.route("/enterprises/<int:enterprise_id>/vacancies/<int:vacancy_id>/languages", methods=['GET'])
    def get_all_languages_by_vacancy_id(enterprise_id, vacancy_id):
        languagesJSON = json.loads(Language.get_all_by_vacancy_id(graph, vacancy_id))
        languagesJSON = Response.format_languages_json(languagesJSON)
        
        return Response.make_response_for_content_type_and_data(request.headers.get("Accept", "text/html"), data=languagesJSON, template="languages.html")

    @app.route("/enterprises/<int:enterprise_id>/vacancies/<int:vacancy_id>/languages/<string:language>", methods=['DELETE'])
    def remove_language_from_vacancy(enterprise_id, vacancy_id, language):

        if not (check_maintainer(graph, enterprise_id, session['_user_id'])):
            return Response.make_response_for_content_type('application/json', message="Only maintainer of enterprise can delete language from vacancy")
            return f'only maintainer of enterprise can delete language from vacancy'

        Language.remove_from_vacancy(graph, vacancy_id, language)

        return Response.make_response_for_content_type('application/json', message=f"Removed language {language} from vacancy {vacancy_id}.")
        return f"Removed language {language} from vacancy {vacancy_id}."
from flask import request
from flask_login import login_required, logout_user
import hashlib

from backend_REST import session

from backend_REST.models.user import User
from backend_REST.models.skill import Skill
from backend_REST.models.diploma import Diploma
from backend_REST.models.language import Language
from backend_REST.models.work_experience import WorkExperience

from backend_REST.models.validator import Validator
from backend_REST.models.response import Response


def create_user_routes(app, g):
    ########################################
    # USER ROUTES - BASICS
    ########################################
    @app.route("/users", methods=["GET"])
    def get_all_users():
        return User.get_all(g)

    @app.route("/users", methods=["POST"])
    def create_user():
        data = request.form

        # Encryption must be done before send with HTTP POST, but currently no front-end
        encrypted_password = hashlib.sha256(
            data["password"].encode('utf-8')).hexdigest()

        if not Validator.valid_email(data["email"]):
            return Response.email_not_valid()

        if not User.is_available(data["email"]):
            return Response.email_not_available()

        user_id = User.create(g, data["name"], data["surname"],
                              data["email"], encrypted_password)
        return f"Created user {user_id}."

    @app.route("/users/<int:user_id>", methods=["GET"])
    def get_user(user_id):
        return User.get_by_id(g, user_id)

    @app.route("/users/<int:user_id>", methods=["PUT"])
    @ login_required
    def update_user(user_id):
        data = request.form

        # Check if logged-in user is correct
        if session['_user_id'] != user_id:
            return Response.unauthorized_access_wrong_user()

        if not Validator.same_password(data["password"], data["passwordConfirmation"]):
            return Response.password_not_matching()

        if not Validator.valid_email(data["email"]):
            return Response.email_not_valid()

        if not User.is_available(data["email"]):
            return Response.email_not_available()

        # Encryption must be done before send with HTTP POST, but currently no front-end
        encrypted_password = hashlib.sha256(
            data["password"].encode('utf-8')).hexdigest()

        User.update_user_by_id(g, user_id, data["name"], data["surname"],
                               data["email"], encrypted_password)
        return f"Updated user {user_id}."

    @ app.route("/users/<int:user_id>", methods=["DELETE"])
    @ login_required
    def delete_user(user_id):
        print(f"Trying to delete: {session['_user_id']}")

        # Check if logged-in user is correct
        if session['_user_id'] != user_id:
            return Response.unauthorized_access_wrong_user()

        # Auto logout
        logout_user()

        User.delete(g, user_id)
        return f"Deleted user {user_id}."

    @ app.route("/users/<int:user_id>/profile", methods=["GET"])
    def get_user_profile(user_id):
        return User.get_profile_by_id(g, user_id)

    @ app.route("/users/<int:user_id>/email", methods=["PUT"])
    @ login_required
    def update_user_email(user_id):
        data = request.form

        # Check if logged-in user is correct
        if session['_user_id'] != user_id:
            return Response.unauthorized_access_wrong_user()

        if not Validator.valid_email(data["email"]):
            return Response.email_not_valid()

        if not User.is_available(data["email"]):
            return Response.email_not_available()

        User.update_email(g, user_id, data["email"])
        return f"Updated email of user {user_id}."

    @ app.route("/users/<int:user_id>/phone", methods=["PUT"])
    @ login_required
    def update_user_phone(user_id):
        data = request.form

        # Check if logged-in user is correct
        if session['_user_id'] != user_id:
            return Response.unauthorized_access_wrong_user()

        # TODO: check phone number (hard do to)

        User.update_phone(g, user_id, data["phone"])
        return f"Updated phone of user {user_id}."

    @ app.route("/users/<int:user_id>/location", methods=["PUT"])
    @ login_required
    def update_user_location(user_id):
        data = request.form

        # Check if logged-in user is correct
        if session['_user_id'] != user_id:
            return Response.unauthorized_access_wrong_user()

        User.update_location(g, user_id, data["location_id"])
        return f"Updated location of user {user_id}."

    ########################################
    # USER ROUTES - DIPLOMAS
    ########################################

    @ app.route("/users/<int:user_id>/diplomas", methods=["POST"])
    @ login_required
    def create_user_diploma(user_id):
        data = request.form

        # Check if logged-in user is correct
        if session['_user_id'] != user_id:
            return Response.unauthorized_access_wrong_user()

        if not Validator.valid_date(data["startDate"]):
            return Response.start_date_not_valid()
        if not Validator.valid_date(data["endDate"]):
            return Response.end_date_not_valid()

        if not Validator.valid_degree(data["degree"]):
            return Response.degree_not_valid()

        if not Validator.valid_discipline(data["discipline"]):
            return Response.discipline_not_valid()

        diploma_id = Diploma.create_for_user(g, user_id, data["degree"], data["discipline"],
                                             data["institution"], data["startDate"], data["endDate"])
        return f"Created diploma {diploma_id } for user {user_id}."

    @ app.route("/users/<int:user_id>/diplomas", methods=["GET"])
    def get_user_diplomas(user_id):
        return Diploma.get_all_by_user_id(g, user_id)

    @ app.route("/users/<int:user_id>/diplomas/<int:diploma_id>", methods=["GET"])
    def get_user_diploma(user_id, diploma_id):
        return Diploma.get_by_id(g, diploma_id)

    @ app.route("/users/<int:user_id>/diplomas/<int:diploma_id>", methods=["PUT"])
    @ login_required
    def update_user_diploma(user_id, diploma_id):
        data = request.form

        # Check if logged-in user is correct
        if session['_user_id'] != user_id:
            return Response.unauthorized_access_wrong_user()

        if not Validator.valid_date(data["startDate"]):
            return Response.start_date_not_valid()
        if not Validator.valid_date(data["endDate"]):
            return Response.end_date_not_valid()

        if not Validator.valid_degree(data["degree"]):
            return Response.degree_not_valid()

        if not Validator.valid_discipline(data["discipline"]):
            return Response.discipline_not_valid()

        Diploma.update(g, diploma_id, data["degree"], data["discipline"],
                       data["institution"], data["startDate"], data["endDate"])
        return f"Updated diploma {diploma_id}."

    @app.route("/users/<int:user_id>/diplomas/<int:diploma_id>", methods=["DELETE"])
    @login_required
    def delete_user_diploma(user_id, diploma_id):

        # Check if logged-in user is correct
        if session['_user_id'] != user_id:
            return Response.unauthorized_access_wrong_user()

        Diploma.delete_from_user(g, user_id, diploma_id)
        return f"Deleted diploma {diploma_id} from user {user_id}."

    ########################################
    # USER ROUTES - LANGUAGES
    ########################################

    @app.route("/users/<int:user_id>/languages", methods=["POST"])
    @login_required
    def add_language_to_user(user_id):
        data = request.form

        # Check if logged-in user is correct
        if session['_user_id'] != user_id:
            return Response.unauthorized_access_wrong_user()

        if not Validator.valid_language(data["language"]):
            return Response.language_not_valid()

        Language.add_to_user(g, user_id, data["language"])
        return f"Added language {data['language']} to user {user_id}'s languages."

    @app.route("/users/<int:user_id>/languages", methods=["GET"])
    def get_all_languages_from_user(user_id):
        return Language.get_all_by_user_id(g, user_id)

    @app.route("/users/<int:user_id>/languages/<string:language>", methods=["DELETE"])
    @login_required
    def remove_language_from_user(user_id, language):

        # Check if logged-in user is correct
        if session['_user_id'] != user_id:
            return Response.unauthorized_access_wrong_user()

        Language.remove_from_user(g, user_id, language)
        return f"Removed language {language} from user {user_id}'s languages."

    ########################################
    # USER ROUTES - SKILLS
    ########################################

    @app.route("/users/<int:user_id>/skills", methods=["POST"])
    @login_required
    def add_skill_to_user(user_id):
        data = request.form

        # Check if logged-in user is correct
        if session['_user_id'] != user_id:
            return Response.unauthorized_access_wrong_user()

        if not Validator.valid_skill(data["skill"]):
            return Response.skill_not_valid()

        Skill.add_to_user(g, user_id, data["skill"])
        return f"Added skill {data['skill']} to user {user_id}'s skills."

    @app.route("/users/<int:user_id>/skills", methods=["GET"])
    def get_all_skills_from_user(user_id):
        return Skill.get_all_by_user_id(g, user_id)

    @app.route("/users/<int:user_id>/skills/<string:skill>", methods=["DELETE"])
    @login_required
    def remove_skill_from_user(user_id, skill):

        # Check if logged-in user is correct
        if session['_user_id'] != user_id:
            return Response.unauthorized_access_wrong_user()

        Skill.remove_from_user(g, user_id, skill)
        return f"Removed skill {skill} from user {user_id}'s skills."

    ########################################
    # USER ROUTES - WORK EXPERIENCE
    ########################################

    @app.route("/users/<int:user_id>/experiences", methods=["POST"])
    @login_required
    def create_user_experience(user_id):
        data = request.form
        skill_list = data["skills"].split(',')

        # Check if logged-in user is correct
        if session['_user_id'] != user_id:
            return Response.unauthorized_access_wrong_user()

        if not Validator.valid_date(data["startDate"]):
            return Response.start_date_not_valid()
        if not Validator.valid_date(data["endDate"]):
            return Response.end_date_not_valid()

        for skill in skill_list:
            if not Validator.valid_skill(skill):
                return Response.skill_not_valid()

        if not Validator.valid_profession(skill):
            return Response.profession_not_valid()

        experience_id = WorkExperience.create_for_user(g, user_id, data["jobTitle"], data["profession"],
                                                       skill_list, data["startDate"], data["endDate"])
        return f"Created experience {experience_id } for user {user_id}."

    @app.route("/users/<int:user_id>/experiences", methods=["GET"])
    def get_user_experiences(user_id):
        return WorkExperience.get_all_by_user_id(g, user_id)

    @app.route("/users/<int:user_id>/experiences/<int:experience_id>", methods=["GET"])
    def get_user_experience(user_id, experience_id):
        return WorkExperience.get_by_id(g, experience_id)

    @app.route("/users/<int:user_id>/experiences/<int:experience_id>", methods=["PUT"])
    @login_required
    def update_user_experience(user_id, experience_id):
        data = request.form
        skill_list = data["skills"].split(',')

        # Check if logged-in user is correct
        if session['_user_id'] != user_id:
            return Response.unauthorized_access_wrong_user()

        if not Validator.valid_date(data["startDate"]):
            return Response.start_date_not_valid()
        if not Validator.valid_date(data["endDate"]):
            return Response.end_date_not_valid()

        for skill in skill_list:
            if not Validator.valid_skill(skill):
                return Response.skill_not_valid()

        if not Validator.valid_profession(skill):
            return Response.profession_not_valid()

        WorkExperience.update(g, user_id, data["jobTitle"], data["profession"],
                              skill_list, data["startDate"], data["endDate"])
        return f"Updated experience {experience_id}."

    @app.route("/users/<int:user_id>/experiences/<int:experience_id>", methods=["DELETE"])
    @login_required
    def delete_user_experience(user_id, experience_id):

        # Check if logged-in user is correct
        if session['_user_id'] != user_id:
            return Response.unauthorized_access_wrong_user()

        WorkExperience.delete_from_user(g, user_id, experience_id)
        return f"Deleted experience {experience_id} from user {user_id}."

    ########################################
    # USER ROUTES - VACANCIES TOGGLE
    ########################################

    @app.route("/users/<int:user_id>/vacancies/toggle", methods=['PUT'])
    def toggle_user_vacancies(user_id):
        get_vacancies = User.toggle_get_vacancies(g, user_id)

        if (get_vacancies):
            return f"User {user_id} vacancies: enabled"
        else:
            return f"User {user_id} vacancies: disabled"

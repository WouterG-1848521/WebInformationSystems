from flask import request
from pandas import DataFrame
import json
from flask_login import login_required, logout_user
from backend_REST import session

from rdflib import Graph, URIRef, Literal, Namespace

from backend_REST.models.user import User


def create_matching_routes(app, graph):
    ########################################
    # MATCHING ROUTES - USER -> VACANCIES
    ########################################

    @app.route("/users/<int:user_id>/matches", methods=['GET'])
    def get_all_vacancy_matches_for_user(user_id):
        pass

    @app.route("/users/<int:user_id>/matches/skills", methods=['GET'])
    def get_all_vacancy_matches_for_user_by_skills(user_id):
        pass

    @app.route("/users/<int:user_id>/matches/diplomas", methods=['GET'])
    def get_all_vacancy_matches_for_user_by_diplomas(user_id):
        pass

    @app.route("/users/<int:user_id>/matches/languages", methods=['GET'])
    def get_all_vacancy_matches_for_user_by_languages(user_id):
        pass

    ########################################
    # MATCHING ROUTES - VACANCY -> USERS
    ########################################

    @app.route("/vacancies/<int:vacancy_id>/matches", methods=['GET'])
    def get_all_user_matches_for_vacancy(vacancy_id):
        pass

    @app.route("/vacancies/<int:vacancy_id>/matches/skills", methods=['GET'])
    def get_all_user_matches_for_vacancy_by_skills(vacancy_id):
        pass

    @app.route("/vacancies/<int:vacancy_id>/matches/diplomas", methods=['GET'])
    def get_all_user_matches_for_vacancy_by_diplomas(vacancy_id):
        pass

    @app.route("/vacancies/<int:vacancy_id>/matches/languages", methods=['GET'])
    def get_all_user_matches_for_vacancy_by_languages(vacancy_id):
        pass

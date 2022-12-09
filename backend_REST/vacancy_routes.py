from flask import request
from pandas import DataFrame
import json 

from backend_REST.models.vacancy import Vacancy
from backend_REST.models.enterprise import Enterprise

from flask_login import login_required, logout_user
from backend_REST import session

from .matching import matchOnVacancy_allParameters, matchOnVacancy_anyParameters, matchOnPerson



def create_vacancy_routes(app, graph):
    # add a vacancy to an enterprise
    @app.route("/enterprise/vacancy/add", methods=['POST'])
    @login_required
    def add_vacancy():
        data = request.form     # request contains : enterpriseID, mainterID (for security check), jobtitle, address, startdate, enddate
            # waarschijnlijk ook nog een lijst van skills
        
        enterprise_id = data["enterprise_id"]


        id = Vacancy.create(graph)

        print("Test Route")
        
        return f"Created vacancy {id}."

    # remove a vacancy from an enterprise
    @app.route("/enterprise/vacancy/remove", methods=['POST'])
    def remove_vacancy():
        data = request.form     # request contains : enterpriseID, vacancyID, mainterID (for security check)
        

       
        
        print(data)
        # TODO: remove in rdf 
        return ""

    def get_all_vacancies_of_enterprise(graph, enterpriseID):
        pass

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

from flask_login import login_required
from flask import request
from pandas import DataFrame
import json

from .queries import query_getVacancy, check_enterprise, check_maintainer, check_valid_vacancy, check_person, query_personByDiploma
from .queries import query_getDiplomasFromVacancy, query_getSkillsFromVacancy, query_personBySkill, query_getLanguagesFromVacancy, query_personByLanguage
from .queries import query_getExperiencesFromPerson, query_getDiplomasFromPerson, query_getSkillsFromPerson, query_getLanguagesFromPerson, query_getExperienceFromVacancy
from .queries import query_personByExperience, query_vacancyByDiploma, query_vacancyBySkill, query_vacancyByLanguage, query_vacancyByExperience

from backend_REST import session

from backend_REST.models.vacancy import Vacancy
from backend_REST.models.enterprise import Enterprise

from backend_REST.models.skill import Skill
from backend_REST.models.language import Language
from backend_REST.models.diploma import Diploma

from backend_REST.models.validator import Validator
from backend_REST.models.response import Response


def getPersonsWithDiploma(graph, diploma):
    out = {}
    query = query_personByDiploma(diploma)
    result = graph.query(query)
    df = DataFrame(result, columns=result.vars)
    for row in df.values:
        if not (row[0] == None):
            personID = row[0].n3()
            out[personID] = row
    return out


def getPersonWithSill(graph, skill):
    out = {}
    query = query_personBySkill(skill)
    result = graph.query(query)
    df = DataFrame(result, columns=result.vars)
    for row in df.values:
        if not (row[0] == None):
            personID = row[0].n3()
            out[personID] = row
    return out


def getPersonWithLanguage(graph, language):
    out = {}
    query = query_personByLanguage(language)
    result = graph.query(query)
    df = DataFrame(result, columns=result.vars)
    for row in df.values:
        if not (row[0] == None):
            personID = row[0].n3()
            out[personID] = row
    return out


def getPersonWithExperience(graph, experience):
    out = {}
    query = query_personByExperience(experience)
    result = graph.query(query)
    df = DataFrame(result, columns=result.vars)
    for row in df.values:
        if not (row[0] == None):
            personID = row[0].n3()
            out[personID] = row
    return out


def getVacanciesForDiploma(graph, diploma):
    out = []
    query = query_vacancyByDiploma(diploma)
    result = graph.query(query)
    df = DataFrame(result, columns=result.vars)
    for row in df.values:
        if not (row[0] == None):
            out.append(row[0].n3())
    return out


def getVacanciesForSkill(graph, skill):
    out = []
    query = query_vacancyBySkill(skill)
    result = graph.query(query)
    df = DataFrame(result, columns=result.vars)
    for row in df.values:
        if not (row[0] == None):
            out.append(row[0].n3())
    return out


def getVacanciesForLanguage(graph, language):
    out = []
    query = query_vacancyByLanguage(language)
    result = graph.query(query)
    df = DataFrame(result, columns=result.vars)
    for row in df.values:
        if not (row[0] == None):
            out.append(row[0].n3())
    return out


def getVacanciesForExperience(graph, experience):
    out = []
    query = query_vacancyByExperience(experience)
    result = graph.query(query)
    df = DataFrame(result, columns=result.vars)
    for row in df.values:
        if not (row[0] == None):
            out.append(row[0].n3())
    return out


def create_vacancy_routes(app, graph):
    ########################################
    # VACANCY ROUTES - BASICS
    ########################################
    @app.route("/enterprises/<int:enterprise_id>/vacancies/", methods=['POST'])
    def add_vacancy(enterprise_id):
        data = request.form

        maintainerID = data["maintainerID"]
        maintainerID = int(maintainerID)

        if not (check_maintainer(graph, maintainerID, enterprise_id)):
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

        maintainerID = data["maintainerID"]
        maintainerID = int(maintainerID)

        if not (check_maintainer(graph, maintainerID, enterprise_id)):
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

        maintainerID = data["maintainerID"]
        maintainerID = int(maintainerID)

        if not (check_maintainer(graph, maintainerID, enterprise_id)):
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

        maintainerID = data["maintainerID"]
        maintainerID = int(maintainerID)

        if not (check_maintainer(graph, maintainerID, enterprise_id)):
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

        maintainerID = data["maintainerID"]
        maintainerID = int(maintainerID)

        if not (check_maintainer(graph, maintainerID, enterprise_id)):
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

        # TODO : How are we going to do user_id here?
        # if session['_user_id'] != user_id:
        #     return Response.unauthorized_access_wrong_user()

        # maintainerID = data["maintainerID"]
        # maintainerID = int(maintainerID)

        # if not (check_maintainer(graph, maintainerID, enterprise_id)):
        #     return "only maintainer of enterprise can delete vacancy diploma"

        Diploma.delete_from_vacany(graph, vacancy_id, diploma_id)
        return f"Deleted diploma {diploma_id} from vacancy {vacancy_id}."

    ########################################
    # VACANCY ROUTES - SKILLS
    ########################################

    @app.route("/enterprises/<int:enterprise_id>/vacancies/<int:vacancy_id>/skills", methods=['POST'])
    def add_skill_to_vacancy(enterprise_id, vacancy_id):
        data = request.form

        maintainerID = data["maintainerID"]
        maintainerID = int(maintainerID)

        if not (check_maintainer(graph, maintainerID, enterprise_id)):
            return "only maintainer of enterprise can add skill to vacancy"

        # TODO: check if logged-in user is maintainer of enterprise
        # TODO: check if skill in list

        Skill.add_to_vacancy(graph, vacancy_id, data["skill"])

        return f"Added skill {data['skill']} to vacancy {vacancy_id}."

    @app.route("/enterprises/<int:enterprise_id>/vacancies/<int:vacancy_id>/skills", methods=['GET'])
    def get_all_skills_by_vacancy_id(enterprise_id, vacancy_id):

        return Skill.get_all_by_vacancy_id(graph, vacancy_id)

    @app.route("/enterprises/<int:enterprise_id>/vacancies/<int:vacancy_id>/skills/<string:skill>", methods=['DELETE'])
    def remove_skill_from_vacancy(enterprise_id, vacancy_id, skill):

        # maintainerID = data["maintainerID"]
        # maintainerID = int(maintainerID)

        # if not (check_maintainer(graph, maintainerID, enterprise_id)):
        #     return "only maintainer of enterprise can delete vacancy diploma"

        Skill.remove_from_vacancy(graph, vacancy_id, skill)

        return f"Removed skill {skill} from vacancy {vacancy_id}."

    ########################################
    # VACANCY ROUTES - LANGUAGES
    ########################################

    @app.route("/enterprises/<int:enterprise_id>/vacancies/<int:vacancy_id>/languages", methods=['POST'])
    def add_language_to_vacancy(enterprise_id, vacancy_id):
        data = request.form

        maintainerID = data["maintainerID"]
        maintainerID = int(maintainerID)

        if not (check_maintainer(graph, maintainerID, enterprise_id)):
            return "only maintainer of enterprise can delete vacancy diploma"
        # TODO: check if language in list

        Language.add_to_vacancy(graph, vacancy_id, data["language"])

        return f"Added language {data['language']} to vacancy {vacancy_id}."

    @app.route("/enterprises/<int:enterprise_id>/vacancies/<int:vacancy_id>/languages", methods=['GET'])
    def get_all_languages_by_vacancy_id(enterprise_id, vacancy_id):

        return Language.get_all_by_vacancy_id(graph, vacancy_id)

    @app.route("/enterprises/<int:enterprise_id>/vacancies/<int:vacancy_id>/languages/<string:language>", methods=['DELETE'])
    def remove_language_from_vacancy(enterprise_id, vacancy_id, language):

        # TODO: How?
        # TODO: check if logged-in user is maintainer of enterprise

        Language.remove_from_vacancy(graph, vacancy_id, language)

        return f"Removed language {language} from vacancy {vacancy_id}."

    # DONE : pass queries aan met equivalent skills
    # TODO : experience heeft ook skills, deze ook matchen met de skills? of gewoon op experience matchen
    # DONE : groepeer returned values per person/vacancy
    # DONE : add column names

    # DONE : ik check by vacancies that ze available zijn via "availability = 'true'"
    #      Dit lijkt enkel te werken als we specifieren dat het een boolean is? via local:availability "true"^^xsd:boolean
    #  -> ofwel schrijven we "true"^^xsd:boolean ofwel gewoon true (zonder quotes) en dan wordt het automatisch een boolean

    # find persons that have minimum 1 match with the given vacancy
    # TODO : vervangen door helper functies

    @app.route("/vacancy/match1", methods=['POST'])
    def match_vacancy():
        data = request.form

        if not ("vacancyID" in data):   # search people that match the given vacancy
            return "Missing vacancyID parameter", 400

        vacancyID = data["vacancyID"]
        vacancyID = int(vacancyID)

        # check if the vacancy exists
        if not check_valid_vacancy(graph, vacancyID):
            return "Vacancy not found", 404

        # TODO: equivalent dingen staan nog niet in query

        matches = {}  # we use the uri as a key and assume that it's the first value returned
        # find matches on diploma
        query = query_getDiplomasFromVacancy(vacancyID)
        result = graph.query(query)
        diplomas = [row.diploma.n3() for row in result]
        # print("diplomas: ", diplomas)
        for diploma in diplomas:
            query = query_personByDiploma(diploma)
            result = graph.query(query)
            df = DataFrame(result, columns=result.vars)
            for row in df.values:
                if not (row[0] == None):
                    personID = row[0].n3()
                    matches[personID] = row
        # print("after diploma: ", matches)

        # find matches on skills
        query = query_getSkillsFromVacancy(vacancyID)
        result = graph.query(query)
        skills = [row.skill.n3() for row in result]
        # print("skills: ", skills)
        for skill in skills:
            query = query_personBySkill(skill)
            result = graph.query(query)
            df = DataFrame(result, columns=result.vars)
            for row in df.values:
                if not (row[0] == None):
                    personID = row[0].n3()
                    matches[personID] = row
        # print("after skills: ", matches)

        # find matches on experience
        query = query_getExperienceFromVacancy(vacancyID)
        result = graph.query(query)
        experiences = [row.exp.n3() for row in result]
        # print("experiences: ", experiences)
        for experience in experiences:
            query = query_personByExperience(experience)
            result = graph.query(query)
            df = DataFrame(result, columns=result.vars)
            for row in df.values:
                if not (row[0] == None):
                    personID = row[0].n3()
                    matches[personID] = row
        # print("after experiences: ", matches)

        # find matches on languages
        query = query_getLanguagesFromVacancy(vacancyID)
        result = graph.query(query)
        languages = [row.lang.n3() for row in result]
        # print("languages: ", languages)
        for language in languages:
            query = query_personByLanguage(language)
            result = graph.query(query)
            df = DataFrame(result, columns=result.vars)
            for row in df.values:
                if not (row[0] == None):
                    personID = row[0].n3()
                    matches[personID] = row
        # print("after languages: ", matches)

        # print("matches: ", matches)

        returnString = "{"
        for key in matches:
            returnString += key + ": {"
            for val in matches[key]:
                returnString += val.n3() + ", "
            returnString += "}, "
        returnString += "}"

        # df = DataFrame.from_dict(matches, orient='index', columns=matches.keys())

        # return df.to_json(orient='index', indent=2)
        # return json.dumps(matches, indent = 4)
        return returnString

    # TODO : als hij onderweg leeg geraakt wordt hij terug opgevuld -> mag niet

    @app.route("/vacancy/matchall", methods=['POST'])
    def match_vacancyAll():
        data = request.form

        if not ("vacancyID" in data):   # search people that match the given vacancy
            return "Missing vacancyID parameter", 400

        vacancyID = data["vacancyID"]
        vacancyID = int(vacancyID)

        # check if the vacancy exists
        if not check_valid_vacancy(graph, vacancyID):
            return "Vacancy not found", 404

        # TODO: equivalent dingen staan nog niet in query

        matches = {}  # we use the uri as a key and assume that it's the first value returned
        filled = False

        # find matches on diploma
        query = query_getDiplomasFromVacancy(vacancyID)
        result = graph.query(query)
        diplomas = [row.diploma.n3() for row in result]
        # print("diplomas: ", diplomas)
        temp = matches.copy()
        for diploma in diplomas:
            result = getPersonsWithDiploma(graph, diploma)
            if (len(matches) == 0 and not filled):  # first time we just add everything
                temp = result
                filled = True
            else:
                for key in matches:
                    if not (key in result):
                        del temp[key]
            matches = temp.copy()

        # print("after diploma: ", matches)

        # find matches on skills
        query = query_getSkillsFromVacancy(vacancyID)
        result = graph.query(query)
        skills = [row.skill.n3() for row in result]
        # print("skills: ", skills)
        temp = matches.copy()
        for skill in skills:
            result = getPersonWithSill(graph, skill)
            if (len(matches) == 0 and not filled):  # first time we just add everything
                temp = result
                filled = True
            else:
                for key in matches:
                    if not (key in result):
                        del temp[key]
            matches = temp.copy()
        # print("after skills: ", matches)

        # find matches on experience
        query = query_getExperienceFromVacancy(vacancyID)
        result = graph.query(query)
        experiences = [row.exp.n3() for row in result]
        # print("experiences: ", experiences)
        temp = matches.copy()
        for experience in experiences:
            result = getPersonWithExperience(graph, experience)
            if (len(matches) == 0 and not filled):  # first time we just add everything
                temp = result
                filled = True
            else:
                for key in matches:
                    if not (key in result):
                        del temp[key]
            matches = temp.copy()
        # print("after experiences: ", matches)

        # find matches on languages
        query = query_getLanguagesFromVacancy(vacancyID)
        result = graph.query(query)
        languages = [row.lang.n3() for row in result]
        # print("languages: ", languages)
        temp = matches.copy()
        for language in languages:
            result = getPersonWithLanguage(graph, language)
            print("lang", result)
            if (len(matches) == 0 and not filled):  # first time we just add everything
                temp = result
                filled = True
            else:
                for key in matches:
                    if not (key in result):
                        del temp[key]
            matches = temp.copy()
        # print("after languages: ", matches)

        # print("matches: ", matches)

        returnString = "{"
        for key in matches:
            returnString += key + ": {"
            for val in matches[key]:
                returnString += val.n3() + ", "
            returnString += "}, "
        returnString += "}"

        # df = DataFrame.from_dict(matches, orient='index', columns=matches.keys())

        # return df.to_json(orient='index', indent=2)
        # return json.dumps(matches, indent = 4)
        return returnString

    # find vacancies for a given person that matches with any of the qualifications of the person
    @app.route("/vacancy/find", methods=['POST'])
    def find_vacancy():
        data = request.form

        if not ("personID" in data):
            return "Missing personID parameter", 400
        personID = data["personID"]
        personID = int(personID)

        if not (check_person(graph, personID)):
            return "Person not found", 404

        matches = {}  # we use the uri as a key and assume that it's the first value returned
        vacancies = []

        # find on diploma
        query = query_getDiplomasFromPerson(personID)
        result = graph.query(query)
        diplomas = [row.diploma.n3() for row in result]
        for diploma in diplomas:
            result = getVacanciesForDiploma(graph, diploma)
            for el in result:
                vacancies.append(el)
        # print("after diploma: ", vacancies)

        # find on experience
        query = query_getExperiencesFromPerson(personID)
        result = graph.query(query)
        experiences = [row.exp.n3() for row in result]
        for experience in experiences:
            result = getVacanciesForExperience(graph, experience)
            for el in result:
                vacancies.append(el)
        # print("after experience: ", vacancies)

        # find on skills
        query = query_getSkillsFromPerson(personID)
        result = graph.query(query)
        skills = [row.skill.n3() for row in result]
        for skill in skills:
            result = getVacanciesForSkill(graph, skill)
            for el in result:
                vacancies.append(el)
        # print("after skills: ", vacancies)

        # find on languages
        query = query_getLanguagesFromPerson(personID)
        result = graph.query(query)
        languages = [row.lang.n3() for row in result]
        for language in languages:
            result = getVacanciesForLanguage(graph, language)
            for el in result:
                vacancies.append(el)
        # print("after languages: ", vacancies)

        # for every vacancy get all the information
        vacancies = list(set(vacancies))
        for vacancy in vacancies:
            query = query_getVacancy(vacancy)
            result = graph.query(query)
            df = DataFrame(result, columns=result.vars)
            for i in range(len(df)):
                row = df.iloc[i]
                if not (vacancy in matches):
                    matches[vacancy] = {}
                    for j in range(len(row)):
                        key = row.keys()[j].n3()
                        matches[vacancy][key] = row.iloc[j].n3()
                else:
                    for j in range(len(row)):
                        key = df.keys()[j].n3()
                        val = row.iloc[j].n3()
                        if not (key in matches[vacancy]):
                            matches[vacancy][key] = val
                        else:
                            # check if its already in the list
                            if (not (val in matches[vacancy][key])):
                                matches[vacancy][key] += ", " + val

        # print("matches: ", matches)

        # matches = groupByVacancy(matches)
        # convert to json
        returnString = "{\n"
        for key in matches:
            returnString += key + ": {\n"
            for skey in matches[key]:
                val = matches[key][skey]
                returnString += skey + " : " + val + ",\n"
            returnString += "},\n"
        returnString += "}"

        return returnString

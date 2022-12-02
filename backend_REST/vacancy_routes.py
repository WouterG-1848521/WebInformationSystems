from flask import request
from pandas import DataFrame
import json 

from .queries import create_vacancyRDF, check_enterprise, check_maintainer, check_valid_vacancy, check_person, query_personByDiploma
from .queries import query_getDiplomasFromVacancy, query_getSkillsFromVacancy, query_personBySkill, query_getLanguagesFromVacancy, query_personByLanguage
from .queries import query_getExperiencesFromPerson, query_getDiplomasFromPerson, query_getSkillsFromPerson, query_getLanguagesFromPerson

def create_vacancy_routes(app, graph):
    # add a vacancy to an enterprise
    @app.route("/enterprise/vacancy/add", methods=['POST'])
    def add_vacancy():
        data = request.form     # request contains : enterpriseID, mainterID (for security check), jobtitle, address, startdate, enddate
        
        print(data)
        # TODO: insert in rdf 
        return "add vacancy"

    # remove a vacancy from an enterprise
    @app.route("/enterprise/vacancy/remove", methods=['POST'])
    def remove_vacancy():
        data = request.form     # request contains : enterpriseID, vacancyID, mainterID (for security check)
        print(data)
        # TODO: remove in rdf 
        return "remove vacancy"

    def get_all_vacancies_of_enterprise(graph, enterpriseID):
        pass

    # find persons that have minimum 1 match with the given vacancy
    @app.route("/vacancy/match1", methods=['POST'])
    def match_vacancy():
        data = request.form

        # TODO : add experience

        if not ("vacancyID" in data):   # search people that match the given vacancy
            return "Missing vacancyID parameter", 400
        
        vacancyID = data["vacancyID"]
        vacancyID = int(vacancyID)

        # check if the vacancy exists
        if not check_valid_vacancy(graph, vacancyID):
            return "Vacancy not found", 404

        # TODO: equivalent dingen staan nog niet in query

        matches = {} # we use the uri as a key and assume that it's the first value returned
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


    # TODO : nu wordt iedereen teruggegeven die 1 ding heeft, ma eigenlijk moet die alles hebben      

    # find vacancies for a given person
    @app.route("/vacancy/find", methods=['POST'])
    def find_vacancy():
        data = request.form

        if not ("personID" in data):
            return "Missing personID parameter", 400
        personID = data["personID"]
        personID = int(personID)

        if not (check_person(graph, personID)):
            return "Person not found", 404

        matches = {} # we use the uri as a key and assume that it's the first value returned

        # find on diploma
        query = query_getDiplomasFromPerson(personID)
        result = graph.query(query)
        diplomas = [row.diploma.n3() for row in result]
        for diploma in diplomas:
            query = query_personByDiploma(diploma)
            result = graph.query(query)
            df = DataFrame(result, columns=result.vars)
            for row in df.values:
                if not (row[0] == None):
                    personID = row[0].n3()
                    matches[personID] = row

        # find on experience

        # find on skills

        # find on languages
  
        pass


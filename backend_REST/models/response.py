from flask import make_response, jsonify, url_for, render_template, request
import json

# class RDFResponse():
#     def __init__(self, status, message, data, graph, location = None):
#         self.status = status
#         self.message = message
#         self.data = data
#         self.graph = graph
#         self.location = location

#     def get_response(self):
#         response = make_response(self.data, self.status)
#         response.headers["Content-Type"] = "application/rdf+xml"

#         if (self.location != None):
#             response.headers["Location"] = url_for(self.location)

#         return response

# class JSONResponse():
#     def __init__(self, status, message, data, location = None):
#         self.status = status
#         self.message = message
#         self.data = data
#         self.location = location


#     def get_response(self):
#         response = make_response(self.data, self.status)
#         response.headers["Content-Type"] = "application/json"

#         if (self.location != None):
#             response.headers["Location"] = url_for(self.location)

#         return response

date_formats = "Y/M/D or Y-M-D"


class Response():
    def unauthorized_access_not_logged_in():
        return make_response(jsonify({"message": "Unauthorized Access (Need to login first)"}), 401)

    def unauthorized_access_wrong_user():
        return make_response(jsonify({"message": "Unauthorized Access (Wrong user)"}), 401)

    def start_date_not_valid():
        return make_response(jsonify({"message": f"Start date not valid. (Formats: {date_formats})"}), 400)

    def end_date_not_valid():
        return make_response(jsonify({"message": f"End date not valid. (Formats: {date_formats})"}), 400)

    def email_not_valid():
        return make_response(jsonify({"message": "Email not valid."}), 400)

    def email_not_available():
        return make_response(jsonify({"message": "Email not available."}), 400)

    def degree_not_valid():
        return make_response(jsonify({"message": "Degree not valid."}), 400)

    def discipline_not_valid():
        return make_response(jsonify({"message": "Discipline not valid."}), 400)

    def skill_not_valid():
        return make_response(jsonify({"message": "Skill not valid."}), 400)

    def language_not_valid():
        return make_response(jsonify({"message": "Language not valid."}), 400)

    def profession_not_valid():
        return make_response(jsonify({"message": "Profession not valid."}), 400)

    def user_not_exist():
        return make_response(jsonify({"message": "User does not exist."}), 400)

    def password_not_matching():
        return make_response(jsonify({"message": "Passwords don't match"}), 400)

    @staticmethod
    def make_response_for_content_type(accept_headers, message="", template="index.html", status="success", code=200):
        if ('text/html' in accept_headers):
            return make_response(render_template(template, message=message, status=status), code)
        elif ('application/json' in accept_headers):
            return make_response(jsonify({"message": message}), code)
        else:
            return make_response(render_template("415.html"), 415), 415

            # Default to HTML
            # return make_response(render_template(template, message=message, status=status), code)
    
    @staticmethod
    def make_response_for_content_type_and_data(accept_headers, data, template="index.html", status="success", code=200):
        if ('text/html' in accept_headers):
            return make_response(render_template(template, status=status, data=data), code)
        elif ('application/json' in accept_headers):
            return make_response(jsonify(data), code)
        else:
            return make_response(render_template("415.html"), 415), 415

            # Default to HTML
            # return make_response(render_template(template, status=status, data=data), code)
    
    # p, name, surname, diploma, experience, getVacancies, language, skill
    @staticmethod
    def format_users_json(usersJSON):
        # Format dictionary correctly for response so that each key is a user_id 
        # and the value is the user data
        newDict = {'users': {}}
        for id in usersJSON['p']:
            info = {
                "p": usersJSON['p'][id],
                "name": usersJSON['name'][id],
                "surname": usersJSON['surname'][id],
                "getVacancies": usersJSON['getVacancies'][id]                
            }
            newDict['users'][int(id)] = info
            print(newDict)
        
        return newDict
    
    # d, degree, discipline, institution, startDate, endDate
    @staticmethod
    def format_diplomas_json(diplomasJSON):
        # Format dictionary correctly for response so that each key is a diploma_id 
        # and the value is the diploma data
        newDict = {'diplomas': {}}
        for id in diplomasJSON['d']:
            info = {
                "d": diplomasJSON['d'][id],
                "degree": diplomasJSON['degree'][id],
                "discipline": diplomasJSON['discipline'][id],
                "institution": diplomasJSON['institution'][id],
                "startDate": diplomasJSON['startDate'][id],
                "endDate": diplomasJSON['endDate'][id],
            }
            newDict['diplomas'][int(id)] = info
            print(newDict)
        
        return newDict
    
    # e, jobTitle, profession, skill, startDate, endDate
    @staticmethod
    def format_experiences_json(experiencesJSON):
        # Format dictionary correctly for response so that each key is a experience_id 
        # and the value is the experience data
        newDict = {'experiences': {}}
        for id in experiencesJSON['e']:
            info = {
                "e": experiencesJSON['e'][id],
                "jobTitle": experiencesJSON['jobTitle'][id],
                "profession": experiencesJSON['profession'][id],
                "skill": experiencesJSON['skill'][id],
                "startDate": experiencesJSON['startDate'][id],
                "endDate": experiencesJSON['endDate'][id],
            }
            newDict['experiences'][int(id)] = info
            print(newDict)
        
        return newDict
    
    # skill
    @staticmethod
    def format_skills_json(skillsJSON):
        # Format dictionary correctly for response so that each key is a experience_id 
        # and the value is the experience data
        newDict = {'skills': {}}
        for id in skillsJSON['skill']:
            newDict['skills'][int(id)] = skillsJSON['skill'][id],
        
        return newDict
    
    # language
    @staticmethod
    def format_languages_json(languagesJSON):
        # Format dictionary correctly for response so that each key is a experience_id 
        # and the value is the experience data
        newDict = {'languages': {}}
        for id in languagesJSON['language']:
            newDict['languages'][int(id)] = languagesJSON['language'][id],
        
        return newDict
    
    # v, maintainerId, jobTitle, startDate, endDate, location
    @staticmethod
    def format_vacancies_json(vacanciesJSON):
        # Format dictionary correctly for response so that each key is a experience_id 
        # and the value is the experience data
        print(vacanciesJSON)
        newDict = {'vacancies': {}}
        for id in vacanciesJSON['v']:
            info = {
                "v": vacanciesJSON['v'][id],
                "maintainerId": vacanciesJSON['maintainerId'][id],
                "jobTitle": vacanciesJSON['jobTitle'][id],
                "location": vacanciesJSON['location'][id],
                "startDate": vacanciesJSON['startDate'][id],
                "endDate": vacanciesJSON['endDate'][id],
            }
            newDict['vacancies'][int(id)] = info
            print(newDict)
        
        return newDict
    
    
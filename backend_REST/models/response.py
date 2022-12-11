from flask import make_response, jsonify, url_for
import flask_rdf

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

# class JsonResponse():
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
        return make_response(jsonify({"message": "User not exist."}), 400)

    def password_not_matching():
        return make_response(jsonify({"message": "Passwords don't match"}), 400)

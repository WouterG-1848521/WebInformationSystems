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
            # Default to HTML
            return make_response(render_template(template, message=message, status=status), code)
    
    @staticmethod
    def make_response_for_content_type_and_data(accept_headers, data, template="index.html", status="success", code=200):
        if ('text/html' in accept_headers):
            return make_response(render_template(template, status=status, data=data), code)
        elif ('application/json' in accept_headers):
            return make_response(jsonify(data), code)
        else:
            # Default to HTML
            return make_response(render_template(template, status=status, data=data), code)
    
    @staticmethod
    def format_users_json(usersJson):
        # Format dictionary correctly for response so that each key is a user_id 
        # and the value is the user data
        newDict = {}
        for id in usersJson['p']:
            info = {
                "p": usersJson['p'][id],
                "name": usersJson['name'][id],
                "surname": usersJson['surname'][id],
            }
            newDict[id] = info
            print(newDict)
        
        return newDict
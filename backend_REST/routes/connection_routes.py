from flask import request, make_response, jsonify
from pandas import DataFrame
import json
from flask_login import login_required, logout_user
from backend_REST import session


from backend_REST.models.connection import Connection
from backend_REST.models.user import User

from backend_REST.models.validator import Validator
from backend_REST.models.response import Response


def create_connections_routes(app, graph):

    @app.route("/connections/send", methods=['POST'])
    @login_required
    def send_connection_request():

        data = request.form

        fromUserId = data["fromUserId"]
        if (type(data["fromUserId"]) != int):
            fromUserId= int(data["fromUserId"])
        if session['_user_id'] != fromUserId:
            return Response.unauthorized_access_wrong_user()

        if not User.exists(data["toUserId"]):
            return Response.user_not_exist()

        request_id = Connection.send_request(
            data["fromUserId"], data["toUserId"])

        responseMessage = f"Connection request send. ({data['fromUserId']} -> {data['toUserId']})"
        if (request_id != -1):  

            return make_response(jsonify({"request_id": request_id, "message": responseMessage}), 200)
        else:
            return make_response(jsonify({"message": "Connection request already sent."}), 200)

    @app.route("/connections/cancel/<int:request_id>", methods=['DELETE'])
    @login_required
    def cancel_connection_request(request_id):

        request = Connection.get_by_id(request_id)

        if not request:
            return Response.unauthorized_access_wrong_user()

        if (request.fromUser != session['_user_id']):
            return Response.unauthorized_access_wrong_user()

        Connection.cancel_request(request_id)

        return make_response(jsonify({"message": jsonify(f"Connection request {request_id} canceled.")}), 200)

    @app.route("/connections/accept", methods=['POST'])
    @login_required
    def accept_connection_request():
        data = request.form

        request2 = Connection.get_by_id(data['request_id'])
        print(request2)

        if not request2:
            return Response.unauthorized_access_wrong_user()

        if (request2.toUser != session['_user_id']):
            return Response.unauthorized_access_wrong_user()

        Connection.accept_request(data["request_id"])

        return make_response(jsonify({"message": f"Connection request {data['request_id']} accepted."}), 200)
        return make_response(jsonify({"message": jsonify(f"Connection request {data['request_id']} accepted.")}), 200)

    @app.route("/connections/deny", methods=['POST'])
    @login_required
    def deny_connection_request():
        data = request.form

        request = Connection.get_by_id(data['request_id'])

        if not request:
            return Response.unauthorized_access_wrong_user()

        if (request.toUser != session['_user_id']):
            return Response.unauthorized_access_wrong_user()

        Connection.deny_request(data['request_id'])

        return make_response(jsonify({"message": jsonify(f"Connection request {data['request_id']} denied.")}), 200)

    @app.route("/connections/pending/<int:user_id>", methods=['GET'])
    @login_required
    def get_pending_connection_requests(user_id):

        if (user_id != session['_user_id']):
            return Response.unauthorized_access_wrong_user()

        pending_requests = Connection.get_pending_requests_by_user(user_id)
        
        return make_response(jsonify(pending_requests), 200)
        # return make_response(json.dump(pending_requests), 200)

    @app.route("/connections/add", methods=['POST'])
    @login_required
    def add_connection():
        data = request.form

        if not User.is_admin(session['_user_id']):
            return Response.unauthorized_access_wrong_user()

        Connection.add_to_user(graph, data["user1_id"], data["user2_id"])

        return Response.make_response_for_content_type('application/json', f"Created connection between {data['user1_id']} and {data['user2_id']}.", 200)

    @app.route("/connections/<int:user_id>", methods=['GET'])
    def get_connections_by_id(user_id):

        return Connection.get_all_by_user_id(graph, user_id)

    @app.route("/connections/delete", methods=['DELETE'])
    @login_required
    def delete_connection():
        data = request.form

        if (data["user1_id"] != session['_user_id']):
            return Response.unauthorized_access_wrong_user()

        Connection.remove_from_user(graph, data["user1_id"], data["user2_id"])

        return Response.make_response_for_content_type('application/json', f"Removed connection between {data['user1_id']} and {data['user2_id']}.", 200)

from flask import request
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

        if session['_user_id'] != data["fromUserId"]:
            return Response.unauthorized_access_wrong_user()

        if not User.exists(data["toUserId"]):
            return Response.user_not_exist()

        request_id = Connection.send_request(
            data["fromUserId"], data["toUserId"])

        if (request_id != -1):
            return f"Connection request {request_id} send. ({data['fromUserId']} -> {data['toUserId']})"
        else:
            return f"Connection request already send."

    @app.route("/connections/cancel/<int:request_id>", methods=['DELETE'])
    @login_required
    def cancel_connection_request(request_id):

        request = Connection.get_by_id(request_id)

        if not request:
            return Response.unauthorized_access_wrong_user()

        if (request.fromUser != session['_user_id']):
            return Response.unauthorized_access_wrong_user()

        Connection.cancel_request(request_id)

        return f"Connection request {request_id} canceled."

    @app.route("/connections/accept", methods=['POST'])
    @login_required
    def accept_connection_request():
        data = request.form

        request = Connection.get_by_id(data['request_id'])

        if not request:
            return Response.unauthorized_access_wrong_user()

        if (request.toUser != session['_user_id']):
            return Response.unauthorized_access_wrong_user()

        Connection.accept_request(data["request_id"])

        return f"Connection request {data['request_id']} accepted."

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

        return f"Connection request {data['request_id']} denied."

    @app.route("/connections/pending/<int:user_id>", methods=['GET'])
    @login_required
    def get_pending_connection_requests(user_id):

        if (user_id != session['_user_id']):
            return Response.unauthorized_access_wrong_user()

        return Connection.get_pending_requests_by_user(user_id)

    @app.route("/connections/add", methods=['POST'])
    @login_required
    def add_connection():
        data = request.form

        if not User.is_admin(session['_user_id']):
            return Response.unauthorized_access_wrong_user()

        Connection.add_to_user(graph, data["user1_id"], data["user2_id"])

        return f"Created connection between {data['user1_id']} and {data['user2_id']}."

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

        return f"Removed connection between {data['user1_id']} and {data['user2_id']}."

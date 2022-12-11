from flask import request, render_template, redirect, url_for, make_response, jsonify
from flask import Response as FlaskResponse
from flask_login import login_user, logout_user, login_required, current_user
import hashlib
import json

from backend_REST import db, session
from backend_REST.models.database import DBUser
from backend_REST.models.response import Response

from backend_REST.models.user import User


def create_login_routes(app, g):
    @app.route("/login", methods=['POST'])
    def db_login():
        data = request.form
        accept_headers = request.headers.get("Accept", "text/html")

        if (current_user.is_authenticated):
            Response.make_response_for_content_type(accept_headers, "Already logged in.")

        # Encryption must be done before send with HTTP POST, but currently no front-end
        encrypted_password = hashlib.sha256(
            data["password"].encode('utf-8')).hexdigest()

        app.logger.info("Logging in...")
        user = DBUser.query.filter_by(
            email=data['email'], password=encrypted_password).first()

        if (user == None):
            return Response.make_response_for_content_type(accept_headers, "Email or password is incorrect.")

        login_user(user)

        user = json.loads(User.get_by_id(g, current_user.id))
        data = Response.format_users_json(user)

        return Response.make_response_for_content_type_and_data(accept_headers, data)

    @app.route("/logout", methods=['GET'])
    @login_required
    def db_logout():
        app.logger.info("Logging out...")
        logout_user()

        accept_headers = request.headers.get("Accept", "text/html")
        return Response.make_response_for_content_type(accept_headers, "Logged out.")

        # return render_template("index.html", message="Logged out.", status="success")

    # @app.route("/sign-up", methods=['POST'])
    # def db_sign_up():
    #     data = request.form
    #     accept_headers = request.headers.get("Accept", "text/html")

    #     # Check if email is already in use
    #     if (DBUser.query.filter_by(email=data['email']).first() != None):
    #         return Response.make_response_for_content_type(accept_headers, "Email is already in use.")

    #     if (current_user.is_authenticated):
    #         return Response.make_response_for_content_type(accept_headers, "Already logged in.")

    #     # Encryption must be done before send with HTTP POST, but currently no front-end
    #     encrypted_password = hashlib.sha256(
    #         data["password"].encode('utf-8')).hexdigest()

    #     app.logger.info("Signing up...")
    #     user = DBUser(email=data['email'], password=encrypted_password)

    #     db.session.add(user)
    #     db.session.commit()

    #     # login_user(user)

    #     userJson = jsonify({
    #         "id": user.id,
    #         "email": user.email,
    #         "password": user.password
    #     })
        
    #     return Response.make_response_for_content_type_and_data(accept_headers, userJson)
from flask import request, render_template, redirect, url_for, make_response, jsonify
from flask import Response as FlaskResponse
from flask_login import login_user, logout_user, login_required, current_user
import hashlib
import json

from backend_REST import db, session
from backend_REST.models.database import DBUser
from backend_REST.models.response import Response


def create_login_routes(app):
    @app.route("/login", methods=['POST'])
    def db_login():
        data = request.form

        if (current_user.is_authenticated):
            return make_response(jsonify({"message": "Already logged in."}), 200)

        # Encryption must be done before send with HTTP POST, but currently no front-end
        encrypted_password = hashlib.sha256(
            data["password"].encode('utf-8')).hexdigest()

        app.logger.info("Logging in...")
        user = DBUser.query.filter_by(
            email=data['email'], password=encrypted_password).first()

        # TODO: check email and password
        if (user == None):
            return "Email and/or password are wrong."

        login_user(user)

        userJson = jsonify({
            "id": user.id,
            "email": user.email,
            "password": user.password
        })

        return make_response(userJson, 200)

    @app.route("/logout", methods=['GET'])
    @login_required
    def db_logout():
        app.logger.info("Logging out...")
        logout_user()

        return make_response(jsonify({"message": "Logged out."}), 200)
        # return render_template("index.html", message="Logged out.", status="success")

    @app.route("/sign-up", methods=['POST'])
    def db_sign_up():
        data = request.form

        # Check if email is already in use
        if (DBUser.query.filter_by(email=data['email']).first() != None):
            return make_response(jsonify({"message": "Email is already in use."}), 200)

        if (current_user.is_authenticated):
            return make_response(jsonify({"message": "Already logged in."}), 200)

        # Encryption must be done before send with HTTP POST, but currently no front-end
        encrypted_password = hashlib.sha256(
            data["password"].encode('utf-8')).hexdigest()

        app.logger.info("Signing up...")
        user = DBUser(email=data['email'], password=encrypted_password)

        db.session.add(user)
        db.session.commit()

        # login_user(user)

        userJson = jsonify({
            "id": user.id,
            "email": user.email,
            "password": user.password
        })
        
        return make_response(userJson, 200)
        # return render_template("index.html", message="Signed up.", status="success")
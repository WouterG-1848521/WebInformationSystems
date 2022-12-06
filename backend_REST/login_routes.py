from flask import request
from flask_login import login_user, logout_user, login_required

from backend_REST import db, session
from backend_REST.models.database import DBUser


def create_login_routes(app):

    @app.route("/login", methods=['POST'])
    def db_login():
        data = request.form

        app.logger.info("Logging in...")
        user = DBUser.query.filter_by(
            email=data['email'], password=data['password']).first()

        # TODO: check email and password
        if (user == None):
            return "Email and/or password are wrong."

        login_user(user)

        return "Logged in."

    @app.route("/logout", methods=['GET'])
    @login_required
    def db_logout():
        app.logger.info("Logging out...")
        logout_user()

        return "Logged out."

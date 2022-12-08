from flask import request, render_template
from flask_login import login_user, logout_user, login_required
import hashlib

from backend_REST import db, session
from backend_REST.models.database import DBUser


def create_login_routes(app):
    @app.route("/index", methods=['GET'])
    @app.route("/", methods=['GET'])
    def home():
        return render_template("index.html")


    @app.route("/login", methods=['POST'])
    def db_login():
        data = request.form

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

        return render_template("index.html", message="Logged in.", status="success", user=user)

    @app.route("/logout", methods=['GET'])
    @login_required
    def db_logout():
        app.logger.info("Logging out...")
        logout_user()

        return render_template("index.html", message="Logged out.", status="success")

    @app.route("/sign-up", methods=['POST'])
    def db_sign_up():
        data = request.form

        # Encryption must be done before send with HTTP POST, but currently no front-end
        encrypted_password = hashlib.sha256(
            data["password"].encode('utf-8')).hexdigest()

        app.logger.info("Signing up...")
        user = DBUser(email=data['email'], password=encrypted_password)

        db.session.add(user)
        db.session.commit()

        login_user(user)

        return render_template("index.html", message="Signed up.", status="success", user=user)

    @app.route("/sign-up", methods=['GET'])
    def sign_up_form():
        return render_template("sign_up_form.html")
    

    @app.route("/login", methods=['GET'])
    def login_form():
        return render_template("login_form.html")
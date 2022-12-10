
from flask import request, render_template, redirect, url_for, make_response, jsonify
from flask_login import login_user, logout_user, login_required, current_user
import hashlib

from backend_REST import db, session
from backend_REST.models.database import DBUser
from backend_REST.routes import connection_routes, matching_routes, user_routes, enterprise_routes, vacancy_routes, login_routes, test_routes
from backend_REST.models.response import Response

def create_frontend_routes(app, graph):

    ########################################
    # Index
    ########################################
    @app.route("/index", methods=['GET'])
    @app.route("/", methods=['GET'])
    def home():
        return render_template("index.html")

    # ########################################
    # # Authentication / Sign up
    # ########################################
    # @app.route("/login/save", methods=['POST'])
    # def login_save():
    #     data = request.form

    #     # Use API login routes
    #     response = login_routes.db_login()


    #     return render_template("index.html", message="Logged in.", status="success")


    @app.route("/sign-up", methods=['GET'])
    def sign_up_form():
        if (current_user.is_authenticated):
            return render_template("index.html")

        return render_template("sign_up_form.html")
    
    @app.route("/login", methods=['GET'])
    def login_form():
        # Check if user is logged in
        if (current_user.is_authenticated):
            return redirect("/index")

        return render_template("login_form.html")

    ########################################
    # User profiles
    ########################################
    
    # @app.route("/users/<int:user_id>/profile/show", methods=["GET"])
    # @login_required
    # def show_profile_create_form(user_id):
    #     return render_template("profile_create.html", user_id=user_id)
   
   
    ########################################
    # Error Handling
    ########################################
    
    @app.errorhandler(404)
    def not_found(request):
        """Page not found."""
        return make_response(jsonify({"error": "Page not found."}), 404)

    @app.errorhandler(400)
    def bad_request(request):
        """Bad request."""
        return make_response(jsonify({"error": "Bad request."}), 400)

    @app.errorhandler(500)
    def server_error(request):
        """Internal server error."""
        return make_response(jsonify({"error": "Internal server error."}), 500)
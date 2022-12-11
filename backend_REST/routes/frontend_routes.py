
from flask import request, render_template, redirect, url_for, make_response, jsonify
from flask_login import login_user, logout_user, login_required, current_user
import hashlib
import json

from backend_REST import db, session
from backend_REST.models.database import DBUser
from backend_REST.routes import connection_routes, matching_routes, user_routes, enterprise_routes, vacancy_routes, login_routes, test_routes
from backend_REST.models.response import Response
from backend_REST.models.user import User

def create_frontend_routes(app, g):

    ########################################
    # Index
    ########################################
    @app.route("/index", methods=['GET'])
    @app.route("/", methods=['GET'])
    def home():
        if current_user.is_authenticated:
            # Get the user's profile
            user = json.loads(User.get_by_id(g, current_user.id))
            data = Response.format_users_json(user)
            # # Get the user's matches
            # matches = matching_routes.get_matches(current_user.id)
            # # Get the user's enterprises
            # enterprises = enterprise_routes.get_enterprises(current_user.id)
            # # Get the user's vacancies
            # vacancies = vacancy_routes.get_vacancies(current_user.id)
            # # Get the user's recommendations
            # recommendations = matching_routes.get_recommendations(current_user.id)

        else:
            data = None

        accept_headers = request.headers.get("Accept", "text/html")
        return Response.make_response_for_content_type_and_data(accept_headers, data)

    # ########################################
    # # Authentication / Sign up
    # ########################################
    # These routes have content negotiation to support both HTML and JSON

    @app.route("/sign-up", methods=['GET'])
    def sign_up_form():
        # Check the Accept header
        content_type = request.headers.get("Accept", "text/html")
        if (content_type == "application/json"):
            return make_response(jsonify({"message": f"Please use the HTML form to sign up or send a POST request to {url_for('sign-up')}."}), 200)
        elif (content_type == "text/html"):
            return make_response(render_template("sign_up_form.html"), 200)
        else:
            return make_response(render_template("sign_up_form.html"), 200)
    
    @app.route("/login", methods=['GET'])
    def login_form():
        # Check the Accept header
        content_type = request.headers.get("Accept", "text/html")

        if (content_type == "application/json"):
            return make_response(jsonify({"message": f"Please use the HTML form to login or send a POST request to {url_for('login')}."}), 200)
        elif (content_type == "text/html"):
            return make_response(render_template("login_form.html"), 200)
        else:
            return make_response(render_template("login_form.html"), 200)

    ########################################
    # User profiles
    ########################################
    
    # @app.route("/users/<int:user_id>/profile/show", methods=["GET"])
    # @login_required
    # def show_profile_create_form(user_id):
    #     return render_template("profile_create.html", user_id=user_id)
    @app.route("/users/<int:user_id>", methods=["GET"])
    @login_required
    def update_user_form(user_id):
        # Check the Accept header
        content_type = request.headers.get("Accept", "text/html")

        if (content_type == "application/json"):
            return make_response(jsonify({"message": f"Please use the HTML form to update the user or send a POST request to {url_for('update_user')}."}), 200)
        elif (content_type == "text/html"):
            return make_response(render_template("update_user.html"), 200)
        else:
            return make_response(render_template("update_user.html"), 200)
   
    ########################################
    # Error Handling
    ########################################
    
    @app.errorhandler(404)
    def not_found(request):
        """Page not found."""
        return render_template("404.html"), 404
        return make_response(jsonify({"error": "Page not found."}), 404)

    @app.errorhandler(400)
    def bad_request(request):
        """Bad request."""
        return render_template("400.html"), 400
        return make_response(jsonify({"error": "Bad request."}), 400)

    @app.errorhandler(500)
    def server_error(request):
        """Internal server error."""
        return render_template("500.html"), 500
        return make_response(jsonify({"error": "Internal server error."}), 500)


    @app.errorhandler(415)
    def unsupported_media_type(request):
        """Unsupported media type."""
        return render_template("415.html"), 415
        return make_response(jsonify({"error": "Unsupported media type."}), 415)

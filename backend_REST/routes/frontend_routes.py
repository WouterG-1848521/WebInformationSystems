
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
        # Check the Content-Type header
        content_type = request.headers.get("Content-Type", "text/html")
        if (content_type == "application/json"):
            return make_response(jsonify({"message": f"Welcome!"}), 200)
        elif (content_type == "text/html"):
            return make_response(render_template("index.html"), 200)
        else:
            return make_response(jsonify({"error": "Unsupported Content-Type."}), 400)

    # ########################################
    # # Authentication / Sign up
    # ########################################
    # These routes have content negotiation to support both HTML and JSON

    @app.route("/sign-up", methods=['GET'])
    def sign_up_form():
        # Check the Content-Type header
        content_type = request.headers.get("Content-Type", "text/html")
        if (content_type == "application/json"):
            return make_response(jsonify({"message": f"Please use the HTML form to sign up or send a POST request to {url_for('sign_up_form')}."}), 200)
        elif (content_type == "text/html"):
            return make_response(render_template("sign_up_form.html"), 200)
        else:
            return make_response(jsonify({"message": f"Please use the HTML form to sign up or send a POST request to {url_for('sign_up_form')}."}), 200)
    
    @app.route("/login", methods=['GET'])
    def login_form():
        # Check the Content-Type header
        content_type = request.headers.get("Content-Type", "text/html")

        if (content_type == "application/json"):
            return make_response(jsonify({"message": f"Please use the HTML form to login or send a POST request to {url_for('login_form')}."}), 200)
        elif (content_type == "text/html"):
            return make_response(render_template("login_form.html"), 200)
        else:
            return make_response(jsonify({"message": f"Please use the HTML form to login or send a POST request to {url_for('login_form')}."}), 200)

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
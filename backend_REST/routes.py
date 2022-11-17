from flask import jsonify
# from markupsafe import escape

def create_routes(app):
    users = {}
    # Connect to database and make queries to users table
    # TO DO

    ########################################
    # USER ROUTES
    ########################################
    @app.route("/")
    def get_users():
        return "Hello World!"

    @app.route("/users", methods=["GET"])
    def get_users():
        return jsonify(users)
    
    @app.route("/users", methods=["POST"])
    def create_user():
        # TO DO: Create user in database

        return jsonify(users)
    
    @app.route("/users/<int:id>", methods=["GET"])
    def get_user(id):
        return jsonify(users[id])

    @app.route("/users/<int:id>", methods=["PUT"])
    def update_user(id):
        # TO DO: Update user in database

        return jsonify(users[id])
    
    @app.route("/users/<int:id>", methods=["DELETE"])
    def delete_user(id):
        # TO DO: Delete user in database

        return "User with id {id} deleted"
    
    @app.route("/users/<int:id>/profile", methods=["GET"])
    def get_user_profile(id):
        # TODO: get user profile
        return "No user profile made yet"
    
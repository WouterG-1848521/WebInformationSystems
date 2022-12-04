from flask import request
from pandas import DataFrame
import json 

from backend_REST.models.connection import Connection

def create_connections_routes(app, graph):
    # add a vacancy to an enterprise
    @app.route("/connection/add", methods=['POST'])
    def add_connection():
        data = request.form    
        
        Connection.add_to_user(graph, data["user1_id"], data["user2_id"])
        
        return f"Created connection between {data['user1_id']} and {data['user2_id']}."

    @app.route("/connection/<int:user_id>", methods=['GET'])
    def get_connections_by_id(user_id):
        
        return Connection.get_all_by_user_id(graph, user_id)


    @app.route("/connection/delete", methods=['DELETE'])
    def delete_connection():
        data = request.form

        Connection.remove_from_user(graph, data["user1_id"], data["user2_id"])

        return f"Removed connection between {data['user1_id']} and {data['user2_id']}."
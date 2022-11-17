from flask import jsonify
# from markupsafe import escape
from rdflib.plugins.sparql.results.jsonresults import *
from pandas import DataFrame



def create_routes(app, g):
    



    # Connect to database and make queries to users table
    # TO DO

    ########################################
    # USER ROUTES
    ########################################
    @app.route("/users", methods=["GET"])
    def get_users():

        q = '''
                PREFIX foaf: <http://xmlns.com/foaf/0.1/>

                SELECT ?p
                WHERE {
                    ?p rdf:type foaf:Person .
                }
            '''
        
        result = g.query(q)
        df = DataFrame(result, columns=result.vars)
        return df.to_json()
    
    @app.route("/users", methods=["POST"])
    def create_user():
        # TO DO: Create user in database

        return jsonify(users)
    
    @app.route("/users/<int:id>", methods=["GET"])
    def get_user(id):
        q = '''
                PREFIX foaf: <http://xmlns.com/foaf/0.1/>
                SELECT ?p
                WHERE {
                    ?p rdf:type foaf:Person .
                    ?p <http://localhost/hasId> %d .
                }
            ''' % (id)
        # q.format(id)
        
        result = g.query(q)
        df = DataFrame(result, columns=result.vars)
        return df.to_json()



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
    
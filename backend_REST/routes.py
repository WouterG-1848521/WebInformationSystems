from flask import jsonify
# from markupsafe import escape
from rdflib.plugins.sparql.results.jsonresults import *
from pandas import DataFrame
from backend_REST.enterprise_routes import create_enterprise_routes
from backend_REST.test_routes import create_test_routes
from flask import request

def create_routes(app, g):
    
    # Connect to database and make queries to users table
    # TO DO

    create_test_routes(app)
    create_enterprise_routes(app)

    ########################################
    # USER ROUTES
    ########################################
    @app.route("/users", methods=["GET"])
    def get_users():
        
        q = f'''
                PREFIX foaf: <http://xmlns.com/foaf/0.1/>

                SELECT ?p
                WHERE {{
                    ?p rdf:type foaf:Person .
                }}
            '''
        
        result = g.query(q)
        df = DataFrame(result, columns=result.vars)
        return df.to_json(orient="records")

        
   
    @app.route("/users", methods=["POST"])
    def set_users():
        # data contains
        # id
        # name
        # email
        # pw?
        # type
        # information
        data = request.args

        g.add(())
        g.serialize(destination="test.ttl")

        print(data)

            

        return "lol"
    
    @app.route("/users/<int:id>", methods=["GET"])
    def get_user(id):
        q = f'''
                PREFIX foaf: <http://xmlns.com/foaf/0.1/>
                SELECT ?p
                WHERE {{
                    ?p rdf:type foaf:Person .
                    ?p <http://localhost/hasId> {id} .
                }}
            '''
        # q.format(id)
        
        result = g.query(q)
        df = DataFrame(result, columns=result.vars)
        return df.to_json()



    @app.route("/users/<int:id>", methods=["PUT"])
    def update_user(id):
       
        

        return jsonify(users[id])
    
    @app.route("/users/<int:id>", methods=["DELETE"])
    def delete_user(id):

        q = f"""
        PREFIX foaf: <http://xmlns.com/foaf/0.1/>
        DELETE {{ 
            ?p <http://localhost/hasId> {id} .
            ?p <http://localhost/hasSurName> ?s .
            ?p a foaf:Person ;
            
        }}
        WHERE {{ 
            ?p <http://localhost/hasId> {id} .
            ?p a <http://xmlns.com/foaf/0.1/Person> .
         }}
        
        """

        g.update(q)
        g.serialize(destination="test.ttl")

        return f"User with id {id} deleted"
    
    @app.route("/users/<int:id>/profile", methods=["GET"])
    def get_user_profile(id):
        
        q = f"""
                
                PREFIX foaf: <http://xmlns.com/foaf/0.1/>
                SELECT ?p ?surName ?email
                WHERE {{
                    ?p rdf:type foaf:Person .
                    ?p <http://localhost/hasId> {id} .
                    OPTIONAL {{ ?p <http://localhost/hasSurName> ?surName . }}
                    OPTIONAL {{ ?p <http://localhost/hasEmail> ?email . }}    
                }}
            """
        
        result = g.query(q)
        df = DataFrame(result, columns=result.vars)
        return df.to_json(orient="records")

        
    
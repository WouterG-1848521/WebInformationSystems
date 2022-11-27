from flask import jsonify
# from markupsafe import escape
from rdflib.plugins.sparql.results.jsonresults import *
from pandas import DataFrame
import owlrl

from flask import request

from backend_REST.models import User

from backend_REST.enterprise_routes import create_enterprise_routes
from backend_REST.test_routes import create_test_routes


"""Reasoning stuff"""
def run_inferences( g ):
    #print('run_inferences')
    # expand deductive closure
    owlrl.DeductiveClosure(owlrl.OWLRL_Semantics).expand(g)
    owlrl.DeductiveClosure(owlrl.RDFS_Semantics).expand(g)
    # n_triples(g)
    return g

def create_routes(app, g):
    
    # Connect to database and make queries to users table
    # TO DO

    create_test_routes(app)
    create_enterprise_routes(app, g)

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
    def create_users():
        data = request.form     # request contains : name, surname, email, (encrypted) password (, type, information)

        if (User.is_user_available(data["email"])): 
            user_id = User.create(g, data["name"], data["surname"], data["email"], data["password"])            
            return "Created user " + str(user_id) + "."
        else:
            return "Email already in use."
        
    
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

    @app.route("/test", methods=["GET"])
    def test():

        query = """
            SELECT ?userInfo
            where {
                ?userInfo a <http://localhost/UserInfo> .
                ?userInfo <http://localhost/hasDiploma> ?diploma .
                ?diploma <http://localhost/degreeField> <http://localhost/field/Doctor> .

            }
        """

        # owlrl.DeductiveClosure(owlrl.OWLRL_Semantics).expand(g)
        owlrl.DeductiveClosure(owlrl.RDFS_Semantics).expand(g)

        g.serialize(destination="out.ttl")

        result = g.query(query)

        df = DataFrame(result, columns=result.vars)
        return df.to_json(orient="records")

        
    
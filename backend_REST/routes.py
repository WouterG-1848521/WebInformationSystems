from flask import jsonify
# from markupsafe import escape
from rdflib.plugins.sparql.results.jsonresults import *
from pandas import DataFrame
import owlrl

from flask import request

from backend_REST.models import User, Diploma, Skills, Language

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

    create_test_routes(app, g)
    create_enterprise_routes(app, g)

    ########################################
    # USER ROUTES
    ########################################
    @app.route("/users", methods=["GET"])
    def get_all_users():
        return User.get_all(g)

 
    @app.route("/users", methods=["POST"])
    def create_user():
        data = request.form     # request contains : name, surname, email, (encrypted) password (, type, information)

        if (User.is_user_available(data["email"])): 
            id = User.create(g, data["name"], data["surname"], data["email"], data["password"])            
            return f"Created user {id}."
        else:
            return "Email already in use."
        
    
    @app.route("/users/<int:id>", methods=["GET"])
    def get_user(id):
        return User.get_by_id(g, id)


    # @app.route("/users/<int:id>", methods=["PUT"])
    # def update_user(id):
    #     User.update_user_by_id(g, id, request.form.to_dict(flat=False))
    #     return f"Updated user {id}."

    
    @app.route("/users/<int:id>", methods=["DELETE"])
    def delete_user(id):
        User.delete(g, id)
        return f"Deleted user {id}."
    
    
    @app.route("/users/<int:id>/profile", methods=["GET"])
    def get_user_profile(id):
        return User.get_profile_by_id(g, id)
    
    
    @app.route("/users/<int:id>/email", methods=["PUT"])
    def update_user_email(id):
        data = request.form
        
        User.update_email(g, id, data["email"])
        return f"Updated email of user {id}."
    
    
    @app.route("/users/<int:id>/phone", methods=["PUT"])
    def update_user_phone(id):
        data = request.form
        
        User.update_phone(g, id, data["phone"])
        return f"Updated phone of user {id} to ."
    
    
    
    

    @app.route("/users/<int:user_id>/diplomas", methods=["POST"])
    def create_user_diploma(user_id):
        data = request.form
        
        diploma_id = Diploma.create(g, user_id, data["degree"], 
                                         data["profession"], data["institution"], 
                                         data["startDate"], data["endDate"])
        return f"Created diploma {diploma_id } of user {user_id}."
    
    
    @app.route("/users/<int:user_id>/diplomas", methods=["GET"])
    def get_user_diplomas(user_id):
        return Diploma.get_all_by_user_id(g, user_id)
    
    
    @app.route("/users/<int:user_id>/diplomas/<int:diploma_id>", methods=["GET"])
    def get_user_diploma(user_id, diploma_id):
        return Diploma.get_by_id(g, diploma_id)
    
    
    @app.route("/users/<int:user_id>/diplomas/<int:diploma_id>", methods=["PUT"])
    def update_user_diploma(user_id, diploma_id):
        data = request.form
        
        Diploma.update(g, user_id, diploma_id, 
                            data["degree"], data["profession"], 
                            data["institution"], data["startDate"], data["endDate"])
        return f"Updated diploma {diploma_id} of user {user_id}."
    
    
    @app.route("/users/<int:user_id>/diplomas/<int:diploma_id>", methods=["DELETE"])
    def delete_user_diploma(user_id, diploma_id):
        Diploma.delete(g, user_id, diploma_id)
        return f"Deleted diploma {diploma_id} of user {user_id}."
    
    
    
    
    @app.route("/users/<int:user_id>/languages", methods=["POST"])
    def add(user_id):
        data = request.form
        language = data["language"]
        Language.add(g, user_id, language)
        return f"Added language {language} to user {user_id}'s languages."
    
    
    @app.route("/users/<int:user_id>/languages", methods=["GET"])
    def get_all(user_id):
        return Language.get_all_by_user_id(g, user_id)
    
    
    @app.route("/users/<int:user_id>/languages/<string:language>", methods=["DELETE"])
    def remove(user_id, language):
        Language.remove(g, user_id, language)
        return f"Removed language {language} from user {user_id}'s languages."
    
    

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

        
    
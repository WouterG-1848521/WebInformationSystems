from flask import request

from backend_REST.models.user import User
from backend_REST.models.skill import Skill
from backend_REST.models.diploma import Diploma
from backend_REST.models.language import Language
from backend_REST.models.work_experience import WorkExperience

def create_user_routes(app, g):
    ########################################
    # USER ROUTES - BASICS
    ########################################
    @app.route("/users", methods=["GET"])
    def get_all_users():
        return User.get_all(g)

 
    @app.route("/users", methods=["POST"])
    def create_user():
        data = request.form     # request contains : name, surname, email, (encrypted) password (, type, information)

        # TODO: check data

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
        
        # TODO: check if owner
        
        User.delete(g, id)
        return f"Deleted user {id}."
    
    
    @app.route("/users/<int:id>/profile", methods=["GET"])
    def get_user_profile(id):
        return User.get_profile_by_id(g, id)
    
    
    @app.route("/users/<int:id>/email", methods=["PUT"])
    def update_user_email(id):
        data = request.form
        
        # TODO: check data
        
        User.update_email(g, id, data["email"])
        return f"Updated email of user {id}."
    
    
    @app.route("/users/<int:id>/phone", methods=["PUT"])
    def update_user_phone(id):
        data = request.form
        
        # TODO: check data
        
        User.update_phone(g, id, data["phone"])
        return f"Updated phone of user {id} to ."
    
    ########################################
    # USER ROUTES - DIPLOMAS
    ########################################
    

    @app.route("/users/<int:user_id>/diplomas", methods=["POST"])
    def create_user_diploma(user_id):
        data = request.form
        print(data)
        # TODO: check data
        
        diploma_id = Diploma.create_for_user(g, user_id, data["degree"], 
                                         data["profession"], data["institution"], 
                                         data["startDate"], data["endDate"])
        return f"Created diploma {diploma_id } for user {user_id}."
    
    
    @app.route("/users/<int:user_id>/diplomas", methods=["GET"])
    def get_user_diplomas(user_id):
        return Diploma.get_all_by_user_id(g, user_id)
    
    
    @app.route("/users/<int:user_id>/diplomas/<int:diploma_id>", methods=["GET"])
    def get_user_diploma(user_id, diploma_id):
        return Diploma.get_by_id(g, diploma_id)
    
    
    @app.route("/users/<int:user_id>/diplomas/<int:diploma_id>", methods=["PUT"])
    def update_user_diploma(user_id, diploma_id):
        data = request.form
        
        # TODO: check data
        
        Diploma.update(g, diploma_id, data["degree"], data["profession"], data["institution"], 
                                      data["startDate"], data["endDate"])
        return f"Updated diploma {diploma_id}."
    
    
    @app.route("/users/<int:user_id>/diplomas/<int:diploma_id>", methods=["DELETE"])
    def delete_user_diploma(user_id, diploma_id):
        
        # TODO: check if owner
        
        Diploma.delete_from_user(g, user_id, diploma_id)
        return f"Deleted diploma {diploma_id} from user {user_id}."
    
    
    ########################################
    # USER ROUTES - LANGUAGES
    ########################################
    
    
    @app.route("/users/<int:user_id>/languages", methods=["POST"])
    def add_language_to_user(user_id):
        data = request.form
        language = data["language"]
        Language.add_to_user(g, user_id, language)
        return f"Added language {language} to user {user_id}'s languages."
    
    
    @app.route("/users/<int:user_id>/languages", methods=["GET"])
    def get_all_languages_from_user(user_id):
        return Language.get_all_by_user_id(g, user_id)
    
    
    @app.route("/users/<int:user_id>/languages/<string:language>", methods=["DELETE"])
    def remove_language_from_user(user_id, language):
        Language.remove_from_user(g, user_id, language)
        return f"Removed language {language} from user {user_id}'s languages."
    
    ########################################
    # USER ROUTES - SKILLS
    ########################################
    
    @app.route("/users/<int:user_id>/skills", methods=["POST"])
    def add_skill_to_user(user_id):
        data = request.form
        skill = data["skill"]
        Skill.add_to_user(g, user_id, skill)
        return f"Added skill {skill} to user {user_id}'s skills."
    
    
    @app.route("/users/<int:user_id>/skills", methods=["GET"])
    def get_all_skills_from_user(user_id):
        return Skill.get_all_by_user_id(g, user_id)
    
    
    @app.route("/users/<int:user_id>/skills/<string:skill>", methods=["DELETE"])
    def remove_skill_from_user(user_id, skill):
        Skill.remove_from_user(g, user_id, skill)
        return f"Removed skill {skill} from user {user_id}'s skills."
    
    ########################################
    # USER ROUTES - WORK EXPERIENCE
    ########################################

    @app.route("/users/<int:user_id>/experiences", methods=["POST"])
    def create_user_experience(user_id):
        data = request.form  # job_title, skills, start_date, end_date
     
        # TODO: check data
        
        experience_id = WorkExperience.create_for_user(g, user_id, data["jobTitle"], 
                                         data["skills"].split(','), data["startDate"], 
                                         data["endDate"])
        return f"Created experience {experience_id } for user {user_id}."
    
    
    @app.route("/users/<int:user_id>/experiences", methods=["GET"])
    def get_user_experiences(user_id):
        return WorkExperience.get_all_by_user_id(g, user_id)
    
    
    @app.route("/users/<int:user_id>/experiences/<int:experience_id>", methods=["GET"])
    def get_user_experience(user_id, experience_id):
        return WorkExperience.get_by_id(g, experience_id)
    
    
    @app.route("/users/<int:user_id>/experiences/<int:experience_id>", methods=["PUT"])
    def update_user_experience(user_id, experience_id):
        data = request.form  # job_title, skills, start_date, end_date
        
        # TODO: check data
        
        WorkExperience.update(g, user_id, data["jobTitle"], 
                                data["skills"].split(','), data["startDate"], 
                                data["endDate"])
        return f"Updated experience {experience_id}."
    
    
    @app.route("/users/<int:user_id>/experiences/<int:experience_id>", methods=["DELETE"])
    def delete_user_experience(user_id, experience_id):
        
        # TODO: check if owner
        
        WorkExperience.delete_from_user(g, user_id, experience_id)
        return f"Deleted experience {experience_id} from user {user_id}."
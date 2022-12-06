from flask import jsonify, request
from flask_login import login_user, logout_user, login_required
from rdflib import Literal, RDF, URIRef

from pandas import DataFrame
import owlrl

from backend_REST import db, session
from backend_REST.models.database import DBUser
from backend_REST.graph import LOCAL, LANGUAGE, SKILL


def create_test_routes(app, g):

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

    @app.route("/db/add", methods=['GET'])
    def db_add_user():
        app.logger.info("Add user to DB...")
        user = DBUser(email="email", password="password")
        db.session.add(user)
        db.session.commit()

        return "Added user."

    @app.route("/db/get", methods=['GET'])
    @login_required
    def db_get_user():
        app.logger.info(
            f"User {session['user_id']} trying to GET something...")
        user = DBUser.query.filter_by(email='email').first()
        app.logger.info(user.id)

        return str(user.id)

    @app.route("/db/remove", methods=['GET'])
    def db_remove_user():
        app.logger.info("Removing user from DB...")
        user = DBUser.query.filter_by(email='email').first()
        db.session.delete(user)
        db.session.commit()

        # To delete all:
        DBUser.query.delete()

        return "Removed user."

    @app.route("/fill/skills", methods=['GET'])
    def fill_skills():
        g.add((URIRef(SKILL + "leadership"), RDF.type, LOCAL.skill))
        g.add((URIRef(SKILL + "teamwork"), RDF.type, LOCAL.skill))

        g.serialize(destination="user.ttl")

        return "Filled graph with the following skills: leadership, teamwork."

    @app.route("/fill/languages", methods=['GET'])
    def fill_languages():
        g.add((URIRef(LANGUAGE + "dutch"), RDF.type, LOCAL.language))
        g.add((URIRef(LANGUAGE + "english"), RDF.type, LOCAL.language))
        g.add((URIRef(LANGUAGE + "french"), RDF.type, LOCAL.language))

        g.serialize(destination="user.ttl")

        return "Filled graph with the following languages: dutch, english, french."

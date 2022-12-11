from flask import jsonify, request
from pandas import DataFrame
import json

from flask_login import login_required
from backend_REST import session
from config import GRAPH_FILE

from rdflib import Graph, URIRef, Literal, Namespace

from backend_REST.queries import query_enterpriseGetAll, query_enterpriseGetById, query_enterpriseGetByName, query_enterpriseGetByLocation, check_maintainer, check_owner, check_person
from backend_REST.queries import create_enterpriseRDF, query_update_enterpriseRDF, query_delete_enterpriseRDF, query_transfer_ownershipRDF
from backend_REST.queries import query_remove_maintainerRDF, query_add_maintainerRDF, check_enterprise

from backend_REST.models.enterprise import Enterprise
from backend_REST.models.response import Response

graphFile = GRAPH_FILE

def create_enterprise_routes(app, graph):
    # getters
    # get all enterprises
    @app.route("/enterprises", methods=['GET'])
    def get_all_enterprises():
        enterprisesJSON = json.loads(Enterprise.get_all_enterprises(graph))
        return Response.make_response_for_content_type_and_data(request.headers.get("Accept", "text/html"), data=enterprisesJSON, template="enterprises.html")

    # get enterprise by id
    @app.route("/enterprises/<int:id>", methods=['GET'])
    def get_enterprises_by_ID(id):
        enterprisesJSON = json.loads(Enterprise.get_by_id(graph, id))
        return Response.make_response_for_content_type_and_data(request.headers.get("Accept", "text/html"), data=enterprisesJSON, template="enterprise.html")

    # get enterprise by name
    @app.route("/enterprises/name/<string:name>", methods=['GET'])
    def get_enterprises_by_name(name):
        enterprisesJSON = json.loads(Enterprise.get_enterprises_by_name(graph, name))
        return Response.make_response_for_content_type_and_data(request.headers.get("Accept", "text/html"), data=enterprisesJSON, template="enterprise.html")
    

    # get enterprise by location
    @app.route("/enterprises/address/<string:address>", methods=['GET'])
    def get_enterprises_by_address(address):
        enterprisesJSON = json.loads(Enterprise.get_enterprises_by_address(graph, address))
        return Response.make_response_for_content_type_and_data(request.headers.get("Accept", "text/html"), data=enterprisesJSON, template="enterprise.html")

    # CRUD operations
    # create enterprise
    @app.route("/enterprises", methods=['POST'])
    @login_required
    def create_enterprise():
        data = request.form

        # check if data is in the request
        if "name" not in data:
            return "name is missing"
        if "lat" not in data:
            return "lat is missing"
        if "long" not in data:
            return "long is missing"
        if "address" not in data:
            return "address is missing"
        # if "owner" not in data:
        #     return "owner is missing"
        if "phone" not in data:
            return "phone is missing"
        if "email" not in data:
            return "email is missing"
        if "website" not in data:
            return "website is missing"
        if "description" not in data:
            return "description is missing"
        if "location" not in data:
            return "location is missing"

        # get the logged in user as the owner
        user_id = session['_user_id']
        owner = user_id
        print("owner: ", owner)

        name = data["name"]
        lat = data["lat"]
        lat = float(lat)
        long = data["long"]
        long = float(long)
        address = data["address"]
        owner = int(owner)
        phone = data["phone"]
        email = data["email"]
        website = data["website"]
        description = data["description"]
        location = data["location"]

        # check if data is correct
        if name == "" or lat == "" or long == "" or location == "" or owner == "" or phone == "" or email == "" or website == "" or description == "":
            return "Not all data is provided"
        if type(name) != str or type(lat) != float or type(long) != float or type(location) != str or type(owner) != int:
            print(type(name), type(lat), type(
                long), type(location), type(owner))
            return "Data is not of the correct type"
        # create(graph, name, lat, long, address, phone, email, website, owner, description, location)
        return Enterprise.create(graph, name, lat, long, address, phone, email, website, owner, description, location)    

    # update enterprise
    @app.route("/enterprises/<int:id>", methods=['PUT'])
    @login_required
    def update_enterprise(id):
        # request contains : maintainerid (for security check)
        data = request.form

        user_id = session['_user_id']
        maintainerID = user_id

        enterpriseID = int(id)

         # check if data is in the request
        name = ""
        lat = ""
        long = ""
        location = ""
        email = ""
        phone = ""
        website = ""
        description = ""
        address = ""
        if "name" in data:
            name = data["name"]
        if "lat" in data:
            lat = data["lat"]
        if "long" in data:
            long = data["long"]
        if "location" in data:
            location = data["location"]
        if ("email" in data):
            email = data["email"]
        if ("phone" in data):
            phone = data["phone"]
        if ("website" in data):
            website = data["website"]
        if ("description" in data):
            description = data["description"]  
        if ("address" in data):
            address = data["address"] 
        # update_enterprise(graph, enterpriseID, maintainerID, name, lat, long, address, phone, email, website, description, location)
        return Enterprise.update_enterprise(graph, enterpriseID, maintainerID, name, lat, long, address, phone, email, website, description, location)

    # delete enterprise
    @app.route("/enterprises", methods=['DELETE'])
    @login_required
    def delete_enterprise():
        # request contains : enterpriseID, ownerID (for security check)
        data = request.form

        user_id = session['_user_id']
        ownerID = user_id
        if "enterpriseID" not in data:
            return "enterpriseID is missing"
        enterpriseID = data["enterpriseID"]
        enterpriseID = int(enterpriseID)

        return Enterprise.delete_enterprise(graph, enterpriseID, ownerID)

    # transfer ownership
    @app.route("/enterprises/transfer", methods=['PUT'])
    @login_required
    def transfer_enterprise():
        data = request.form

        user_id = session['_user_id']
        ownerID = user_id
        if "enterpriseID" not in data:
            return "enterpriseID is missing"
        enterpriseID = data["enterpriseID"]
        enterpriseID = int(enterpriseID)

        # check if the newOwner is a person and a maintainer of the enterprise
        if "newOwnerID" not in data:
            return "newOwnerID is missing"
        newOwnerID = data["newOwnerID"]
        newOwnerID = int(newOwnerID)

        # transfer_enterprise(graph, ownerID, enterpriseID, newOwnerID)
        return Enterprise.transfer_enterprise(graph, ownerID, enterpriseID, newOwnerID)

    # Maintainers
    # add a maintainer to an enterprise
    @app.route("/enterprises/maintainer/add", methods=['POST'])
    @login_required
    def add_maintainer():
        data = request.form

        user_id = session['_user_id']
        ownerID = user_id
        if "enterpriseID" not in data:
            return "enterpriseID is missing"
        enterpriseID = data["enterpriseID"]
        enterpriseID = int(enterpriseID)

        # check if the maintainer is a person and not already a maintainer of the enterprise
        if "maintainerID" not in data:
            return "maintainerID is missing"
        maintainerID = data["maintainerID"]
        maintainerID = int(maintainerID)

        return Enterprise.add_maintainer(graph, enterpriseID, ownerID, maintainerID)

    # remove a maintainer from an enterprise
    @app.route("/enterprises/maintainer/remove", methods=['PUT'])
    @login_required
    def remove_maintainer():
        data = request.form     # request contains : enterpriseID, ownerID (for security check), MaintainerID
        
        user_id = session['_user_id']
        ownerID = user_id
        if "enterpriseID" not in data:
            return "enterpriseID is missing"
        enterpriseID = data["enterpriseID"]
        enterpriseID = int(enterpriseID)

        # check if the maintainer is a person and not already a maintainer of the enterprise
        if "maintainerID" not in data:
            return "maintainerID is missing"
        maintainerID = data["maintainerID"]
        maintainerID = int(maintainerID)

        # remove_maintainer(graph, ownerID, enterpriseID, maintainerID)
        return Enterprise.remove_maintainer(graph, ownerID, enterpriseID, maintainerID)

    # get the enterprises on a specific location
    @app.route("/enterprises/location/<int:location>", methods=['GET'])
    def get_enterprises_location(location):
        enterprisesJSON = json.loads(Enterprise.get_onLocation(graph, location))
        return Response.make_response_for_content_type_and_data(request.headers.get("Accept", "text/html"), data=enterprisesJSON, template="enterprise.html")

    # get the enterprises close to a specif lat and long
    @app.route("/enterprises/locationLL/<float:lat>/<float:long>/<float:distance>", methods=['GET'])
    @app.route("/enterprises/locationLL/<float:lat>/<float:long>/<int:distance>", methods=['GET'])
    def get_enterprises_close(lat, long, distance):
        enterprisesJSON = json.loads(Enterprise.get_onLATLONGLocation(graph, lat, long, distance))
        return Response.make_response_for_content_type_and_data(request.headers.get("Accept", "text/html"), data=enterprisesJSON, template="enterprise.html")
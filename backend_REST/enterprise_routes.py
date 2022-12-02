from flask import jsonify, request
from pandas import DataFrame

from rdflib import Graph, URIRef, Literal, Namespace

from .queries import query_enterpriseGetAll, query_enterpriseGetById, query_enterpriseGetByName, query_enterpriseGetByLocation, check_maintainer, check_owner, check_person
from .queries import create_enterpriseRDF, query_update_enterpriseRDF, query_delete_enterpriseRDF, query_transfer_ownershipRDF
from .queries import query_remove_maintainerRDF, query_add_maintainerRDF, check_enterprise

# TODO: security voor machtegingen, nu wordt gewoon bv ownerID meegegeven in post body.
#       Dit is niet secure en zo via bv cookies of andere log-in moeten

graphFile = "graph.ttl"

def create_enterprise_routes(app, graph):
    # getters
    # get all enterprises
    @app.route("/enterprise/get/all", methods=['GET'])
    def get_all_enterprises():
        query = query_enterpriseGetAll()
        result = graph.query(query)
        df = DataFrame(result, columns=result.vars)

        return df.to_json(orient='index', indent=2)

    # get enterprise by id
    @app.route("/enterprise/get/id/<int:id>", methods=['GET'])
    def get_enterprises_by_ID(id):
        query = query_enterpriseGetById(id)
        print(query)
        result = graph.query(query)
        df = DataFrame(result, columns=result.vars)
        # TODO : hoe groeperen per enterprise? per maintainer is er een aparte entry

        return df.to_json(orient='index', indent=2) 

    # get enterprise by name
    @app.route("/enterprise/get/name/<string:name>", methods=['GET'])
    def get_enterprises_by_name(name):
        query = query_enterpriseGetByName(name)
        print(query)
        result = graph.query(query)
        df = DataFrame(result, columns=result.vars)

        return df.to_json(orient='index', indent=2)

    # get enterprise by location
    @app.route("/enterprise/get/location/<string:location>", methods=['GET'])
    def get_enterprises_by_location(location):
        query = query_enterpriseGetByLocation(location)
        print(query)
        # TODO: mayby search on distance
        result = graph.query(query)
        df = DataFrame(result, columns=result.vars)

        return df.to_json(orient='index', indent=2)

    # CRUD operations
    # create enterprise
    @app.route("/enterprise/create", methods=['POST'])
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
        if "owner" not in data:
            return "owner is missing"
        if "phone" not in data:
            return "phone is missing"
        if "email" not in data:
            return "email is missing"
        if "website" not in data:
            return "website is missing"
        if "description" not in data:
            return "description is missing"
        

        enterpriseID = 0

        name = data["name"]
        lat = data["lat"]
        lat = float(lat)
        long = data["long"]
        long = float(long)
        location = data["location"]
        owner = data["owner"]
        owner = int(owner)
        phone = data["phone"]
        email = data["email"]
        website = data["website"]
        description = data["description"]

        # check if data is correct
        if name == "" or lat == "" or long == "" or location == "" or owner == "" or phone == "" or email == "" or website == "" or description == "":
            return "Not all data is provided"
        if type(name) != str or type(lat) != float or type(long) != float or type(location) != str or type(owner) != int:
            print(type(name), type(lat), type(long), type(location), type(owner))
            return "Data is not of the correct type"

        enterpriseID = create_enterpriseRDF(graph, name, owner, lat, long, location, phone, email, website, description)

        graph.serialize(destination=graphFile)
        
        return "Enterprise created with ID: " + str(enterpriseID)     

    # update enterprise
    @app.route("/enterprise/update/<int:id>", methods=['PUT'])
    def update_enterprise(id):
        data = request.form     # request contains : maintainerid (for security check)

        # check if request contains enterpriseID and maintainerID
        if "maintainerID" not in data:
            return "maintainerID is missing"
        maintainerID = data["maintainerID"]
        maintainerID = int(maintainerID)
        if "enterpriseID" not in data:
            return "enterpriseID is missing"
        enterpriseID = data["enterpriseID"]
        enterpriseID = int(enterpriseID)

        # check if enterprise exists
        if not check_enterprise(graph, enterpriseID):
            return "Enterprise does not exist"

        # check if the maintainer is allowed to update the enterprise
        if not (check_maintainer(graph, maintainerID, enterpriseID)):
            return "only maintainer of enterprise can update the enterprise"

         # check if data is in the request
        name = ""
        lat = ""
        long = ""
        location = ""
        email = ""
        phone = ""
        website = ""
        description = ""
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

        query = query_update_enterpriseRDF(name, lat, long, location, phone, email, website, description, enterpriseID)
        graph.update(query)
        graph.serialize(destination=graphFile)   # TODO : moet dit nu al ge serialized worden naar de echte graaf, of kunnen we dit periodiek laten gebueren
        # TODO : hoe controleer je of de update gelukt is?

        return "update enterprise"

    # delete enterprise
    @app.route("/enterprise/delete", methods=['DELETE'])
    def delete_enterprise():
        data = request.form     # request contains : enterpriseID, ownerID (for security check)

        # check if request contains enterpriseID and ownerID
        if "ownerID" not in data:
            return "ownerID is missing"
        ownerID = data["ownerID"]
        ownerID = int(ownerID)
        if "enterpriseID" not in data:
            return "enterpriseID is missing"
        enterpriseID = data["enterpriseID"]
        enterpriseID = int(enterpriseID)

        # check if enterprise exists
        if not check_enterprise(graph, enterpriseID):
            return "Enterprise does not exist"

        # check if the owner is allowed to delete the enterprise
        if not (check_owner(graph, enterpriseID, ownerID)):
            return "only owner of enterprise can delete the enterprise"

        query = query_delete_enterpriseRDF(enterpriseID)
        graph.update(query)
        graph.serialize(destination=graphFile)   # TODO : moet dit nu al ge serialized worden naar de echte graaf, of kunnen we dit periodiek laten gebueren
        # TODO : hoe controleer je of de delete gelukt is?

        return "delete enterprise"

    # transfer ownership
    @app.route("/enterprise/transfer", methods=['PUT'])
    def transfer_enterprise():
        data = request.form

        # check if request contains enterpriseID and ownerID
        if "ownerID" not in data:
            return "ownerID is missing"
        ownerID = data["ownerID"]
        ownerID = int(ownerID)
        if "enterpriseID" not in data:
            return "enterpriseID is missing"
        enterpriseID = data["enterpriseID"]
        enterpriseID = int(enterpriseID)

        # check if enterprise exists
        if not check_enterprise(graph, enterpriseID):
            return "Enterprise does not exist"

        # check if the owner is allowed to transfer the enterprise
        if not (check_owner(graph, ownerID, enterpriseID)):
            return "only owner of enterprise can transfer the enterprise"

        # check if the newOwner is a person and a maintainer of the enterprise
        if "newOwnerID" not in data:
            return "newOwnerID is missing"
        newOwnerID = data["newOwnerID"]
        newOwnerID = int(newOwnerID)

        if not (check_person(graph, newOwnerID)):
            return "newOwner is not a person"

        if not (check_maintainer(graph, enterpriseID, newOwnerID)):
            return "new owner is not a maintainer of the enterprise"
        
        query = query_transfer_ownershipRDF(enterpriseID, newOwnerID)
        graph.update(query)
        graph.serialize(destination=graphFile)   # TODO : moet dit nu al ge serialized worden naar de echte graaf, of kunnen we dit periodiek laten gebueren
        # TODO : hoe controleer je of de update gelukt is?
    
        return "transfer enterprise"

    # Maintainers
    # add a maintainer to an enterprise
    @app.route("/enterprise/maintainer/add", methods=['POST'])
    def add_maintainer():
        data = request.form

        # check if request contains enterpriseID and ownerID
        if "ownerID" not in data:
            return "ownerID is missing"
        ownerID = data["ownerID"]
        ownerID = int(ownerID)
        if "enterpriseID" not in data:
            return "enterpriseID is missing"
        enterpriseID = data["enterpriseID"]
        enterpriseID = int(enterpriseID)

        # check if enterprise exists
        if not check_enterprise(graph, enterpriseID):
            return "Enterprise does not exist"

        # check if the owner is allowed to transfer the enterprise
        if not (check_owner(graph, ownerID, enterpriseID)):
            return "only owner of enterprise can transfer the enterprise"


        # check if the maintainer is a person and not already a maintainer of the enterprise
        if "maintainerID" not in data:
            return "maintainerID is missing"
        maintainerID = data["maintainerID"]
        maintainerID = int(maintainerID)

        if not (check_person(graph, maintainerID)):
            return "maintainerID is not a person"

        if (check_maintainer(graph, maintainerID, enterpriseID)):
            return "maintainerID is already a maintainer of the enterprise"

        query = query_add_maintainerRDF(enterpriseID, maintainerID)
        graph.update(query)
        graph.serialize(destination=graphFile)   # TODO : moet dit nu al ge serialized worden naar de echte graaf, of kunnen we dit periodiek laten gebueren
        # TODO : hoe controleer je of de update gelukt is?
        
        return "added maintainer"

    # remove a maintainer from an enterprise
    @app.route("/enterprise/maintainer/remove", methods=['PUT'])
    def remove_maintainer():
        data = request.form     # request contains : enterpriseID, ownerID (for security check), MaintainerID
        
        # check if request contains enterpriseID and ownerID
        if "ownerID" not in data:
            return "ownerID is missing"
        ownerID = data["ownerID"]
        ownerID = int(ownerID)
        if "enterpriseID" not in data:
            return "enterpriseID is missing"
        enterpriseID = data["enterpriseID"]
        enterpriseID = int(enterpriseID)

        # check if enterprise exists
        if not check_enterprise(graph, enterpriseID):
            return "Enterprise does not exist"

        # check if the owner is allowed to transfer the enterprise
        if not (check_owner(graph, enterpriseID, ownerID)):
            return "only owner of enterprise can transfer the enterprise"


        # check if the maintainer is a person and not already a maintainer of the enterprise
        if "maintainerID" not in data:
            return "maintainerID is missing"
        maintainerID = data["maintainerID"]
        maintainerID = int(maintainerID)

        if not (check_maintainer(graph, enterpriseID, maintainerID)):
            return "maintainerID is no maintainer of the enterprise"

        # check that the owner is not removing himself
        if (ownerID == maintainerID):
            return "owner cannot remove himself"

        query = query_remove_maintainerRDF(enterpriseID, maintainerID)
        graph.update(query)
        graph.serialize(destination=graphFile)   # TODO : moet dit nu al ge serialized worden naar de echte graaf, of kunnen we dit periodiek laten gebueren
        # TODO : hoe controleer je of de update gelukt is?
        return "remove maintainer"


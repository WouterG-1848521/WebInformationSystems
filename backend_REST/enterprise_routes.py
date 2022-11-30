from flask import jsonify, request
from pandas import DataFrame

from rdflib import Graph, URIRef, Literal, Namespace

from .queries import query_enterpriseGetAll, query_enterpriseGetById, query_enterpriseGetByName, query_enterpriseGetByLocation, check_maintainer, check_owner, check_person
from .queries import create_enterpriseInfoRDF, create_enterpriseRDF, query_update_enterpriseRDF, query_delete_enterpriseRDF, query_transfer_ownershipRDF
from .queries import query_remove_maintainerRDF, query_add_maintainerRDF, query_get_enterpriseInfoRDF, check_enterpriseHasInfo, query_add_enterpriseInfoToEnterprise

# TODO: security voor machtegingen, nu wordt gewoon bv ownerID meegegeven in post body.
#       Dit is niet secure en zo via bv cookies of andere log-in moeten

def create_vacancy_routes(app, graph):
    # add a vacancy to an enterprise
    @app.route("/enterprise/vacancy/add", methods=['POST'])
    def add_vacancy():
        data = request.form     # request contains : enterpriseID, mainterID (for security check), jobtitle, address, startdate, enddate
            # waarschijnlijk ook nog een lijst van skills
        print(data)
        # TODO: insert in rdf 
        return "add vacancy"

    # remove a vacancy from an enterprise
    @app.route("/enterprise/vacancy/remove", methods=['POST'])
    def remove_vacancy():
        data = request.form     # request contains : enterpriseID, vacancyID, mainterID (for security check)
        print(data)
        # TODO: remove in rdf 
        return "remove vacancy"

    # match a vacancy from parameters
    @app.route("/vacancy/match", methods=['POST'])
    def match_vacancy():
        data = request.form    # request contains : parameters to search a vacancy for

def create_enterprise_routes(app, graph):
    # getters
    # get all enterprises
    @app.route("/enterprise/get/all", methods=['GET'])
    def get_all_enterprises():
        query = query_enterpriseGetAll()
        print(query)
        result = graph.query(query)
        df = DataFrame(result, columns=result.vars)
        print(df)

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
        if "location" not in data:
            return "location is missing"
        if "owner" not in data:
            return "owner is missing"
        

        enterpriseID = 0

        name = data["name"]
        lat = data["lat"]
        lat = float(lat)
        long = data["long"]
        long = float(long)
        location = data["location"]
        owner = data["owner"]
        owner = int(owner)

        # check if data is correct
        if name == "" or lat == "" or long == "" or location == "" or owner == "":
            return "Not all data is provided"
        if type(name) != str or type(lat) != float or type(long) != float or type(location) != str or type(owner) != int:
            print(type(name), type(lat), type(long), type(location), type(owner))
            return "Data is not of the correct type"

        # check if we get an enterpriseInfoID or if we need to create one
        if "enterpriseInfo" in data:
            enterpriseInfoID = data["enterpriseInfo"]
            enterpriseInfoID = int(enterpriseInfoID)
            if enterpriseInfoID == "" or type(enterpriseInfoID) != int:
                return "Data is not correct"
            enterpriseID = create_enterpriseRDF(graph, name, lat, long, location, owner, enterpriseInfoID)
        else:
            if "enterpriseInfoDescription" not in data:
                return "enterpriseInfoDescription is missing"

            enterpriseInfoDescription = data["enterpriseInfoDescription"]
            if (enterpriseInfoDescription == "" or type(enterpriseInfoDescription) != str):
                return "Data is not correct"
            enterpriseInfoID = create_enterpriseInfoRDF(graph, enterpriseInfoDescription)
            enterpriseID = create_enterpriseRDF(graph, name, lat, long, location, owner, enterpriseInfoID)

        graph.serialize(destination="graph.ttl")
        
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

        # check if the maintainer is allowed to update the enterprise
        if not (check_maintainer(graph, maintainerID, enterpriseID)):
            return "only maintainer of enterprise can update the enterprise"

         # check if data is in the request
        name = ""
        lat = ""
        long = ""
        location = ""
        enterpriseInfoID = ""
        if "name" in data:
            name = data["name"]
        if "lat" in data:
            lat = data["lat"]
        if "long" in data:
            long = data["long"]
        if "location" in data:
            location = data["location"]
        if ("enterpriseInfo" in data):
            enterpriseInfoID = data["enterpriseInfo"]       

        query = query_update_enterpriseRDF(name, lat, long, location, enterpriseInfoID, enterpriseID)
        graph.update(query)
        graph.serialize(destination="graph.ttl")   # TODO : moet dit nu al ge serialized worden naar de echte graaf, of kunnen we dit periodiek laten gebueren
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

        # check if the owner is allowed to delete the enterprise
        if not (check_owner(graph, enterpriseID, ownerID)):
            return "only owner of enterprise can delete the enterprise"

        query = query_delete_enterpriseRDF(enterpriseID)
        print(query)
        graph.update(query)
        graph.serialize(destination="graph.ttl")   # TODO : moet dit nu al ge serialized worden naar de echte graaf, of kunnen we dit periodiek laten gebueren
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
        graph.serialize(destination="graph.ttl")   # TODO : moet dit nu al ge serialized worden naar de echte graaf, of kunnen we dit periodiek laten gebueren
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
        graph.serialize(destination="graph.ttl")   # TODO : moet dit nu al ge serialized worden naar de echte graaf, of kunnen we dit periodiek laten gebueren
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

        # check if the owner is allowed to transfer the enterprise
        if not (check_owner(graph, ownerID, enterpriseID)):
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
        graph.serialize(destination="graph.ttl")   # TODO : moet dit nu al ge serialized worden naar de echte graaf, of kunnen we dit periodiek laten gebueren
        # TODO : hoe controleer je of de update gelukt is?
        return "remove maintainer"

    # Enterprise page
    # get enterprise page
    @app.route("/enterprise/enterpriseInfo/get/<id>", methods=['GET'])
    def get_enterprise_info(id):
        id = int(id)
        query = query_get_enterpriseInfoRDF(id)
        print(query)

        result = graph.query(query)
        df = DataFrame(result, columns=result.vars)

        return df.to_json(orient='index', indent=2)

    # create neterprise page
    @app.route("/enterprise/enterpriseInfo/create", methods=['POST'])
    def create_enterprise_page():
        data = request.form    # request contains : enterpriseID, mainterID (for security check), description, website, ...

        # check if request contains enterpriseID and maintainerID
        if "maintainerID" not in data:
            return "maintainerID is missing"
        maintainerID = data["maintainerID"]
        maintainerID = int(maintainerID)
        if "enterpriseID" not in data:
            return "enterpriseID is missing"
        enterpriseID = data["enterpriseID"]
        enterpriseID = int(enterpriseID)

        # check if the maintainer is allowed to create the enterprise page
        if not (check_maintainer(graph, enterpriseID, maintainerID)):
            return "only maintainer of enterprise can create enterprise page"

        # check if the enterprise page already exists
        if (check_enterpriseHasInfo(graph, enterpriseID)):
            return "enterprise page already exists"

        # check if the request contains all the required data
        if "description" not in data:
            return "description is missing"
        description = data["description"]
        

        enterpriseInfoID = create_enterpriseInfoRDF(graph, description)

        # Add the enterpriseInfo to the enterprise
        query = query_add_enterpriseInfoToEnterprise(enterpriseInfoID, enterpriseID)
        graph.update(query)

        graph.serialize(destination="graph.ttl")   # TODO : moet dit nu al ge serialized worden naar de echte graaf, of kunnen we dit periodiek laten gebueren
        # TODO : hoe controleer je of de update gelukt is?

        return "create enterprise page"

    # update enterprise page
    @app.route("/enterprise/enterpriseInfo/update", methods=['PUT'])
    def update_enterprise_page():   # TODO
        data = request.form     # request contains : enterpriseID, MaintainerID(for security check), description, website, ...
        print(data)
        # TODO: update in rdf 
        return "update enterprise page"


    # Vacancies
    create_vacancy_routes(app, graph)

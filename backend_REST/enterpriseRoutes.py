from flask import jsonify, request

enterprises = {}

def setup_DEBUG():
    global enterprises

    for i in range(10):
        enterprises[i] = {
            "id": i,
            "name": f"Enterprise {i}",
            "address": f"Address of enterprise {i}",
            "maintainerid": [i * 3, i * 3 + 1, i * 3 + 2, i * 2],
            "ownerid": i * 2
        }

def create_enterprise_routes(app):
    setup_DEBUG()

    # getters
    # get all enterprises
    @app.route("/enterprise/get/all", methods=['GET'])
    def get_all_enterprises():
        # TODO : get from rdf
        return jsonify(enterprises)

    # get enterprise by id
    @app.route("/enterprise/get/id/<id>", methods=['GET'])
    def get_enterprises_by_ID(id):
        # TODO: get out of rdf
        return jsonify(enterprises[0])

    # get enterprise by name
    @app.route("/enterprise/get/name/<name>", methods=['GET'])
    def get_enterprises_by_name(name):
        # TODO: get out of rdf 
        return jsonify(enterprises[0])

    # get enterprise by location
    @app.route("/enterprise/get/location/<location>", methods=['GET'])
    def get_enterprises_by_location(location):
        # TODO: get out of rdf, mayby search on distance
        return jsonify(enterprises[0])

    # CRUD operations
    # create enterprise
    @app.route("/enterprise/create", methods=['POST'])
    def create_enterprise():
        data = request.form     # request contains : name, address, ownerID
        print(data)
        # TODO: add to rdf 
        return "create enterprise"

    # update enterprise
    @app.route("/enterprise/update", methods=['PUT'])
    def update_enterprise():
        data = request.form     # request contains : enterpriseID, maintainerid (for security check), name, address
        print(data)
        # TODO: updated in rdf 
        return "update enterprise"

    # delete enterprise
    @app.route("/enterprise/delete", methods=['DELETE'])
    def delete_enterprise():
        data = request.form     # request contains : enterpriseID, ownerID (for security check)
        print(data)
        # TODO: delete in rdf 
        return "delete enterprise"

    # transfer ownership
    @app.route("/enterprise/transfer", methods=['PUT'])
    def transfer_enterprise():
        data = request.form     # request contains : enterpriseID, ownerID (for security check), newOwnerID
        print(data)
        # TODO: delete in rdf 
        return "transfer enterprise"

    # Vacancies
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


    # Maintainers
    # add a maintainer to an enterprise
    @app.route("/enterprise/maintainer/add", methods=['POST'])
    def add_maintainer():
        data = request.form     # request contains : enterpriseID, ownerID (for security check), newMaintainerID
        print(data)
        # TODO: insert in rdf 
        return "add maintainer"

    # remove a maintainer from an enterprise
    @app.route("/enterprise/maintainer/remove", methods=['POST'])
    def remove_maintainer():
        data = request.form     # request contains : enterpriseID, ownerID (for security check), MaintainerID
        print(data)
        # TODO: remove in rdf 
        return "remove maintainer"

    # Enterprise page
    # get enterprise page
    @app.route("/enterprise/enterpriseInfo/get/<id>", methods=['GET'])
    def get_enterprise_page(id):
        # TODO: get out of rdf
        return "get enterprise page"

    # create neterprise page
    @app.route("/enterprise/enterpriseInfo/create", methods=['POST'])
    def create_enterprise_page():
        data = request.form    # request contains : enterpriseID, mainterID (for security check), description, website, ...
        print(data)
        # TODO: insert in rdf
        return "create enterprise page"

    # update enterprise page
    @app.route("/enterprise/enterpriseInfo/update", methods=['PUT'])
    def update_enterprise_page():
        data = request.form     # request contains : enterpriseID, MaintainerID(for security check), description, website, ...
        print(data)
        # TODO: update in rdf 
        return "update enterprise page"

from flask import jsonify, request
from pandas import DataFrame

from rdflib import Graph, URIRef, Literal, Namespace
from rdflib.namespace import RDF, FOAF, RDFS

from .queries import query_enterpriseGetAll

enterprises = {}

NS1 = Namespace("http://localhost/")


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
    setup_DEBUG()

    # getters
    # get all enterprises
    @app.route("/enterprise/get/all", methods=['GET'])
    def get_all_enterprises():
        query = query_enterpriseGetAll()
        print(query)
        # query = f'''
        #     SELECT ?p ?name
        #     WHERE {{
        #         ?p rdf:type <http://xmlns.com/foaf/0.1/Organization> .
        #     }}
        # '''
        result = graph.query(query)
        df = DataFrame(result, columns=result.vars)
        print(df)

        return df.to_json()

    # get enterprise by id
    @app.route("/enterprise/get/id/<int:id>", methods=['GET'])
    def get_enterprises_by_ID(id):
        query = f'''
            SELECT ?p
            WHERE {{
                ?p rdf:type <http://xmlns.com/foaf/0.1/Organization> .
                ?p <http://localhost/hasId> {id} .
            }}
        '''
        result = graph.query(query)
        df = DataFrame(result, columns=result.vars)

        return df.to_json() 

    # get enterprise by name
    @app.route("/enterprise/get/name/<string:name>", methods=['GET'])
    def get_enterprises_by_name(name):
        app.logger.info(name)
        query = f'''
            SELECT ?p
            WHERE {{
                ?p rdf:type <http://xmlns.com/foaf/0.1/Organization> .
                ?p <http://localhost/hasName> "{name}" .
            }}
        '''
        result = graph.query(query)
        df = DataFrame(result, columns=result.vars)

        return df.to_json() 

    # get enterprise by location
    @app.route("/enterprise/get/location/<string:location>", methods=['GET'])
    def get_enterprises_by_location(location):
        # TODO: get out of rdf, mayby search on distance
        return jsonify(enterprises[0])

    # CRUD operations
    # create enterprise
    @app.route("/enterprise/create", methods=['POST'])
    def create_enterprise():
        data = request.form     # request contains : name, address, ownerID
        name = data["name"]
        
        URI = "http://localhost/Enterprise/" + str(7)
        enterprise = URIRef(URI)

        graph.bind("ns1", NS1)
        
        graph.add((enterprise, RDF.type, FOAF.Organization))
        graph.add((enterprise, NS1.hasName, Literal(name)))
        
        graph.serialize(destination="test.ttl")
        
        return "create enterprise"

    # update enterprise
    @app.route("/enterprise/update/<int:id>", methods=['PUT'])
    def update_enterprise(id):
        data = request.form     # request contains : maintainerid (for security check), name, address
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
    create_vacancy_routes(app, graph)


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

from pandas import DataFrame
from rdflib import Literal, RDF, URIRef
from rdflib.namespace import RDF, RDFS, FOAF, XSD
from backend_REST.graph import LOCAL

from backend_REST import db
from config import GRAPH_FILE

from backend_REST.models.database import DBEnterprise

from backend_REST.queries import query_enterpriseGetAll, query_enterpriseGetById, query_enterpriseGetByName, query_enterpriseGetByLocation, check_maintainer, check_owner, check_person
from backend_REST.queries import create_enterpriseRDF, query_update_enterpriseRDF, query_delete_enterpriseRDF, query_transfer_ownershipRDF
from backend_REST.queries import query_remove_maintainerRDF, query_add_maintainerRDF, check_enterprise

gFile = "graph.ttl"

# TODO : delete omzetten naar rdflib vorm
# DONE : update omzetten
# DONE : create omzetten
# DONE : log in testen
# DONE : ID by create uit db halen
# TODO : location bij enterprise insteken via gn, nog bij delete
# TODO : matchen on lacation

class Enterprise:

    def get_maintainers_by_id(graph, enterprise_id):
        q = f'''
                SELECT ?p
                WHERE {{
                    enterprise:{enterprise_id} a enterprise .
                    ?p local:maintains enterprise:{enterprise_id} .
                }}
            '''
        result = graph.query(q)
        df = DataFrame(result, columns=result.vars)
        return df.to_json()

    def get_by_id(graph, enterprise_id):
        query = query_enterpriseGetById(enterprise_id)
        result = graph.query(query)

        df = DataFrame(result, columns=result.vars)

        return df.to_json(orient='index', indent=2)

    def get_all_enterprises(graph):
        query = query_enterpriseGetAll()
        result = graph.query(query)
        df = DataFrame(result, columns=result.vars)

        return df.to_json(orient='index', indent=2)

    def get_enterprises_by_name(graph, name):
        query = query_enterpriseGetByName(name)
        print(query)
        result = graph.query(query)
        df = DataFrame(result, columns=result.vars)

        return df.to_json(orient='index', indent=2)

    def get_enterprises_by_location(graph, location):
        query = query_enterpriseGetByLocation(location)
        print(query)
        # TODO: mayby search on distance
        result = graph.query(query)
        df = DataFrame(result, columns=result.vars)

        return df.to_json(orient='index', indent=2)

    def create(graph, name, lat, long, address, phone, email, website, owner, description, location):
        # Add enterprise to DB
        enterprise = DBEnterprise()
        db.session.add(enterprise)
        db.session.commit()
        
        # Get user_id
        enterpriseID = enterprise.id
        print(enterpriseID)

        create_enterpriseRDF(graph, name, owner, lat, long, address, phone, email, website, description, enterpriseID, location)

        graph.serialize(destination=gFile)
        
        return "Enterprise created with ID: " + str(enterpriseID)    

    def update_enterprise(graph, enterpriseID, maintainerID, name, lat, long, address, phone, email, website, description, location):
        # check if enterprise exists
        if not check_enterprise(graph, enterpriseID):
            return "Enterprise does not exist"

        # check if the maintainer is allowed to update the enterprise
        if not (check_maintainer(graph, maintainerID, enterpriseID)):
            return "only maintainer of enterprise can update the enterprise"

        query = query_update_enterpriseRDF(name, lat, long, address, phone, email, website, description, enterpriseID, location)
        graph.update(query)
        graph.serialize(destination=gFile)
        # TODO : hoe controleer je of de update gelukt is?

        return "update enterprise"

    def delete_enterprise(graph, enterpriseID, ownerID):
        # check if enterprise exists
        if not check_enterprise(graph, enterpriseID):
            return "Enterprise does not exist"

        # check if the owner is allowed to delete the enterprise
        if not (check_owner(graph, enterpriseID, ownerID)):
            return "only owner of enterprise can delete the enterprise"

        query = query_delete_enterpriseRDF(enterpriseID)
        graph.update(query)
        graph.serialize(destination=gFile)
        # TODO : hoe controleer je of de delete gelukt is?

        return "delete enterprise"

    def transfer_enterprise(graph, ownerID, enterpriseID, newOwnerID):
        # check if enterprise exists
        if not check_enterprise(graph, enterpriseID):
            return "Enterprise does not exist"

        # check if the owner is allowed to transfer the enterprise
        if not (check_owner(graph, ownerID, enterpriseID)):
            return "only owner of enterprise can transfer the enterprise"

        if not (check_person(graph, newOwnerID)):
            return "newOwner is not a person"

        if not (check_maintainer(graph, enterpriseID, newOwnerID)):
            return "new owner is not a maintainer of the enterprise"
        
        query = query_transfer_ownershipRDF(enterpriseID, newOwnerID)
        graph.update(query)
        graph.serialize(destination=gFile)  
        # TODO : hoe controleer je of de update gelukt is?
    
        return "transfer enterprise"

    def add_maintainer(graph, enterpriseID, ownerID, maintainerID):
        # check if enterprise exists
        if not check_enterprise(graph, enterpriseID):
            return "Enterprise does not exist"

        # check if the owner is allowed to transfer the enterprise
        if not (check_owner(graph, ownerID, enterpriseID)):
            return "only owner of enterprise can transfer the enterprise"

        if not (check_person(graph, maintainerID)):
            return "maintainerID is not a person"

        if (check_maintainer(graph, maintainerID, enterpriseID)):
            return "maintainerID is already a maintainer of the enterprise"

        query = query_add_maintainerRDF(enterpriseID, maintainerID)
        graph.update(query)
        graph.serialize(destination=gFile)   
        # TODO : hoe controleer je of de update gelukt is?
        
        return "added maintainer"

    def remove_maintainer(graph, ownerID, enterpriseID, maintainerID):
        # check if enterprise exists
        if not check_enterprise(graph, enterpriseID):
            return "Enterprise does not exist"

        # check if the owner is allowed to transfer the enterprise
        if not (check_owner(graph, enterpriseID, ownerID)):
            return "only owner of enterprise can transfer the enterprise"

        if not (check_maintainer(graph, enterpriseID, maintainerID)):
            return "maintainerID is no maintainer of the enterprise"

        # check that the owner is not removing himself
        if (ownerID == maintainerID):
            return "owner cannot remove himself"

        query = query_remove_maintainerRDF(enterpriseID, maintainerID)
        graph.update(query)
        graph.serialize(destination=gFile)   
        return "remove maintainer"
from pandas import DataFrame
from rdflib import Literal, RDF, URIRef
from rdflib.namespace import RDF, RDFS, FOAF, XSD
from backend_REST.graph import ENTERPRISE, VACANCY
from math import sqrt

from backend_REST import db
from config import GRAPH_FILE

from backend_REST.models.database import DBEnterprise

from backend_REST.queries import query_enterpriseGetAll, query_enterpriseGetById, query_enterpriseGetByName, query_enterpriseGetByLocation, check_maintainer, check_owner, check_person
from backend_REST.queries import create_enterpriseRDF, query_update_enterpriseRDF, query_enterpriseGetByAddress, query_transfer_ownershipRDF, query_enterpriseGetByOwner
from backend_REST.queries import query_remove_maintainerRDF, query_add_maintainerRDF, check_enterprise, query_enterpriseGetByLocation, query_getVacanciesOfEnterprise

gFile = GRAPH_FILE

def groupByMaintainer(df):
    r = DataFrame()
    df = df.reset_index()
    for index, row in df.iterrows():
        inside = False
        # check if it is already in the list
        for index, row2 in r.iterrows():
            if row[1] == row2[1]:
                # add the maintainer to the list
                r.at[index, 'maintainer'] = r.at[index, 'maintainer'] + "," + row[4]
                inside = True
                break
        if not inside:
            # ?uri ?name ?owner ?maintainer ?lat ?long ?address ?description ?phone ?email ?website ?location
            r = r.append({'id': row[0], 'name': row[1], 'lat': row[2], 'owner': row[3], 'maintainer': row[4], 'lat': row[5], 'long': row[6], 'address': row[7], 'description': row[8], 'phone': row[9], 'email': row[10], 'website': row[11], 'location': row[12]}, ignore_index=True)

    return r

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

        df = groupByMaintainer(df)

        return df.to_json(orient='index', indent=2)

    def get_all_enterprises(graph):
        query = query_enterpriseGetAll()
        result = graph.query(query)
        df = DataFrame(result, columns=result.vars)

        df = groupByMaintainer(df)

        return df.to_json(orient='index', indent=2)

    def get_enterprises_by_name(graph, name):
        query = query_enterpriseGetByName(name)
        result = graph.query(query)
        df = DataFrame(result, columns=result.vars)
        df = groupByMaintainer(df)

        return df.to_json(orient='index', indent=2)

    def get_enterprises_by_address(graph, address):
        query = query_enterpriseGetByAddress(address)
        result = graph.query(query)
        df = DataFrame(result, columns=result.vars)

        df = groupByMaintainer(df)

        return df.to_json(orient='index', indent=2)

    def create(graph, name, lat, long, address, phone, email, website, owner, description, location):
        # Add enterprise to DB
        enterprise = DBEnterprise()
        db.session.add(enterprise)
        db.session.commit()
        
        # Get user_id
        enterpriseID = enterprise.id
        print(owner)
        create_enterpriseRDF(graph, name, owner, lat, long, address, phone, email, website, description, enterpriseID, location)

        graph.serialize(destination=gFile)
        
        return "Enterprise created with ID: " + str(enterpriseID)    

    def update_enterprise(graph, enterpriseID, maintainerID, name, lat, long, address, phone, email, website, description, location):
        # check if enterprise exists
        if not check_enterprise(graph, enterpriseID):
            return "Enterprise does not exist"

        # check if the maintainer is allowed to update the enterprise
        if not (check_maintainer(graph, enterpriseID, maintainerID)):
            return "only maintainer of enterprise can update the enterprise"

        query = query_update_enterpriseRDF(name, lat, long, address, phone, email, website, description, enterpriseID, location)
        graph.update(query)
        graph.serialize(destination=gFile)

        return "update enterprise"

    def delete_enterprise(graph, enterpriseID, ownerID):
        # check if enterprise exists
        if not check_enterprise(graph, enterpriseID):
            return "Enterprise does not exist"

        # check if the owner is allowed to delete the enterprise
        if not (check_owner(graph, enterpriseID, ownerID)):
            return "only owner of enterprise can delete the enterprise"

        # delete enterprise from DB
        enterprise = DBEnterprise().query.get(enterpriseID)

        if not (enterprise is None):
            db.session.delete(enterprise)
            db.session.commit()

        # verwijder al de vacancies van de enterprise
        query = query_getVacanciesOfEnterprise(enterpriseID)
        result = graph.query(query)
        df = DataFrame(result, columns=result.vars)

        for index, row in df.iterrows():
            vacancyURI = row[0]
            graph.remove((vacancyURI, None, None))


        enterpriseURI = URIRef(ENTERPRISE + str(enterpriseID))

        # query = query_delete_enterpriseRDF(enterpriseID)
        # graph.update(query)
        # graph.serialize(destination=gFile)

        # Delete user
        graph.remove((enterpriseURI, None, None))

        graph.serialize(destination=GRAPH_FILE)

        return "delete enterprise"

    def transfer_enterprise(graph, ownerID, enterpriseID, newOwnerID):
        # check if enterprise exists
        if not check_enterprise(graph, enterpriseID):
            return "Enterprise does not exist"

        # check if the owner is allowed to transfer the enterprise
        # check_owner(graph, enterpriseID, ownerID)
        if not (check_owner(graph, enterpriseID, ownerID)):
            return "only owner of enterprise can transfer the enterprise"

        if not (check_person(graph, newOwnerID)):
            return "newOwner is not a person"
        print(enterpriseID, newOwnerID)
                # check_maintainer(graph, enterpriseID, maintainerID)
        if not (check_maintainer(graph, enterpriseID, newOwnerID)):
            return "new owner is not a maintainer of the enterprise"
        
        query = query_transfer_ownershipRDF(enterpriseID, newOwnerID)
        graph.update(query)
        graph.serialize(destination=gFile)  
    
        return "transfer enterprise"

    def add_maintainer(graph, enterpriseID, ownerID, maintainerID):
        # check if enterprise exists
        if not check_enterprise(graph, enterpriseID):
            return "Enterprise does not exist"

        # check if the owner is allowed to transfer the enterprise
        if not (check_owner(graph, enterpriseID, ownerID)):
            return "only owner of enterprise can transfer the enterprise"

        if not (check_person(graph, maintainerID)):
            return "maintainerID is not a person"

        if (check_maintainer(graph, maintainerID, enterpriseID)):
            return "maintainerID is already a maintainer of the enterprise"

        query = query_add_maintainerRDF(enterpriseID, maintainerID)
        graph.update(query)
        graph.serialize(destination=gFile)   
        
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

    def get_onLATLONGLocation(graph, lat, long, radius):
        query = query_enterpriseGetAll()
        result = graph.query(query)
        df = DataFrame(result, columns=result.vars)

        # lat is on position 4 and long on 5, It doesn't want to work with the column names
        # # ?uri ?name ?owner ?maintainer ?lat ?long ?address ?description ?phone ?email ?website ?location
        
        # Filter on distance
        # df = df[(df['lat'] >= lat - radius) & (df['lat'] <= lat + radius) & (df['long'] >= long - radius) & (df['long'] <= long + radius)]
        # df = df[sqrt( (lat - df['lat'])**2 + (long - df["long"])**2 ) <= radius]

        returndf = DataFrame(columns=['uri', 'name', 'owner', 'maintainer', 'lat', 'long', 'address', 'description', 'phone', 'email', 'website', 'location'])
        for i in range(len(df)):
            # get the float value of lat and long
            dflat = df.iloc[i][4].n3()[1:]
            dflat = float(dflat[:dflat.find('"')])
            dflong = df.iloc[i][5].n3()[1:]
            dflong = float(dflong[:dflong.find('"')])

            if (sqrt( (lat - dflat)**2 + (long - dflong)**2 ) <= radius):
                returndf = returndf.append({'uri': df.iloc[i][0], 'name': df.iloc[i][1], 'owner': df.iloc[i][2], 'maintainer': df.iloc[i][3], 'lat': df.iloc[i][4], 'long': df.iloc[i][5], 'address': df.iloc[i][6], 'description': df.iloc[i][7], 'phone': df.iloc[i][8], 'email': df.iloc[i][9], 'website': df.iloc[i][10], 'location': df.iloc[i][11]}, ignore_index=True)

        returndf = groupByMaintainer(returndf)
        return returndf.to_json(orient='index', indent=2)

    def get_onLocation(graph, location):
        query = query_enterpriseGetByLocation(location)
        result = graph.query(query)

        df = DataFrame(result, columns=result.vars)

        df = groupByMaintainer(df)

        return df.to_json(orient='index', indent=2)

    def get_personIsOwner(graph, ownerURI):
        query = query_enterpriseGetByOwner(ownerURI)
        result = graph.query(query)

        if (len(result) == 0):
            return False
        return True


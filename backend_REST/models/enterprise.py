from backend_REST import db
from backend_REST.graph import LOCAL

from rdflib import Literal, RDF, URIRef
from rdflib.namespace import RDF, RDFS, FOAF, XSD

from pandas import DataFrame

from backend_REST.models.database import DBEnterprise


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


    def get_all_enterprises(graph):
        q = f'''
                SELECT ?p
                WHERE {{
                    ?p a enterprise .
                }}
            '''
        result = graph.query(q)
        df = DataFrame(result, columns=result.vars)
        return df.to_json()

    def get_by_id(graph, enterprise_id):
        # TODO : Add other properties
        q = f'''
                SELECT ?p
                WHERE {{
                    {enterprise_id} a enterprise .
                }}
            '''
        result = graph.query(q)
        df = DataFrame(result, columns=result.vars)
        return df.to_json()
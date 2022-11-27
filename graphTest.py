# Create rdf file
from rdflib import Graph, Literal, RDF, URIRef
from rdflib.namespace import FOAF
import owlrl
from pandas import DataFrame

g = Graph()
g.parse("graph.ttl")

query = """
            prefix local: <http://localhost/#>
            SELECT ?userInfo ?diploma ?degree ?profession ?institution ?startDate ?endDate
            where {
                ?userInfo a local:personalInfo .
                ?userInfo local:diploma ?diploma .
                ?diploma local:degree ?degree .
                ?diploma local:profession ?profession .
                ?diploma local:institution ?institution .
                ?diploma local:startDate ?startDate .
                ?diploma local:endDate ?endDate .
            }
        """
        # owlrl.DeductiveClosure(owlrl.OWLRL_Semantics).expand(g)
# owlrl.DeductiveClosure(owlrl.RDFS_Semantics).expand(g)

query2 = """
            prefix local: <http://localhost/#>
            SELECT ?name ?surname
            where {
                ?user a foaf:Person .
                ?user foaf:name ?name .
                ?user local:hasSurName ?surname .
                ?connections local:connections ?user .
                ?connections rdfs:member ?John .
                ?John foaf:name "John" .
            }
        """

result = g.query(query2)
df = DataFrame(result, columns=result.vars)
print(df.to_json(orient='index', indent=2))


g.serialize(destination="outputgraph.ttl")

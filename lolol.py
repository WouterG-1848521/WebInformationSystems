from rdflib import Graph
from rdflib.namespace import FOAF, RDF
from rdflib import Graph, URIRef, Literal, BNode
g = Graph()
g.parse("test.ttl")
g.bind("foaf", FOAF)

bob = URIRef("http://localhost/people/Bo")
linda = BNode()

g.add((bob, RDF.type, FOAF.Person))

q = """
    PREFIX foaf: <http://xmlns.com/foaf/0.1/>

    SELECT ?p
    WHERE {
        ?p a foaf:Person .   
    }
"""

# Apply the query to the graph and iterate through results
for r in g.query(q):
    print(r["p"])


# print(g.serialize(destination="test.ttl"))
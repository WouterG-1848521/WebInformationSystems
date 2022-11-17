from backend_REST import create_app, db
from flask_migrate import Migrate

from backend_REST.models import User

from backend_REST.routes import create_routes


app = create_app('development')

# Create rdf file

from rdflib import Graph, Literal, RDF, URIRef
from rdflib.namespace import FOAF

g = Graph()
g.parse("test.ttl")


# Relations
hasId = URIRef("http://localhost/hasId")

ed = URIRef("http://localhost/people/Bob")
g.add((ed, hasId, Literal(1)))

g.serialize(destination="test.ttl")


#




create_routes(app, g)




migrate = Migrate(app, db)


# Pre-import symbols into a shell context via flask shell 
@app.shell_context_processor
def make_shell_context():
   return dict(db=db, User = User)

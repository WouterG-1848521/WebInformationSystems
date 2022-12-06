from backend_REST import create_app, db
from flask_migrate import Migrate

from backend_REST.models.database import reset_DB
from backend_REST.graph import create_graph

from backend_REST.routes import create_routes
from backend_REST.login import create_login_manager

from rdflib.namespace import FOAF, RDF, OWL
import owlrl


def set_initial_graph_properties(graph):
    # TODO : Add more?
    graph.add((FOAF.knows, RDF.type, OWL.SymmetricProperty))


app = create_app('development')

# Reset DB
# with app.app_context():
#     reset_DB(app)

g = create_graph("graph.ttl")
owlrl.DeductiveClosure(owlrl.RDFS_OWLRL_Semantics, rdfs_closure = True, axiomatic_triples = True, datatype_axioms = True).expand(g)
set_initial_graph_properties(g)
create_login_manager(app)
create_routes(app, g)

migrate = Migrate(app, db)

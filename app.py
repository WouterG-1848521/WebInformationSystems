
from rdflib.namespace import FOAF, RDF, OWL
import owlrl

from backend_REST import create_app, db
from flask_migrate import Migrate

from config import GRAPH_FILE

from backend_REST.models.database import reset_DB
from backend_REST.graph import create_graph

from backend_REST.routes import create_routes
from backend_REST.login import create_login_manager

from backend_REST.initial_data import clear_graph, set_initial_graph_properties, set_initial_graph_data


app = create_app('development')

g = create_graph(GRAPH_FILE)
# owlrl.DeductiveClosure(owlrl.RDFS_OWLRL_Semantics, rdfs_closure=True,
#                        axiomatic_triples=True, datatype_axioms=True).expand(g)

# with app.app_context():
#     # Reload same data
#     reset_DB(app)
#     clear_graph(app, g)
#     set_initial_graph_properties(g)
#     set_initial_graph_data(g)

create_login_manager(app)
create_routes(app, g)

migrate = Migrate(app, db, compare_type=True)

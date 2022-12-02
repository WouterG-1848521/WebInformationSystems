from backend_REST import create_app, db
from flask_migrate import Migrate

from backend_REST.models.database import reset_DB
from backend_REST.graph import create_graph

from backend_REST.routes import create_routes
from backend_REST.login import create_login_manager

app = create_app('development')

#Reset DB
# with app.app_context():
#    reset_DB(app)

g = create_graph("graph.ttl")
create_login_manager(app)
create_routes(app, g)

migrate = Migrate(app, db)

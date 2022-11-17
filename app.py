from backend_REST import create_app, db
from flask_migrate import Migrate

from backend_REST.models import User
from backend_REST.routes import create_routes
from backend_REST.login import create_login_manager


app = create_app('development')

create_routes(app)

create_login_manager(app)

#

#

migrate = Migrate(app, db)


# Pre-import symbols into a shell context via flask shell 
@app.shell_context_processor
def make_shell_context():
   return dict(db=db, User = User)

from backend_REST.routes.login_routes import create_login_routes
from backend_REST.routes.test_routes import create_test_routes
from backend_REST.routes.user_routes import create_user_routes
from backend_REST.routes.enterprise_routes import create_enterprise_routes
from backend_REST.routes.vacancy_routes import create_vacancy_routes
from backend_REST.routes.connection_routes import create_connections_routes
from backend_REST.routes.matching_routes import create_matching_routes
from backend_REST.routes.frontend_routes import create_frontend_routes


def create_routes(app, g):
    create_login_routes(app, g)
    create_test_routes(app, g)
    create_user_routes(app, g)
    create_enterprise_routes(app, g)
    create_vacancy_routes(app, g)
    create_connections_routes(app, g)
    create_matching_routes(app, g)
    create_frontend_routes(app, g)

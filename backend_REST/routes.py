from backend_REST.test_routes import create_test_routes
from backend_REST.user_routes import create_user_routes
from backend_REST.enterprise_routes import create_enterprise_routes
from backend_REST.vacancy_routes import create_vacancy_routes

def create_routes(app, g):
    create_test_routes(app, g)
    create_user_routes(app, g)
    create_enterprise_routes(app, g)
    create_vacancy_routes(app, g)
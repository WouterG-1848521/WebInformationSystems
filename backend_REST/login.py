from flask_login import LoginManager
from backend_REST.models.database import DBUser
from backend_REST import session


def create_login_manager(app):
    login_manager = LoginManager()

    login_manager.init_app(app)

    # User load callback
    @login_manager.user_loader
    def load_user(user_id):
        """Given <user_id>, return the associated User object.

        :param unicode user_id: user_id (int) user to retrieve
        """
        return DBUser.query.get(str(user_id))

    # Unauthorized callback
    @login_manager.unauthorized_handler
    def unauthorized():
        # do stuff
        return "unautherized access"

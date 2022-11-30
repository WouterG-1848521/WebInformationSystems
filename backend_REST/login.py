from flask_login import LoginManager
from backend_REST.models.user import User

def create_login_manager(app):
    login_manager = LoginManager()

    login_manager.init_app(app)

    # User load callback
    @login_manager.user_loader
    def load_user(user_id):
        """Given <user_id>, return the associated User object.

        :param unicode user_id: user_id (int) user to retrieve
        """
        return User.query.get(str(user_id))

    # Unauthorized callback
    @login_manager.unauthorized_handler
    def unauthorized():
        # do stuff
        return "unautherized access"
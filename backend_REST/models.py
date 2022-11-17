from backend_REST import db


class User(db.Model):
    """'LinkedIn' User.

    :param str email: email address of user
    :param str password: encrypted password for the user

    """
    __tablename__ = 'user'


    id = db.Column(db.Int, primary_key=True)
    email = db.Column(db.String)
    password = db.Column(db.String)
    authenticated = db.Column(db.Boolean, default=False)


    def is_active(self):
        """True, as all users are active."""
        return True

    def get_id(self):
        """Return the email address to satisfy Flask-Login's requirements."""
        return self.email

    def is_authenticated(self):
        """Return True if the user is authenticated."""
        return self.authenticated

    def is_anonymous(self):
        """False, as anonymous users aren't supported."""
        return False
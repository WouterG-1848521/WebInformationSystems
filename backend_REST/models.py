from backend_REST import db

def reset_DB(app):
    app.logger.info("Resetting DB...")
    
    # Drop all tables
    db.drop_all()
    
    # Create all tables
    db.create_all()

def setup_DB_DEBUG(app):
    app.logger.info("Setting up DB debug...")
    user = User(email="email", password="password")
    db.session.add(user)
    db.session.commit()


def test_DB_DEBUG(app):
    app.logger.info("Testing DB...")
    user = User.query.filter_by(email='email').first()
    app.logger.info(user.id)
    
def remove_DB_DEBUG(app):
    app.logger.info("Removing DB debug...")
    user = User.query.filter_by(email='email').first()
    db.session.delete(user)
    db.session.commit()
    
    # To delete all: 
    User.query.delete()
    


class User(db.Model):
    """'LinkedIn' User.

    :param str email: email address of user
    :param str password: encrypted password for the user

    """
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100))
    password = db.Column(db.String(30))
    authenticated = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return '<User %r>' % self.email

    def is_active(self):
        """True, as all users are active."""
        return True

    def get_id(self):
        """Return the id to satisfy Flask-Login's requirements."""
        return self.id

    def is_authenticated(self):
        """Return True if the user is authenticated."""
        return self.authenticated

    def is_anonymous(self):
        """False, as anonymous users aren't supported."""
        return False
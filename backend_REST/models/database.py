from backend_REST import db


def reset_DB(app):
    app.logger.info("Resetting DB...")

    # Drop all tables
    db.drop_all()

    # Create all tables
    db.create_all()


class DBUser(db.Model):
    """
    :param str email: email address of user
    :param str password: encrypted password for the user

    """
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100))
    password = db.Column(db.String(128))
    authenticated = db.Column(db.Boolean, default=False)
    isAdmin = db.Column(db.Boolean, default=False)
    getVacancies = db.Column(db.Boolean, default=True)

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


class DBVacancy(db.Model):

    __tablename__ = 'vacancies'

    id = db.Column(db.Integer, primary_key=True)

    def __repr__(self):
        return '<Vacancy %r>' % self.id

    def get_id(self):
        return self.id


class DBEnterprise(db.Model):

    __tablename__ = 'enterprises'

    id = db.Column(db.Integer, primary_key=True)

    def __repr__(self):
        return '<Enterprise %r>' % self.id

    def get_id(self):
        return self.id


class DBDiploma(db.Model):

    __tablename__ = 'diplomas'

    id = db.Column(db.Integer, primary_key=True)

    def __repr__(self):
        return '<Diploma %r>' % self.id

    def get_id(self):
        return self.id


class DBWorkExperience(db.Model):

    __tablename__ = 'experiences'

    id = db.Column(db.Integer, primary_key=True)

    def __repr__(self):
        return '<Experience %r>' % self.id

    def get_id(self):
        return self.id


class DBConnectionRequest(db.Model):

    __tablename__ = 'connection_requests'

    id = db.Column(db.Integer, primary_key=True)
    fromUser = db.Column(db.Integer)
    toUser = db.Column(db.Integer)

    def __repr__(self):
        return '<Connection Request %r>' % self.id

    def get_id(self):
        return self.id

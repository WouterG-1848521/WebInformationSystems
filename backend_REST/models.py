from backend_REST import db


class User(db.Model):
   __tablename__ = 'users'
   id = db.Column(db.Integer, primary_key=True)
   email = db.Column(db.String(64), unique=True, index=True)

   def __repr__(self):
       return f"<User {self.email} >"

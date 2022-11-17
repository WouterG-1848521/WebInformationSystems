import os
from datetime import timedelta

# TODO: Modify to our needs
class Config:
   SQLALCHEMY_TRACK_MODIFICATIONS = False

   @staticmethod
   def init_app(app):
       pass

class DevelopmentConfig(Config):
   DEBUG=True
   SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:admin@localhost:5432/flaskapp'  # <--- insert our DB URI
   # REMEMBER_COOKIE_DURATION = timedelta(seconds=30)       # Time before cookie expires
   # PERMANENT_SESSION_LIFETIME = timedelta(seconds=30)     # Can be linked to cookie duration?

class TestingConfig(Config):
   DEBUG = True
   TESTING = True
   SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:admin@localhost:5432/flaskapp'  # <--- insert our DB URI
   # REMEMBER_COOKIE_DURATION = timedelta(seconds=30)       # Time before cookie expires
   # PERMANENT_SESSION_LIFETIME = timedelta(seconds=30)     # Can be linked to cookie duration?


config = {
   'development': DevelopmentConfig,
   'testing': TestingConfig,
   'default': DevelopmentConfig
}
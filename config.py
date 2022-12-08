import os
from datetime import timedelta

# TODO: Modify to our needs
class Config:
   SQLALCHEMY_TRACK_MODIFICATIONS = False

   @staticmethod
   def init_app(app):
       pass

class DevelopmentConfig(Config):
   DEBUG = True
   SESSION_TYPE = 'filesystem'
   SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:admin@localhost:5432/postgres'  # <--- insert our DB URI

   # SQLALCHEMY_ECHO = True                                 # If set to True SQLAlchemy will log all the statements issued to stderr which can be useful for debugging.
   # REMEMBER_COOKIE_DURATION = timedelta(seconds=30)       # Time before cookie expires
   # PERMANENT_SESSION_LIFETIME = timedelta(seconds=30)     # Can be linked to cookie duration?

class TestingConfig(Config):
   DEBUG = True
   TESTING = True
   SESSION_TYPE = 'filesystem'
   SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:admin@localhost:5432/postgres'  # <--- insert our DB URI
   SQLALCHEMY_ECHO = True                                   # If set to True SQLAlchemy will log all the statements issued to stderr which can be useful for debugging.
   # REMEMBER_COOKIE_DURATION = timedelta(seconds=30)       # Time before cookie expires
   # PERMANENT_SESSION_LIFETIME = timedelta(seconds=30)     # Can be linked to cookie duration?


config = {
   'development': DevelopmentConfig,
   'testing': TestingConfig,
   'default': DevelopmentConfig
}
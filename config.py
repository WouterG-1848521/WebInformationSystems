import os

# TODO: Modify to our needs
class Config:
   SQLALCHEMY_TRACK_MODIFICATIONS = False

   @staticmethod
   def init_app(app):
       pass

class DevelopmentConfig(Config):
   DEBUG=True
   SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:admin@localhost:5432/flaskapp'  # <--- insert our DB URI

class TestingConfig(Config):
   DEBUG = True
   TESTING = True
   SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:admin@localhost:5432/flaskapp'  # <--- insert our DB URI


config = {
   'development': DevelopmentConfig,
   'testing': TestingConfig,
   'default': DevelopmentConfig}
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import config 

# Init DB
db = SQLAlchemy()

def create_app(config_name):
    # Create Flask app
    app = Flask(__name__)

    # Configure Flask app from Config Object
    app.config.from_object(config[config_name])

    # Call initialize app from Config Object
    config[config_name].init_app(app)

    # Connect DB to Flask App
    db.init_app(app)

    return app
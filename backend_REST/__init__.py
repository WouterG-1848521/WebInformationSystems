from flask import Flask, session
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
from config import config 

# Init DB
db = SQLAlchemy()

# Init Sessions
sess = Session()

def create_app(config_name):
    # Create Flask app
    app = Flask(__name__)

    # Configure Flask app from Config Object
    app.config.from_object(config[config_name])
    
    # Config Object won't import right configs -> solution: hardcode? (this doesn't even work...)
    # Working solution: 
    # set FASK_ENV=development
    # set FLASK_DEBUG=1
    app.config['ENV'] = 'development'
    app.config['DEBUG'] = True
    app.config['TESTING'] = True

    # Call initialize app from Config Object
    config[config_name].init_app(app)

    # Connect DB to Flask App
    db.init_app(app)
    
    # Connect Session to Flask app
    sess.init_app(app)

    return app
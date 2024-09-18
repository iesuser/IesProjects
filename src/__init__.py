from flask import Flask
from flask_cors import CORS

from src.config import Config
from src.views import projects_blueprint, geophysical_blueprint, auth_blueprint


BLUEPRINTS = [projects_blueprint, geophysical_blueprint, auth_blueprint]


def create_app():
    app = Flask(__name__)
    CORS(app)
    app.config.from_object(Config)
    
    register_blueprints(app)
    

    return app

def register_blueprints(app):
    for blueprint in BLUEPRINTS:
        app.register_blueprint(blueprint)
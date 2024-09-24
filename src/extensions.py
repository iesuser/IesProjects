from flask_sqlalchemy import SQLAlchemy
from flask_restx import Api
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager

from src.config import Config

db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()
api = Api(
    title='IesProjects',
    version='1.0',
    description='IesProjects API',
    authorizations=Config.AUTHORIZATION,
    doc='/api'
)
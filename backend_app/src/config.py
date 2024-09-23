from dotenv import load_dotenv
import os
from os import path, sep, pardir
from datetime import timedelta

# Load environment variables from a custom path (adjust if necessary)
load_dotenv(dotenv_path='/.env')

class Config(object):
    SECRET_KEY = os.getenv('MY_SECRET_KEY', 'default_secret_key')
    BASE_DIR = path.abspath(path.dirname(__file__) + sep + pardir)

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # MySQL connection URI
    DATABASE_USER = os.getenv('DATABASE_USER', 'default_user')
    DATABASE_PASSWORD = os.getenv('DATABASE_PASSWORD', 'default_password')
    DATABASE_HOST = os.getenv('DATABASE_HOST', 'localhost')
    DATABASE_PORT = os.getenv('DATABASE_PORT', 3306)
    DATABASE_NAME = os.getenv('DATABASE_NAME', 'default_db')

    SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}'

    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'default_jwt_secret_key')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(hours=12)
    AUTHORIZATION = {
        'JsonWebToken': {
            'type': 'apiKey',
            'in': 'header',
            'name': 'Authorization'
        }
    }

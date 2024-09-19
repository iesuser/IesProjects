from dotenv import load_dotenv
import os
from os import path, sep, pardir
from datetime import timedelta


# Load environment variables from a custom path
load_dotenv(dotenv_path='/.env')  # Adjust the path as necessary

class Config(object):
    SECRET_KEY = os.getenv('MY_SECRET_KEY', 'default_secret_key')
    BASE_DIR = path.abspath(path.dirname(__file__) + sep + pardir)

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///' + path.join(BASE_DIR, 'db.sqlite')
    
    MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD', 'default_password')
    # MySQL connection URI
    SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://root:{MYSQL_PASSWORD}@localhost/iesprojects'


    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'default_jwt_secret_key')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(hours=12)
    AUTHORIZATION ={
        'JsonWebToken': {
            'type': 'apiKey',
            'in': 'header',
            'name': 'Authorization'
        }
    }
from dotenv import load_dotenv
import os
from os import path, sep, pardir


# Load environment variables from a custom path
load_dotenv(dotenv_path='/.env')  # Adjust the path as necessary

class Config(object):
    SECRET_KEY = os.getenv('MY_SECRET_KEY', 'default_secret_key')
    BASE_DIR = path.abspath(path.dirname(__file__) + sep + pardir)
'''config'''
import os
from pathlib import Path  # python3 only

from dotenv import load_dotenv

ENV_PATH = Path('.') / '.env'
load_dotenv(dotenv_path=ENV_PATH)


class Config(object):
    '''config'''
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI') or 'sqlite:///' + os.path.join(
        os.path.abspath(os.path.dirname(__file__)), 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv('SECRET_KEY') or 'This is a very strong secret key!'

    PROPAGATE_EXCEPTIONS = True

    SWAGGER_URL = '/api/docs'
    SWAGGER_API_URL = os.getenv('SWAGGER_API_URL') or 'http://127.0.0.1:5000/static/swagger.json'

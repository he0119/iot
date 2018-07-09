'''config'''
import os


class Config(object):
    '''config'''
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(
        os.path.abspath(os.path.dirname(__file__)), 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SWAGGER_URL = '/api/docs'
    SWAGGER_API_URL = 'http://127.0.0.1:5000/static/swagger.json'

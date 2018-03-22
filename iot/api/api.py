'''
RESTful API
'''
from flask import Blueprint
from flask_restful import Api

from iot.api.resources.status import Status
from iot.api.resources.token import Token
from iot.api.resources.history import History

api_bp = Blueprint('api', __name__)
api = Api(api_bp)

api.add_resource(Token, '/token')
api.add_resource(Status, '/status')
api.add_resource(History, '/history')
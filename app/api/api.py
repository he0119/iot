from flask import Blueprint
from flask_restful import Api

from app.api.resources.device import Status
from app.api.resources.token import Token

api_bp = Blueprint('api', __name__)
api = Api(api_bp)

api.add_resource(Token, '/token')
api.add_resource(Status, '/status')

'''
RESTful API
'''
from flask import Blueprint, current_app, jsonify
from flask_restful import Api
from flask_swagger import swagger

from iot.api.resources.history import History
from iot.api.resources.status import Status
from iot.api.resources.token import Token
from iot.api.resources.users import Users

api_bp = Blueprint('api', __name__)
api = Api(api_bp)

@api_bp.route("/swagger.json")
def spec():
    '''swagger'''
    swag = swagger(current_app)
    swag['info']['version'] = "0.1.0"
    swag['info']['title'] = "My API"
    return jsonify(swag)

api.add_resource(Token, '/token')
api.add_resource(Status, '/status')
api.add_resource(History, '/history')
api.add_resource(Users, '/users')

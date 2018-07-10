'''
RESTful API
'''
from flask import Blueprint
from flask_login import logout_user
from flask_restful import Api

from iot.api.resources.devices import Devices
from iot.api.resources.history import History
from iot.api.resources.status import Status
from iot.api.resources.token import Token
from iot.api.resources.users import Users

api_bp = Blueprint('api', __name__)
api = Api(api_bp)

api.add_resource(Token, '/token')
api.add_resource(Status, '/status')
api.add_resource(History, '/history')
api.add_resource(Users, '/users')
api.add_resource(Devices, '/devices')

@api_bp.route('/logout')
def logout():
    logout_user()
    return "logout"

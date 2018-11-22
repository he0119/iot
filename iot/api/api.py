'''
RESTful API&SocketIO
'''
from flask import Blueprint
from flask_restful import Api

from iot.api.resources.devices import Devices
from iot.api.resources.history import History
from iot.api.resources.status import Status
from iot.api.resources.users import Users
from iot.api.resources.refresh import Refresh
from iot.api.resources.login import Login

import iot.api.socketio.device
import iot.api.socketio.website

api_bp = Blueprint('api', __name__)
api = Api(api_bp)

#TODO: Use flask-jwt-extended instead of flask-login(socketio remain unchange)
api.add_resource(Devices, '/devices')
api.add_resource(History, '/history')
api.add_resource(Status, '/status')
api.add_resource(Users, '/users')
api.add_resource(Refresh, '/refresh')
api.add_resource(Login, '/login')

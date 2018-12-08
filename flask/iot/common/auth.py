'''
Auth
'''
import functools
import json

from flask import Response, jsonify
from flask_login import current_user
from flask_socketio import disconnect

from iot import login_manager, jwt
from iot.models.user import User

# From https://flask-socketio.readthedocs.org/en/latest/


def authenticated_only(func):
    @functools.wraps(func)
    def wrapped(*args, **kwargs):
        if not current_user.is_authenticated:
            disconnect()
        else:
            return func(*args, **kwargs)
    return wrapped


@login_manager.request_loader
def load_user_from_request(request):
    auth = request.authorization
    # try to authenticate with username/password
    if auth:
        user = User.query.filter_by(username=auth.username).first()
        if not user or not user.check_password(auth.password):
            return None
        return user
    # finally, return None if there isn't auth
    return None


@login_manager.unauthorized_handler
def unauthorized_handler():
    message = {
        'code': 401,
        'message': 'You have to login with proper credentials'
    }
    return Response(json.dumps(message), 401, {'WWW-Authenticate': 'Basic realm="Login Required"'})


@jwt.user_loader_callback_loader
def jwt_user_loader(username):
    '''
    return user based on username
    '''
    return User.query.filter_by(username=username).first()


# @jwt.user_loader_error_loader
# def jwt_user_loader_error(username):
#     '''
#     return an error when failed to load user
#     '''
#     return jsonify({'code': 400, 'message': f'User({username}: load error!)'}), 400

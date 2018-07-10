'''
Auth
'''
import functools

from flask import Response
from flask_login import current_user
from flask_socketio import disconnect

from iot import login_manager
from iot.models.user import User


## From https://flask-socketio.readthedocs.org/en/latest/
def authenticated_only(f):
    @functools.wraps(f)
    def wrapped(*args, **kwargs):
        if not current_user.is_authenticated:
            disconnect()
        else:
            return f(*args, **kwargs)
    return wrapped

@login_manager.request_loader
def load_user_from_request(request):
    auth = request.authorization
    # try to authenticate with username/password
    if auth:
        user = User.verify_auth_token(auth.username)
        if not user:
            user = User.query.filter_by(username=auth.username).first()
            if not user or not user.check_password(auth.password):
                return None
            return user
    # finally, return None if both methods did not login the user
    return None

@login_manager.unauthorized_handler
def unauthorized_handler():
    return Response(
        'Could not verify your access level for that URL.\n'
        'You have to login with proper credentials', 401,
        {'WWW-Authenticate': 'Basic realm="Login Required"'})

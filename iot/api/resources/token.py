'''
Token Resource
'''
from flask_login import login_required
from flask_login import current_user as login_current_user
from flask_restful import Resource
from flask_jwt_extended import (
    create_access_token, create_refresh_token,
    jwt_refresh_token_required, get_jwt_identity,
    jwt_required)

from flask_jwt_extended import current_user as jwt_current_user


class Token(Resource):
    '''get(login_required): return token'''

    @staticmethod
    @login_required
    def get():
        '''
        Get token
        '''
        ret = {
            'access_token': create_access_token(identity=login_current_user.username),
            'refresh_token': create_refresh_token(identity=login_current_user.username)
        }

        return ret, 200

    @staticmethod
    @jwt_refresh_token_required
    def post():
        ret = {
            'access_token': create_access_token(identity=get_jwt_identity())
        }
        return ret, 200

    @staticmethod
    @jwt_required
    def put():
        print(jwt_current_user)
        return 'ret', 200

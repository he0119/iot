'''
Token Resource
'''
from flask_restful import Resource
from flask_jwt_extended import (
    create_access_token,
    jwt_refresh_token_required, get_jwt_identity)


class Refresh(Resource):
    '''get(login_required): return token'''

    @staticmethod
    @jwt_refresh_token_required
    def get():
        ret = {
            'access_token': create_access_token(identity=get_jwt_identity())
        }
        return ret, 200

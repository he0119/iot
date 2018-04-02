'''
Token Resource
'''
from flask import g
from flask_restful import Resource

from iot.common.auth import auth


class Token(Resource):
    '''get(login_required): return token'''

    @staticmethod
    @auth.login_required
    def get():
        '''get token'''
        token = g.user.generate_auth_token()
        return {'token': token.decode('ascii')}

'''
Token Resource
'''
from flask_login import current_user, login_required
from flask_restful import Resource


class Token(Resource):
    '''get(login_required): return token'''

    @staticmethod
    @login_required
    def get():
        '''
        Get token
        '''
        token = current_user.generate_auth_token()
        return {'token': token.decode('ascii')}

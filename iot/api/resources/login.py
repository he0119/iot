'''
Token Resource
'''
from flask_restful import Resource, reqparse
from flask_jwt_extended import create_access_token, create_refresh_token
from iot.models.user import User

class Login(Resource):
    '''post(username, password): return token'''

    @staticmethod
    def post():
        '''
        Get token
        '''
        parser = reqparse.RequestParser()
        parser.add_argument('username', required=True,
                            help='Name cannot be blank!', location='json')
        parser.add_argument('password', required=True,
                            help='Password cannot be blank!', location='json')
        args = parser.parse_args()

        user = User.query.filter_by(username=args.username).first()
        if not user or not user.check_password(args.password):
            return {'code': 400, 'message': 'Username or password is incorrect'}, 400

        ret = {
            'access_token': create_access_token(identity=args.username),
            'refresh_token': create_refresh_token(identity=args.username)
        }

        return ret, 200

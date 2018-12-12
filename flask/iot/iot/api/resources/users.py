'''
User Resource
'''
from flask_jwt_extended import current_user, jwt_required
from flask_restful import Resource, reqparse

from iot import db
from iot.models.user import User


class Users(Resource):
    '''Users Resource'''
    @staticmethod
    @jwt_required
    def get():
        '''
        Get login user info
        '''
        return {'username': current_user.username,
                'email': current_user.email}

    @staticmethod
    @jwt_required
    def post():
        '''
        Create a new user
        '''
        parser = reqparse.RequestParser()
        parser.add_argument('username', required=True,
                            help='Name cannot be blank!', location='json')
        parser.add_argument('password', required=True,
                            help='Password cannot be blank!', location='json')
        parser.add_argument('email', required=True,
                            help='Email cannot be blank!', location='json')
        args = parser.parse_args()

        if db.session.query(User).filter(User.username == args.username).first():
            return {'code': 400, 'message': 'Username already exist'}, 400

        if db.session.query(User).filter(User.email == args.email).first():
            return {'code': 400, 'message': 'This Email has been used, please change'}, 400

        user = User(username=args.username, email=args.email)
        user.set_password(args.password)
        db.session.add(user)
        db.session.commit()
        return {'username': user.username, 'message': 'Account Created'}, 201

    @staticmethod
    @jwt_required
    def put():
        '''
        Modify user info
        '''
        parser = reqparse.RequestParser()
        parser.add_argument('password', location='json')
        parser.add_argument('email', location='json')
        args = parser.parse_args()

        if args.email:
            if args.email == current_user.email:
                return {'code': 400, 'message': 'You have used this email'}, 400
            if db.session.query(User).filter(User.email == args.email).first():
                return {'code': 400, 'message': 'This Email has been used, please change'}, 400
            current_user.email = args.email
        if args.password:
            current_user.set_password(args.password)
        db.session.add(current_user)
        db.session.commit()
        return {'message': 'User info updated'}, 201

    @staticmethod
    @jwt_required
    def delete():
        '''
        Delete user
        '''
        # Delete all devices before delete user
        current_user.delete_devices()

        db.session.delete(current_user)
        db.session.commit()
        return {'message': f'{current_user.username} deleted'}, 204

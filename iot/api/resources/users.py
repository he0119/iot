'''
User Resource
'''
from flask_login import current_user, login_required
from flask_restful import Resource, reqparse

from iot.common.db import db
from iot.models.user import User


class Users(Resource):
    '''Users Resource'''
    @staticmethod
    @login_required
    def get():
        '''
        Get login user info
        '''
        return {'username' : current_user.username,
                'email' : current_user.email}

    @staticmethod
    @login_required
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
            return {'message': 'Username already exist'}, 400

        if db.session.query(User).filter(User.email == args.email).first():
            return {'message': 'This Email has been used, please change'}, 400

        user = User(username=args.username, email=args.email)
        user.set_password(args.password)
        db.session.add(user)
        db.session.commit()
        return {'username': user.username, 'message': 'Account Created'}, 201

    @staticmethod
    @login_required
    def put():
        '''
        Modify user info
        '''
        parser = reqparse.RequestParser()
        parser.add_argument('password', location='json')
        parser.add_argument('email', location='json')
        args = parser.parse_args()

        user = db.session.query(User).filter(
            User.username == current_user.username).first()
        if args.email:
            if args.email == current_user.email:
                return {'message': 'You have used this email'}, 400
            if db.session.query(User).filter(User.email == args.email).first():
                return {'message': 'This Email has been used, please change'}, 400
            user.email = args.email
        if args.password:
            user.set_password(args.password)
        db.session.add(user)
        db.session.commit()
        return {'message': 'User info updated'}, 201

    @staticmethod
    @login_required
    def delete():
        '''
        Delete user
        '''
        parser = reqparse.RequestParser()
        parser.add_argument('username', required=True, location='json')
        args = parser.parse_args()

        user = db.session.query(User).filter(
            User.username == args.username).first()
        if not user:
            return {'message': f'{args.username} do not exist'}, 400
        db.session.delete(user)
        db.session.commit()
        return {'message': f'{args.username} deleted'}, 204

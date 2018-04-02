'''
User Resource
TODO:
    Change Password
'''

from flask import g
from flask_restful import Resource, reqparse

from iot.common.auth import auth
from iot.common.db import db
from iot.models.user import User


class Users(Resource):
    '''Users Resource'''
    @staticmethod
    @auth.login_required
    def get():
        '''Get login user info'''
        return {'username' : g.user.username,
                'email' : g.user.email}

    @staticmethod
    @auth.login_required
    def post():
        '''Add new user'''
        parser = reqparse.RequestParser()
        parser.add_argument('username', required=True,
                            help='Name cannot be blank!')
        parser.add_argument('password', required=True,
                            help='Password cannot be blank!')
        parser.add_argument('email', required=True,
                            help='Email cannot be blank!')
        args = parser.parse_args()

        if db.session.query(User).filter(User.username == args['username']).first():
            return {'error': 'Username already exist'}, 400

        if db.session.query(User).filter(User.email == args['email']).first():
            return {'error': 'This Email has been used, please change'}, 400

        user = User(username=args['username'], email=args['email'])
        user.set_password(args['password'])
        db.session.add(user)
        db.session.commit()
        return {'username': user.username, 'message': 'Account Created'}, 201

    @staticmethod
    @auth.login_required
    def put():
        '''Modify user info'''
        parser = reqparse.RequestParser()
        parser.add_argument('password')
        parser.add_argument('email')
        args = parser.parse_args()

        user = db.session.query(User).filter(
            User.username == g.user.username).first()
        if args['email']:
            user.email = args['email']
        if args['password']:
            user.set_password(args['password'])
        db.session.add(user)
        db.session.commit()
        return {'message': 'User info update'}

'''
User Resource
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
        '''
        Get login user info
        ---
        tags:
          - users
        responses:
          200:
            description: User info
            schema:
              properties:
                username:
                  type: string
                  description: username for user
                email:
                  type: string
                  description: email for user
            examples:
              application/json:
                username: John
                email: John@example.com
        '''
        return {'username' : g.user.username,
                'email' : g.user.email}

    @staticmethod
    @auth.login_required
    def post():
        '''
        Create a new user
        ---
        tags:
          - users
        parameters:
          - in: body
            name: body
            schema:
              id: User
              required:
                - username
                - password
                - email
              properties:
                username:
                  type: string
                  description: username for user
                password:
                  type: string
                  format: password
                  description: password for user
                email:
                  type: string
                  description: email for user
        responses:
          201:
            description: User created
          400:
            description: Username or Email already exist
        '''
        parser = reqparse.RequestParser()
        parser.add_argument('username', required=True,
                            help='Name cannot be blank!', location='json')
        parser.add_argument('password', required=True,
                            help='Password cannot be blank!', location='json')
        parser.add_argument('email', required=True,
                            help='Email cannot be blank!', location='json')
        args = parser.parse_args()

        if db.session.query(User).filter(User.username == args['username']).first():
            return {'message': 'Username already exist'}, 400

        if db.session.query(User).filter(User.email == args['email']).first():
            return {'message': 'This Email has been used, please change'}, 400

        user = User(username=args['username'], email=args['email'])
        user.set_password(args['password'])
        db.session.add(user)
        db.session.commit()
        return {'username': user.username, 'message': 'Account Created'}, 201

    @staticmethod
    @auth.login_required
    def put():
        '''
        Modify user info
        ---
        tags:
          - users
        parameters:
          - in: body
            name: body
            schema:
              properties:
                password:
                  type: string
                  format: password
                  description: password for user
                email:
                  type: string
                  description: email for user
        responses:
          201:
            description: User info upfated
          400:
            description: Email already exist
        '''
        parser = reqparse.RequestParser()
        parser.add_argument('password', location='json')
        parser.add_argument('email', location='json')
        args = parser.parse_args()

        user = db.session.query(User).filter(
            User.username == g.user.username).first()
        if args['email']:
            if db.session.query(User).filter(User.email == args['email']).first():
                return {'message': 'This Email has been used, please change'}, 400
            user.email = args['email']
        if args['password']:
            user.set_password(args['password'])
        db.session.add(user)
        db.session.commit()
        return {'message': 'User info updated'}, 201

    @staticmethod
    @auth.login_required
    def delete():
        '''
        Delete user
        ---
        tags:
          - users
        parameters:
          - in: body
            name: body
            schema:
              required:
                - username
              properties:
                username:
                  type: string
        responses:
          204:
            description: User deleted
        '''
        parser = reqparse.RequestParser()
        parser.add_argument('username', required=True, location='json')
        args = parser.parse_args()

        user = db.session.query(User).filter(
            User.username == args['username']).first()
        if not user:
            return {'message': '{} do not exist'.format(args['username'])}, 400
        db.session.delete(user)
        db.session.commit()
        return {'message': '{} deleted'.format(user.username)}, 204

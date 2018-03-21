from flask import jsonify, g
from flask_restful import Resource
from app.common.auth import auth

class Token(Resource):
    @auth.login_required
    def get(self):
        token = g.user.generate_auth_token()
        return jsonify({'token': token.decode('ascii')})
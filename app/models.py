'''User, DeviceData'''
from datetime import datetime

from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import BadSignature, SignatureExpired
from werkzeug.security import check_password_hash, generate_password_hash

from app import db, app

class User(db.Model):
    """User Data(id, username, password_hash)"""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def set_password(self, password):
        '''set your password'''
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        '''check your password'''
        return check_password_hash(self.password_hash, password)

    def generate_auth_token(self, expiration=600):
        '''expiration = 600'''
        s = Serializer(app.config['SECRET_KEY'], expires_in = expiration)
        return s.dumps({ 'id': self.id })
    
    @staticmethod
    def verify_auth_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None # valid token, but expired
        except BadSignature:
            return None # invalid token
        user = User.query.get(data['id'])
        return user
        
    def __repr__(self):
        return '<User {}>'.format(self.username)

class DeviceData(db.Model):
    """Device Data(id, time, temperature, relative_humidity, relay1_status, relay2_status)"""
    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.DateTime)
    temperature = db.Column(db.String(32))
    relative_humidity = db.Column(db.String(32))
    relay1_status = db.Column(db.Boolean)
    relay2_status = db.Column(db.Boolean)

    def set_data(self, temperature, relative_humidity, relay1_status, relay2_status, time):
        self.time = time
        self.temperature = temperature
        self.relative_humidity = relative_humidity
        self.relay1_status = relay1_status
        self.relay2_status = relay2_status
        
    def __repr__(self):
        return '<DeviceData {}>'.format(self.time)

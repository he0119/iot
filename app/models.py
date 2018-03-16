from app import db
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime

class User(db.Model):
    """User Data(id, username, password_hash)"""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), index=True)
    password_hash = db.Column(db.String(128))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

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

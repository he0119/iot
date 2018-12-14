"""User Model"""
from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from iot import db


class User(db.Model, UserMixin):
    """User Data(id, username, password_hash)."""
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True, nullable=False)
    email = db.Column(db.String(120), index=True, unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    devices = db.relationship('Device', backref='user', lazy='dynamic')

    def set_password(self, password):
        """Set your password."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Check your password."""
        return check_password_hash(self.password_hash, password)

    def delete_devices(self):
        """Delete all data."""
        for device in self.devices.all():
            device.delete_data()
            db.session.delete(device)
            db.session.commit()

    def __repr__(self):
        return '<User {}>'.format(self.username)

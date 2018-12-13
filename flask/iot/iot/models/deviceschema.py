"""DeviceSchema Model"""
from iot import db


class DeviceSchema(db.Model):
    """Device schema model."""
    __tablename__ = 'deviceschema'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False, unique=True)
    display_name = db.Column(db.String(64))
    data_type = db.Column(db.Integer, nullable=False)
    show = db.Column(db.Boolean, nullable=False)
    allow_control = db.Column(db.Boolean, nullable=False)

    device_id = db.Column(db.Integer, db.ForeignKey('device.id'))

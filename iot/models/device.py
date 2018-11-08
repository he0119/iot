'''
Device Model
'''
from datetime import datetime

from sqlalchemy.sql.expression import and_

from iot import db
from iot.common.utils import datetime2iso
from iot.models.devicedata import DeviceData


class Device(db.Model):
    '''device model'''
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False, unique=True)
    schema = db.Column(db.PickleType, nullable=False)
    display = db.Column(db.PickleType, nullable=False)
    create_on = db.Column(db.DateTime, default=datetime.utcnow())
    last_connect_on = db.Column(db.DateTime)
    offline_on = db.Column(db.DateTime)
    online_status = db.Column(db.Boolean)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    data = db.relationship('DeviceData', backref='device', lazy='dynamic')

    def change_status(self, status):
        '''Change online status'''
        self.online_status = status
        if status:
            self.last_connect_on = datetime.utcnow()
        else:
            self.offline_on = datetime.utcnow()

    def device_info_to_json(self):
        '''Get device info'''
        return {'id': self.id,
                'name': self.name,
                'schema': self.schema,
                'display': self.display,
                'createOn': datetime2iso(self.create_on),
                'lastConnectOn': datetime2iso(self.last_connect_on),
                'offlineOn': datetime2iso(self.offline_on),
                'onlineStatus': self.online_status}

    def latest_data_to_json(self):
        '''Get device's latest data'''
        latest = self.data.order_by(DeviceData.id.desc()).first()
        if latest:
            data = latest.data_to_json()
            return data
        return {'id': self.id,
                'time': None,
                'data': None}

    def history_data(self, start, end):
        '''Get history data'''
        return self.data.filter(
            and_(DeviceData.time >= start, DeviceData.time <= end)).all()

    def delete_data(self):
        '''Delete all data'''
        for device_data in self.data.all():
            db.session.delete(device_data)
            db.session.commit()

    def __repr__(self):
        return '<Device %r>' % self.name

'''
Device and DeviceData Model
'''
from datetime import datetime

from sqlalchemy.sql.expression import and_

from iot import db
from iot.common.utils import datetime2iso


class Device(db.Model):
    '''device model'''
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    schema = db.Column(db.PickleType)
    create_on = db.Column(db.DateTime, default=datetime.utcnow())
    last_connect_on = db.Column(db.DateTime)
    offline_on = db.Column(db.DateTime)
    online_status = db.Column(db.Boolean)
    data = db.relationship('DeviceData', backref='device', lazy='dynamic')

    def change_status(self, status):
        '''Change online status'''
        self.online_status = status
        if status:
            self.last_connect_on = datetime.utcnow()
        else:
            self.offline_on = datetime.utcnow()

    def get_device_info(self):
        '''Get device info'''
        return {'name': self.name,
                'schema': self.schema,
                'createOn': datetime2iso(self.create_on),
                'lastConnectOn': datetime2iso(self.last_connect_on),
                'offlineOn': datetime2iso(self.offline_on),
                'onlineStatus': self.online_status}

    def get_latest_data(self):
        '''Get device's latest data'''
        latest = self.data.order_by(DeviceData.id.desc()).first()
        if latest:
            data = latest.get_data()
            return data
        return {'name': self.name,
                'time': None,
                'data': None}

    def history_data(self, start, end):
        '''Get history data'''
        return self.data.filter(
            and_(DeviceData.time >= start, DeviceData.time <= end)).all()

    def __repr__(self):
        return '<Device %r>' % self.name


class DeviceData(db.Model):
    '''device data model'''
    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.DateTime, index=True)
    data = db.Column(db.String(120))
    device_id = db.Column(db.Integer, db.ForeignKey('device.id'))

    def get_data(self):
        schema = self.device.schema
        raw_data = self.data.split(',')
        converted_data = {'name': self.device.name,
                          'time': datetime2iso(self.time),
                          'data': {}}

        i = 0
        for name in schema:
            if schema[name] == 'int':
                converted_data['data'][name] = int(raw_data[i])
            elif schema[name] == 'float':
                if raw_data[i] == 'Error':
                    converted_data['data'][name] = None
                else:
                    converted_data['data'][name] = float(raw_data[i])
                # TODO: Use more beautiful way
            elif schema[name] == 'boolean':
                converted_data['data'][name] = bool(int(raw_data[i]))
            elif schema[name] == 'string':
                converted_data['data'][name] = str(raw_data[i])
            i += 1
        return converted_data

    def __repr__(self):
        return '<Devicedata {}, Time {}>'.format(self.id, self.time)

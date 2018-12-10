'''
DeviceData Model
'''
from iot import db
from iot.common.utils import datetime2iso

class DeviceData(db.Model):
    '''device data model'''
    __tablename__ = 'devicedata'

    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.DateTime, index=True, nullable=False)
    data = db.Column(db.JSON, nullable=False)

    device_id = db.Column(db.Integer, db.ForeignKey('device.id'))

    def get_data(self):
        '''get formatted data'''
        return {
            'id': self.device_id,
            'time': datetime2iso(self.time),
            'data': self.data,
        }

    def __repr__(self):
        return '<Devicedata {}, Time {}>'.format(self.id, self.time)

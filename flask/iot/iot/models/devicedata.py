"""
DeviceData Model
"""
from iot import db
from iot.common.utils import datetime2iso

class DeviceData(db.Model):
    """DeviceData Model

    it contains three field id(Integer), time(DateTime), data(JSON)
    """
    __tablename__ = 'devicedata'

    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.DateTime, index=True, nullable=False)
    data = db.Column(db.JSON, nullable=False)

    device_id = db.Column(db.Integer, db.ForeignKey('device.id'))

    def json_data(self):
        """Return formatted data with device id and data time.

        example:
        {
            "id": 1,
            "time": "2017-07-14T02:40:10+00:00", //ISO 8601 String
            "data": {
                "temp": 12,
                "valve": true
            }
        }
        """
        return {
            'id': self.device_id,
            'time': datetime2iso(self.time),
            'data': self.data,
        }

    def __repr__(self):
        return '<Devicedata {}, Time {}>'.format(self.id, self.time)

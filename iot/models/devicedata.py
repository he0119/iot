'''
DeviceData Model
'''
from iot import db
from iot.common.utils import datetime2iso, DataType


class DeviceData(db.Model):
    '''device data model'''
    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.DateTime, index=True, nullable=False)
    data = db.Column(db.String(120), nullable=False)
    device_id = db.Column(db.Integer, db.ForeignKey('device.id'), nullable=False)

    def get_data(self):
        schema = self.device.schema
        raw_data = self.data.split(',')
        converted_data = {'name': self.device.name,
                          'time': datetime2iso(self.time),
                          'data': {}}

        i = 0
        for name in schema:
            if DataType(schema[name]) == DataType.integer:
                converted_data['data'][name] = int(raw_data[i])
            elif DataType(schema[name]) == DataType.float:
                if raw_data[i] == 'Error':
                    converted_data['data'][name] = None
                else:
                    converted_data['data'][name] = float(raw_data[i])
                # TODO: Use more beautiful way
            elif DataType(schema[name]) == DataType.boolean:
                converted_data['data'][name] = bool(int(raw_data[i]))
            elif DataType(schema[name]) == DataType.string:
                converted_data['data'][name] = str(raw_data[i])
            i += 1
        return converted_data

    def __repr__(self):
        return '<Devicedata {}, Time {}>'.format(self.id, self.time)

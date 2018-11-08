'''
DeviceData Model
'''
from iot import db
from iot.common.utils import datetime2iso, DeviceDataType


class DeviceData(db.Model):
    '''device data model'''
    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.DateTime, index=True, nullable=False)
    data = db.Column(db.String(120), nullable=False)
    device_id = db.Column(db.Integer, db.ForeignKey('device.id'), nullable=False)

    def data_to_json(self):
        '''Get json type devicedata'''
        schema = self.device.schema
        raw_data = self.data.split(',')
        converted_data = {'id': self.device.id,
                          'time': datetime2iso(self.time),
                          'data': {}}

        i = 0
        for name in schema:
            if DeviceDataType(schema[name]) == DeviceDataType.integer:
                converted_data['data'][name] = int(raw_data[i])
            elif DeviceDataType(schema[name]) == DeviceDataType.float:
                if raw_data[i] == 'Error':
                    converted_data['data'][name] = None
                else:
                    converted_data['data'][name] = float(raw_data[i])
            elif DeviceDataType(schema[name]) == DeviceDataType.boolean:
                converted_data['data'][name] = bool(int(raw_data[i]))
            elif DeviceDataType(schema[name]) == DeviceDataType.string:
                converted_data['data'][name] = str(raw_data[i])
            i += 1
        return converted_data

    def __repr__(self):
        return '<Devicedata {}, Time {}>'.format(self.id, self.time)

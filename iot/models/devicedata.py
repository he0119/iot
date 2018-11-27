'''
DeviceData Model
'''
from iot import db
from iot.common.utils import datetime2iso, DeviceDataType


class DeviceData(db.Model):
    '''device data model'''
    __tablename__ = 'devicedata'

    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.DateTime, index=True, nullable=False)
    data = db.Column(db.String(120), nullable=False)

    device_id = db.Column(db.Integer, db.ForeignKey('device.id'))

    def data_to_json(self):
        '''Get json type devicedata'''
        schema = self.device.schema
        raw_data = self.data.split(',')
        converted_data = {'id': self.device.id,
                          'time': datetime2iso(self.time),
                          'data': {}}
        # print(schema.all())
        i = 0
        for item in schema.all():
            if DeviceDataType(item.data_type) == DeviceDataType.integer:
                converted_data['data'][item.name] = int(raw_data[i])
            elif DeviceDataType(item.data_type) == DeviceDataType.float:
                if raw_data[i] == 'Error':
                    converted_data['data'][item.name] = None
                else:
                    converted_data['data'][item.name] = float(raw_data[i])
            elif DeviceDataType(item.data_type) == DeviceDataType.boolean:
                converted_data['data'][item.name] = bool(int(raw_data[i]))
            elif DeviceDataType(item.data_type) == DeviceDataType.string:
                converted_data['data'][item.name] = str(raw_data[i])
            i += 1
        return converted_data

    def __repr__(self):
        return '<Devicedata {}, Time {}>'.format(self.id, self.time)

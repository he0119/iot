'''
Device Model
'''
from datetime import datetime

from sqlalchemy import func
from sqlalchemy.sql.expression import and_

from iot import db
from iot.common.utils import datetime2iso
from iot.models.devicedata import DeviceData
from iot.models.deviceschema import DeviceSchema
from iot.common.utils import DeviceDataType


class Device(db.Model):
    '''device model'''
    __tablename__ = 'device'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False, unique=True)
    display_name = db.Column(db.String(64))
    create_on = db.Column(db.DateTime, default=datetime.utcnow())
    last_connect_on = db.Column(db.DateTime)
    offline_on = db.Column(db.DateTime)
    online_status = db.Column(db.Boolean)
    data = db.relationship('DeviceData', backref='device', lazy='dynamic')
    schema = db.relationship('DeviceSchema', backref='device', lazy='dynamic')

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def change_status(self, status):
        '''Change online status'''
        self.online_status = status
        if status:
            self.last_connect_on = datetime.utcnow()
        else:
            self.offline_on = datetime.utcnow()

    def schema_to_json(self):
        ''''Get schema'''
        json = []
        for item in self.schema:
            json.append({
                'name': item.name,
                'displayName': item.display_name,
                'dataType': item.data_type,
                'show': item.show,
                'allowControl': item.allow_control
            })
        return json

    def device_info_to_json(self):
        '''Get device info'''
        return {'id': self.id,
                'name': self.name,
                'displayName': self.display_name,
                'schema': self.schema_to_json(),
                'createOn': datetime2iso(self.create_on),
                'lastConnectOn': datetime2iso(self.last_connect_on),
                'offlineOn': datetime2iso(self.offline_on),
                'onlineStatus': self.online_status}

    def latest_data_to_json(self):
        '''Get device's latest data'''
        latest = self.data.order_by(DeviceData.id.desc()).first()
        if latest:
            data = latest.get_data()
            return data
        return {'id': self.id,
                'time': None,
                'data': None}

    def data_to_json(self, data):
        '''Get json type devicedata'''
        schema = self.schema.all()
        raw_data = data.split(',')
        converted_data = {}

        i = 0
        for item in schema:
            if DeviceDataType(item.data_type) == DeviceDataType.integer:
                converted_data[item.name] = int(raw_data[i])
            elif DeviceDataType(item.data_type) == DeviceDataType.float:
                if raw_data[i] == 'Error':
                    converted_data[item.name] = None
                else:
                    converted_data[item.name] = float(raw_data[i])
            elif DeviceDataType(item.data_type) == DeviceDataType.boolean:
                converted_data[item.name] = bool(int(raw_data[i]))
            elif DeviceDataType(item.data_type) == DeviceDataType.string:
                converted_data[item.name] = str(raw_data[i])
            i += 1

        return converted_data

    def history_data(self, start, end, interval):
        '''Get history data'''
        data = self.data.filter(
            and_(DeviceData.time >= start, DeviceData.time <= end))
        number = data.count()
        # Set proper remainder, make the end always to be the latest data
        number = number % interval

        row_number_column = func.row_number().over(
            order_by=DeviceData.id).label('row_number')
        data = data.add_column(row_number_column)
        data = data.from_self().filter(row_number_column % interval == number).all()

        return data

    def set_schema(self, schema):
        '''Set schema'''
        for item in schema:
            new_item = DeviceSchema(
                name=item,
                display_name=schema[item][0],
                data_type=schema[item][1],
                show=schema[item][2],
                allow_control=schema[item][3],
                device=self
            )
            db.session.add(new_item)
            db.session.commit()

    def delete_data(self):
        '''Delete all data'''
        for device_data in self.data.all():
            db.session.delete(device_data)
            db.session.commit()

    def __repr__(self):
        return '<Device %r>' % self.name

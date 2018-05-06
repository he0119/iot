'''
DeviceData Model
'''
from iot.models.device import Device
from iot.common.db import db


class DeviceData(db.Model):
    '''Device Data(id, time, temperature, relative_humidity, relay1_status, relay2_status)'''
    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.DateTime, index=True)
    temperature = db.Column(db.Float)
    relative_humidity = db.Column(db.Float)
    relay1_status = db.Column(db.Boolean)
    relay2_status = db.Column(db.Boolean)

    def set_data(self, data):
        schema = db.session.query(Device).filter(
            Device.name == self.__tablename__).first().schema
        for i in schema:
            setattr(self, i, data[i])

    def __repr__(self):
        return '<DeviceData {}>'.format(self.time)

# class DeviceData(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     def __init__(self, name):
#         self.schema = db.session.query(Device).filter(
#             Device.name == name).first().schema
#         self.__tablename__ = name
#         self.add_flied_from_schema()

#     def set_flied(self, filed, f_type):
#         if f_type == 'int':
#             setattr(self, filed, db.Column(db.Integer))
#         if f_type == 'float':
#             setattr(self, filed, db.Column(db.Float))
#         if f_type == 'bool':
#             setattr(self, filed, db.Column(db.Boolean))
#         if f_type == 'datetime':
#             setattr(self, filed, db.Column(db.DateTime, index=True))

#     def add_flied_from_schema(self):
#         for i in self.schema:
#             self.set_flied(i, self.schema[i])

#     def set_data(self, data):
#         for i in self.schema:
#             setattr(self, i, data[i])


# {"time": "datetime",
#  "temperature": "float",
#  "relative_humidity": "float",
#  "relay1_status": "bool",
#  "relay2_status": "bool"}
# def set_data(self, data):
#     for i in self.schema:
#         setattr(self, i, data[i])

# def get_devicedata_orm(db, name):
#     schema = db.session.query(Device).filter(Device.name == name).first().schema
#     Base = automap_base()
#     Base.prepare(db.engine, reflect=True)
#     DeviceData = Base.classes[name]
#     DeviceData.schema = schema
#     DeviceData.set_data = types.MethodType(set_data, DeviceData)
#     return DeviceData

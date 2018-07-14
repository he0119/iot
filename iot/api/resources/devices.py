'''
Devices Resource
'''
from flask_login import login_required
from flask_restful import Resource, reqparse

from iot import db
from iot.common.utils import datetime2iso
from iot.models.device import Device


class Devices(Resource):
    '''
    Devices Resource

    GET: All devices info

    POST(login_required): Add new device to database

    PUT(login_required): Change device info
    '''

    @staticmethod
    @login_required
    def get():
        '''
        return json data
        ---
        tags:
          - devices
        '''
        # print(db.session.execute('SELECT * FROM user').fetchall())
        # print(Device)
        device_list = []
        devices = db.session.query(Device).all()
        for device in devices:
            device_list.append({'name': device.name,
                                'schema': device.schema,
                                'createOn': datetime2iso(device.create_on),
                                'lastConnectOn': datetime2iso(device.last_connect_on),
                                'offlineOn': datetime2iso(device.offline_on),
                                'onlineStatus': device.online_status})
        return device_list

    @staticmethod
    @login_required
    def post():
        '''
        create device
        ---
        tags:
          - devices
        parameters:
          - in: body
            name: body
            schema:
              required:
                - name
                - schema
              properties:
                name:
                  type: string
                  description: name for device
                schema:
                  type: string
                  description: schema for device
        responses:
          201:
            description: User created
          400:
            description: Username or Email already exist
        '''
        parser = reqparse.RequestParser()
        parser.add_argument('name', required=True, location='json')
        parser.add_argument('schema', type=dict,
                            required=True, location='json')
        args = parser.parse_args()

        if db.session.query(Device).filter(Device.name == args['name']).first():
            return {'message': 'Name already exist'}, 400

        device = Device(name=args['name'], schema=args['schema'])
        db.session.add(device)
        db.session.commit()
        return {'name': device.name, 'message': 'Device Created'}, 201

    @staticmethod
    @login_required
    def put():
        '''
        Modify device info
        ---
        tags:
          - devices
        parameters:
          - in: body
            name: body
            schema:
              properties:
                name:
                  type: string
                  description: name for device
                schema:
                  type: string
                  description: schema for device
        responses:
          201:
            description: Device info upfated
          400:
            description: Device do not exist
        '''
        parser = reqparse.RequestParser()
        parser.add_argument('name', required=True, location='json')
        parser.add_argument('schema', type=dict,
                            required=True, location='json')
        args = parser.parse_args()

        device = db.session.query(Device).filter(
            Device.name == args['name']).first()
        if not device:
            return {'message': '{} do not exist'.format(args['name'])}, 400

        device.schema = args['schema']
        db.session.add(device)
        db.session.commit()
        return {'message': 'Device info updated'}, 201

    @staticmethod
    @login_required
    def delete():
        '''
        Delete device
        ---
        tags:
          - devices
        parameters:
          - in: body
            name: body
            schema:
              required:
                - name
              properties:
                name:
                  type: string
        responses:
          204:
            description: User deleted
        '''
        parser = reqparse.RequestParser()
        parser.add_argument('name', required=True, location='json')
        args = parser.parse_args()

        device = db.session.query(Device).filter(
            Device.name == args['name']).first()
        if not device:
            return {'message': '{} do not exist'.format(args['name'])}, 400
        db.session.delete(device)
        db.session.commit()
        return {}, 204

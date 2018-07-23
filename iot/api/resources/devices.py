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
    def get():
        '''
        Get devices info
        '''
        parser = reqparse.RequestParser()
        parser.add_argument('name')
        args = parser.parse_args()

        if args.name:
            device = db.session.query(Device).filter(
                Device.name == args.name).first()
            if device:
                return device.get_device_info()
            return {'message': 'Device not found'}, 404

        device_list = []
        devices = db.session.query(Device).all()
        for device in devices:
            device_list.append(device.get_device_info())
        return device_list

    @staticmethod
    @login_required
    def post():
        '''
        Create a new device
        '''
        parser = reqparse.RequestParser()
        parser.add_argument('name', required=True, location='json')
        parser.add_argument('schema', type=dict,
                            required=True, location='json')
        args = parser.parse_args()

        if db.session.query(Device).filter(Device.name == args.name).first():
            return {'message': 'Name already exist'}, 400

        device = Device(name=args.name, schema=args.schema)
        db.session.add(device)
        db.session.commit()
        return {'name': device.name, 'message': 'Device created'}, 201

    @staticmethod
    @login_required
    def put():
        '''
        Modify device info
        '''
        parser = reqparse.RequestParser()
        parser.add_argument('name', required=True, location='json')
        parser.add_argument('schema', type=dict,
                            required=True, location='json')
        args = parser.parse_args()

        device = db.session.query(Device).filter(
            Device.name == args.name).first()
        if not device:
            return {'message': f'{args.name} do not exist'}, 400

        device.schema = args.schema
        db.session.add(device)
        db.session.commit()
        return {'message': 'Device info updated'}, 201

    @staticmethod
    @login_required
    def delete():
        '''
        Delete device
        '''
        parser = reqparse.RequestParser()
        parser.add_argument('name', required=True, location='json')
        args = parser.parse_args()

        device = db.session.query(Device).filter(
            Device.name == args.name).first()
        if not device:
            return {'message': f'{args.name} do not exist'}, 404
        db.session.delete(device)
        db.session.commit()
        return {}, 204

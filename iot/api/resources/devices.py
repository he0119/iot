'''
Devices Resource
'''
from flask_jwt_extended import current_user, jwt_required
from flask_restful import Resource, reqparse

from iot import db
from iot.models.device import Device


class Devices(Resource):
    '''
    Devices Resource
    '''

    @staticmethod
    @jwt_required
    def get():
        '''
        Get devices info
        '''
        parser = reqparse.RequestParser()
        parser.add_argument('id', type=int)
        args = parser.parse_args()

        devices = current_user.devices.all()

        if args.id:
            for device in devices:
                if device.id == args.id:
                    return device.device_info_to_json()
            return {'code': 404, 'message': f'Device(id:{args.id}) does not exist'}, 404

        device_list = []
        for device in devices:
            device_list.append(device.device_info_to_json())
        return device_list

    @staticmethod
    @jwt_required
    def post():
        '''
        Create a new device
        '''
        parser = reqparse.RequestParser()
        parser.add_argument('name', required=True, location='json')
        parser.add_argument('display_name', required=True, location='json')
        parser.add_argument('schema', type=dict,
                            required=True, location='json')
        args = parser.parse_args()

        if current_user.devices.all():
            device = [device for device in current_user.devices.all()
                      if device.name == args.name]
            if device:
                return {'code': 400, 'message': 'Name already exist'}, 400

        device = Device(
            name=args.name, display_name=args.display_name, user=current_user)
        db.session.add(device)
        db.session.commit()

        device.set_schema(args.schema)

        return device.device_info_to_json(), 201

    @staticmethod
    @jwt_required
    def put():
        '''
        Modify device info
        '''
        parser = reqparse.RequestParser()
        parser.add_argument('id', required=True, location='json')
        parser.add_argument('name', location='json')
        parser.add_argument('display_name', location='json')
        parser.add_argument('schema', type=dict, location='json')
        args = parser.parse_args()

        device = current_user.devices.filter(
            Device.id == args.id).first()
        if not device:
            return {'code': 404, 'message': f'Device(id:{args.id}) does not exist'}, 404

        if args.name:
            device.name = args.name
        if args.display_name:
            device.display_name = args.display_name
        if args.schema:
            device.schema = args.schema

        db.session.add(device)
        db.session.commit()
        return {'message': 'Device info updated'}, 201

    @staticmethod
    @jwt_required
    def delete():
        '''
        Delete device
        '''
        parser = reqparse.RequestParser()
        parser.add_argument('id', required=True, location='json')
        args = parser.parse_args()

        device = current_user.devices.filter(
            Device.id == args.id).first()
        if not device:
            return {'code': 404, 'message': f'Device(id:{args.id}) do not exist'}, 404

        # Delete all device data before delete device
        device.delete_data()

        db.session.delete(device)
        db.session.commit()
        return {}, 204

'''
Status Resource
'''
from datetime import datetime

from flask_jwt_extended import current_user, jwt_required
from flask_restful import Resource, reqparse

from iot import db, socketio
from iot.models.devicedata import DeviceData


class Status(Resource):
    '''
    Status Resource

    GET: the lastest data

    POST(login_required): add new data to database

    PUT(login_required): change the relay status
    '''

    @staticmethod
    @jwt_required
    def get():
        '''
        Get all user devices latest status
        return a list
        '''
        json_data = []  # empty list
        devices = current_user.devices.all()
        for device in devices:
            json_data.append(device.latest_data_to_json())
        return json_data

    @staticmethod
    @jwt_required
    def put():
        '''
        Change status
        '''
        parser = reqparse.RequestParser()
        parser.add_argument('id', required=True, location='json')
        parser.add_argument('data', type=dict, required=True, location='json')
        args = parser.parse_args()

        device = current_user.devices.filter_by(id=args.id).first()
        if not device:
            return {'code': 404, 'message': 'Device does not exist'}, 404

        payload = {}
        for field in device.schema:
            if field.allow_control:
                if field.name in args.data:
                    payload[field.name] = args.data[field.name]
                else:
                    payload[field.name] = 'null'

        socketio.emit(str(device.id), payload)
        return {'message': 'Change status succeed'}, 201

    @staticmethod
    @jwt_required
    def post():
        '''
        Add data to database
        '''
        parser = reqparse.RequestParser()
        parser.add_argument('id', required=True, location='json')
        parser.add_argument('time', required=True, type=int, location='json')
        parser.add_argument('data', required=True, location='json')
        args = parser.parse_args()

        device = current_user.devices.filter_by(id=args.id).first()
        if not device:
            return {'code': 404, 'message': 'Device does not exist'}, 404

        args.time = datetime.utcfromtimestamp(args.time)

        if not device.data.filter(DeviceData.time == args.time).all():
            new_data = DeviceData(
                time=args.time, data=device.data_to_json(args.data), device=device)
            db.session.add(new_data)
            db.session.commit()
            return {'message': f'Data{args.time} added'}, 201
        return {'code': 409, 'message': 'Data already exist'}, 409

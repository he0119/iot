'''
Status Resource
'''
from datetime import datetime

from flask_login import login_required
from flask_restful import Resource, reqparse

from iot import db, socketio
from iot.models.device import Device, DeviceData


class Status(Resource):
    '''
    Status Resource

    GET: the lastest data

    POST(login_required): add new data to database

    PUT(login_required): change the relay status
    '''

    @staticmethod
    def get():
        '''
        Get device latest status
        '''
        json_data = []  # empty list
        devices = db.session.query(Device).all()
        for device in devices:
            json_data.append(device.get_latest_data())
        return json_data

    @staticmethod
    @login_required
    def put():
        '''
        Change status
        '''
        parser = reqparse.RequestParser()
        parser.add_argument('name', required=True, location='json')
        parser.add_argument('data', type=dict, required=True, location='json')
        args = parser.parse_args()

        device = db.session.query(Device).filter_by(name=args.name).first()
        if not device:
            return {'message': 'Device do not exist'}, 404

        payload = {}
        for field in device.schema:
            if field in args.data:
                payload[field] = args.data[field]
            else:
                payload[field] = "null"

        socketio.emit(args.name, payload)
        return {'message': 'Succeed'}, 201

    @staticmethod
    @login_required
    def post():
        '''
        Add data to database
        '''
        parser = reqparse.RequestParser()
        parser.add_argument('name', required=True, location='json')
        parser.add_argument('time', required=True, type=int, location='json')
        parser.add_argument('data', required=True, location='json')
        args = parser.parse_args()

        device = db.session.query(Device).filter_by(name=args.name).first()
        if not device:
            return {'message': 'Device do not exist'}, 404

        args.time = datetime.utcfromtimestamp(args.time)

        if not device.data.filter(DeviceData.time == args.time).all():
            new_data = DeviceData(
                time=args.time, data=args.data, device=device)
            db.session.add(new_data)
            db.session.commit()
            return {'message': 'Data added'}, 201
        return {'message': 'Data already exist'}, 409

'''
Status Resource
'''
from datetime import datetime

from flask_restful import Resource, reqparse

from iot import socketio
from iot.common.auth import auth
from iot.common.db import db
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
        json_data = [] #empty list
        devices = db.session.query(Device).all()
        for device in devices:
            latest = device.data.order_by(DeviceData.id.desc()).first()
            if latest:
                data = latest.get_data()
                json_data.append(data)
            else:
                json_data.append({'name': device.name,
                                  'data': None})
        return json_data

    @staticmethod
    @auth.login_required
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
            return {'message': 'device do not exist'}, 404

        payload = f'{args.name},'
        for field in device.schema:
            if field in args.data:
                payload = payload + str(args.data[field]) + ','
            else:
                payload = payload + ','
        payload = payload[:-1]
        socketio.emit('control', payload)
        return {'message': 'Succeed'}, 201

    @staticmethod
    @auth.login_required
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
            return {'message': 'device do not exist'}, 404

        args.time = datetime.utcfromtimestamp(args.time)

        if not device.data.filter(DeviceData.time == args.time).all():
            new_data = DeviceData(time=args.time, data=args.data, device=device)
            db.session.add(new_data)
            db.session.commit()
            return {'message': 'data added'}, 201
        return {'message': 'data already exist'}, 409

@socketio.on('message')
def handle_my_custom_event(json):
    print('received json: ' + str(json))

@socketio.on('status')
def handle_data_event(json):
    socketio.emit('control', json['data'])

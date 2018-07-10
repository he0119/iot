'''
Status Resource
'''
from datetime import datetime

from flask_login import login_required
from flask_restful import Resource, reqparse

from iot import socketio
from iot.common.auth import authenticated_only
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
            return {'message': 'device do not exist'}, 404

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
            return {'message': 'device do not exist'}, 404

        args.time = datetime.utcfromtimestamp(args.time)

        if not device.data.filter(DeviceData.time == args.time).all():
            new_data = DeviceData(time=args.time, data=args.data, device=device)
            db.session.add(new_data)
            db.session.commit()
            return {'message': 'data added'}, 201
        return {'message': 'data already exist'}, 409

@socketio.on('device status')
# @authenticated_only
def handle_status_event(msg):
    '''Handle status data from IOT devices'''
    print(f'device status:{msg["data"]}')
    device_data = msg['data'].split('|')
    time, name = device_data[0].split(',')
    data = device_data[1]

    device = db.session.query(Device).filter_by(name=name).first()
    if not device:
        pass
    else:
        time = datetime.utcfromtimestamp(int(time))
        new_data = DeviceData(time=time, data=data, device=device)
        if not device.data.filter(DeviceData.time == time).all():
            db.session.add(new_data)
            db.session.commit()
        socketio.emit('data', new_data.get_data())

@socketio.on('test')
def print_control(msg):
    print(str(msg))

@socketio.on('message')
def message_event(msg):
    print(msg)

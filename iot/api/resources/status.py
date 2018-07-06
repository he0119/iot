'''
Status Resource
'''
from datetime import datetime

from flask import current_app
from flask_restful import Resource, reqparse

from iot.common.auth import auth
from iot.common.db import db
from iot.common.mqtt import mqtt
from iot.common.utils import datetime2iso
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
        return json data(time, temperature, relative_humidity, relay1, relay2)
        ---
        tags:
          - status
        responses:
          200:
            schema:
              id: Status
        '''
        json_data = [] #empty list
        devices = db.session.query(Device).all()
        for device in devices:
            if device.data.all():
                latest = device.data.all()[-1]
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
        chage status
        ---
        tags:
          - status
        parameters:
          - in: body
            name: body
            schema:
              required:
                -id
                -status
              properties:
                id:
                  type: string
                  format: password
                  description: id for relay
                status:
                  type: string
                  description: status for relay
        responses:
          201:
            description: User info upfated
        '''
        parser = reqparse.RequestParser()
        parser.add_argument('status', required=True, location='json')
        parser.add_argument('id', required=True, location='json')
        args = parser.parse_args()

        if args['status'] == '1':
            payload = str(args['id']) + '1'
        else:
            payload = str(args['id']) + '0'

        res = mqtt.publish(current_app.config.get('MQTT_CONTROL_TOPIC'),
                           payload=payload, qos=2, retain=False)
        return {'rc': res}, 201

    @staticmethod
    @auth.login_required
    def post():
        '''
        Add data to database
        ---
        tags:
          - status
        parameters:
          - in: body
            name: body
            schema:
              id: Status
              required:
                - name
                - time
                - data
              properties:
                name:
                  type: string
                  description: device name
                time:
                  type: string
                  description: time
                data:
                  type: string
                  description: data
        responses:
          201:
            description: Data added
          400:
            description: Data already exist
        '''
        parser = reqparse.RequestParser()
        parser.add_argument('name', required=True, location='json')
        parser.add_argument('time', required=True, location='json')
        parser.add_argument('data', required=True, location='json')
        args = parser.parse_args()

        device = db.session.query(Device).filter_by(name=args.name).first()
        if not device:
            return {'message': 'device do not exist'}, 400

        args['time'] = datetime.utcfromtimestamp(int(args['time']))

        if not device.data.filter(DeviceData.time == args['time']).all():
            new_data = DeviceData(time=args['time'], data=args['data'], device=device)
            db.session.add(new_data)
            db.session.commit()
            return {'message': 'data added'}, 201
        return {'message': 'data already exist'}, 400

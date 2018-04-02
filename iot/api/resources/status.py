'''
Status Resource
'''
from datetime import datetime, timezone

from flask import g
from flask_restful import Resource, reqparse

from iot.common.auth import auth
from iot.common.db import db
from iot.common.mqtt import mqtt
from iot.models.device import DeviceData


class Status(Resource):
    '''
    Status Resource

    GET: the lastest data

    POST(login_required): add new data to database

    PUT(login_required): change the relay status
    '''

    @staticmethod
    def get():
        '''return json data(time, temperature, relative_humidity, relay1, relay2)'''
        json_data = {} #empty list
        max_id = db.session.query(DeviceData).with_entities(db.func.max(DeviceData.id)).scalar()
        latest = db.session.query(DeviceData).get(max_id)

        #Set time zone because database don't have timezone info
        utc = latest.time.replace(tzinfo=timezone.utc)

        json_data = {'time': utc.isoformat(),  # Use ISO 8601
                     'temperature': latest.temperature,
                     'relativeHumidity': latest.relative_humidity,
                     'relay1Status': latest.relay1_status,
                     'relay2Status': latest.relay2_status}
        return json_data

    @staticmethod
    @auth.login_required
    def put():
        '''chage status'''
        parser = reqparse.RequestParser()
        parser.add_argument('status', required=True)
        parser.add_argument('id', required=True)
        args = parser.parse_args()

        if args['status'] == 'ON':
            payload = str(args['id']) + '1'
        else:
            payload = str(args['id']) + '0'

        res = mqtt.publish('control', payload=payload, qos=2, retain=False)
        return {'rc': res.rc}, 201

    @staticmethod
    @auth.login_required
    def post():
        '''
        recive json data save it to database
        return message:(succeed or failed)
        '''
        parser = reqparse.RequestParser()
        parser.add_argument('time', required=True)
        parser.add_argument('temperature', type=float, required=True)
        parser.add_argument('relative_humidity', type=float, required=True)
        parser.add_argument('relay1', type=bool, required=True)
        parser.add_argument('relay2', type=bool, required=True)
        parser.add_argument('code', type=int, required=True)
        args = parser.parse_args()

        new_data = DeviceData()
        time = datetime.strptime(args['time'], '%Y-%m-%d %H:%M:%S')
        if args['code'] == 0:
            if not db.session.query(DeviceData.time).filter(
                    DeviceData.time == time).all():
                new_data.set_data(args['temperature'],
                                  args['relative_humidity'],
                                  args['relay1'],
                                  args['relay2'],
                                  time)
                db.session.add(new_data)
                db.session.commit()
                return {'message': 'data added'}, 201
            return {'error': 'data already exist'}, 400
        g.data = args  # if code is not 0, save current status to g.data
        return {'message': 'succeed'}, 201

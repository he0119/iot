'''
Status Resource
'''
from datetime import datetime

from flask import g, jsonify, request
from flask_restful import Resource

from iot.common.auth import auth
from iot.common.db import db
from iot.common.mqtt import mqtt
from iot.models.device import DeviceData

class Status(Resource):
    '''
    Status Resource

    Get: the lastest data

    Post(login_required): add new data to database
    '''

    @staticmethod
    def get():
        '''return json data(time, temperature, relative_humidity, relay1, relay2)'''
        json_data = {} #empty list
        max_id = db.session.query(DeviceData).with_entities(db.func.max(DeviceData.id)).scalar()
        latest = db.session.query(DeviceData).get(max_id)
        json_data = {'time' : latest.time,
                     'temperature': latest.temperature,
                     'relativeHumidity': latest.relative_humidity,
                     'relay1Status': latest.relay1_status,
                     'relay2Status': latest.relay2_status}
        return jsonify(json_data)

    @staticmethod
    @auth.login_required
    def put():
        '''chage status'''
        json_data = request.get_json(force=True)
        if json_data['status'] == 'ON':
            payload = str(json_data['id']) + '1'
        else:
            payload = str(json_data['id']) + '0'

        res = mqtt.publish('control', payload=payload, qos=2, retain=False)
        return jsonify({'rc' : res.rc})

    @staticmethod
    @auth.login_required
    def post():
        '''
        recive json data save it to database
        return message:(succeed or failed)
        '''
        json_data = request.get_json(force=True)
        new_data = DeviceData()
        time = datetime.strptime(json_data['time'], '%Y-%m-%d %H:%M:%S')
        if json_data['code'] == 0:
            if not db.session.query(DeviceData.time).filter(
                    DeviceData.time == time).all():
                new_data.set_data(json_data['temperature'],
                                  json_data['relative_humidity'],
                                  json_data['relay1'],
                                  json_data['relay2'],
                                  time)
                db.session.add(new_data)
                db.session.commit()
                return jsonify({'message': 'succeed'})
            else:
                return jsonify({'message': 'already exist'})
        g.data = json_data #if code is not 0, save current status to g.data
        return jsonify({'message': 'succeed'})

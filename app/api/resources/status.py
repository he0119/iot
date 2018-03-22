'''
Status Resource
'''
from datetime import datetime

from flask import g, jsonify, request
from flask_restful import Resource

from app.common.auth import auth
from app.common.db import db
from app.models.device import DeviceData

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
                     'relative_humidity': latest.relative_humidity,
                     'relay1_status': latest.relay1_status,
                     'relay2_status': latest.relay2_status}
        return jsonify(json_data)

    @staticmethod
    @auth.login_required
    def post():
        '''
        recive json data save it to database
        return message:(succeed or failed)
        '''
        json_data = request.get_json(force=True)
        new_data = DeviceData()
        if json_data['code'] == 0:
            new_data.set_data(json_data['temperature'],
                              json_data['relative_humidity'],
                              json_data['relay1'],
                              json_data['relay2'],
                              datetime.strptime(json_data['time'], '%Y-%m-%d %H:%M:%S'))
            db.session.add(new_data)
            db.session.commit()
            return jsonify({'message': 'succeed'})

        g.data = json_data #if code is not 0, save current status to g.data
        return jsonify({'message': 'succeed'})

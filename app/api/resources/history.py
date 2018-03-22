'''
History Resource
'''
from datetime import datetime, timedelta

from flask import jsonify
from flask_restful import Resource, reqparse
from sqlalchemy.sql.expression import and_

from app.common.db import db
from app.models.device import DeviceData


class History(Resource):
    '''
    get: return history data
    '''
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('start', type=int)
        self.parser.add_argument('end', type=int)
        self.parser.add_argument('interval', type=int)

    def get(self):
        '''Get history data
        Args:
            start, end, interval
        Return:
            history data json list
        '''
        args = self.parser.parse_args()
        json_data = [] #Empty list
        days_start = datetime.fromtimestamp(args['start'])
        days_end = datetime.fromtimestamp(args['end'])
        interval = args['interval']
        history_data = db.session.query(DeviceData).filter(
            and_(DeviceData.time >= days_start, DeviceData.time <= days_end))
        number = interval - (history_data.count() % interval)#初始取值，使最后一个为最新数据
        for status in history_data:
            number += 1
            if number >= interval:
                number = 0
                history = {}
                #'Sat, 24 Feb 2018 02:41:56 GMT'
                data = {'time' : status.time,
                        'temperature': status.temperature,
                        'relative_humidity': status.relative_humidity,
                        'relay1_status': status.relay1_status,
                        'relay2_status': status.relay2_status}

                if data['temperature'] is None or data['relative_humidity'] is None:
                    continue #Skip None
                time = data['time'] + timedelta(hours=8) #UTC+8
                history['time'] = time.strftime('%d-%m-%Y %H:%M:%S') #24-02-2018 02:41:56
                history['temperature'] = data['temperature']
                history['relative_humidity'] = data['relative_humidity']
                json_data.append(history)

        return jsonify(json_data)

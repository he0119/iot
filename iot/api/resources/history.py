'''
History Resource
'''
from datetime import datetime

from flask_restful import Resource, reqparse
from sqlalchemy.sql.expression import and_

from iot.common.db import db
from iot.models.device import Device, DeviceData

class History(Resource):
    '''
    get: return history data
    '''
    @staticmethod
    def get():
        '''
        Get history data
        '''
        parser = reqparse.RequestParser()
        parser.add_argument('name', required=True)
        parser.add_argument('start', type=int, required=True)
        parser.add_argument('end', type=int, required=True)
        parser.add_argument('interval', type=int, required=True)
        args = parser.parse_args()

        device = db.session.query(Device).filter(
            Device.name == args.name).first()
        if not device:
            return {'message': '{} do not exist'.format(args.name)}, 404

        json_data = [] #Empty list
        days_start = datetime.utcfromtimestamp(args.start)
        days_end = datetime.utcfromtimestamp(args.end)
        interval = args.interval

        history_data = device.data.filter(
            and_(DeviceData.time >= days_start, DeviceData.time <= days_end)).all()

        number = interval - (len(history_data) % interval)#初始取值，使最后一个为最新数据
        for status in history_data:
            number += 1
            if number >= interval:
                number = 0
                history = {}
                #'Sat, 24 Feb 2018 02:41:56 GMT'
                data = status.get_data()

                if data['data']['temperature'] == 'Error' or \
                   data['data']['relative_humidity'] == 'Error':
                    continue #Skip None
                history['time'] = data['data']['time'] #24-02-2018 02:41:56
                history['temperature'] = data['data']['temperature']
                history['relative_humidity'] = data['data']['relative_humidity']
                json_data.append(history)

        return {'list': json_data}

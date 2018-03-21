import logging
from datetime import datetime, timedelta

from flask import jsonify
from flask_restful import Resource, reqparse
from sqlalchemy.sql.expression import and_

from app.common.db import db
from app.models.device import DeviceData


class History(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('start', type=int)
        self.parser.add_argument('end', type=int)
        self.parser.add_argument('interval', type=int)

    def get(self):
        args = self.parser.parse_args()
        json_data = [] #初始数组
        try:
            days_start = datetime.fromtimestamp(args["start"])
            days_end = datetime.fromtimestamp(args["end"])
            interval = args["interval"]
            q = db.session.query(DeviceData).filter(and_(DeviceData.time >= days_start, DeviceData.time <= days_end))
            number = interval - (q.count() % interval)#初始取值，使最后一个为最新数据
            for u in q:
                number += 1
                if number >= interval:
                    number = 0
                    history = {}
                    #"Sat, 24 Feb 2018 02:41:56 GMT"
                    data = {"time" : u.time,
                            "temperature": u.temperature,
                            "relative_humidity": u.relative_humidity,
                            "relay1_status": u.relay1_status,
                            "relay2_status": u.relay2_status}

                    if data["temperature"] == None or data["relative_humidity"] == None:
                        continue #跳过错误数据
                    time = data["time"] + timedelta(hours = 8) #UTC+8
                    history["time"] = time.strftime("%d-%m-%Y %H:%M:%S") #24-02-2018 02:41:56
                    history["temperature"] = data["temperature"]
                    history["relative_humidity"] = data["relative_humidity"]
                    json_data.append(history)
        except Exception as e:
            logging.exception(e)
        
        return jsonify(json_data)

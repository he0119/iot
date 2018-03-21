import logging
from datetime import datetime

from flask import g, jsonify, request
from flask_restful import Resource

from app.common.auth import auth
from app.common.db import db
from app.models.device import DeviceData

class Status(Resource):  
    def get(self):
        json_data = {} #初始数组
        try:
            max_id = db.session.query(DeviceData).with_entities(
                db.func.max(DeviceData.id)).scalar()
            latest = db.session.query(DeviceData).get(max_id)
            json_data = {"time" : latest.time,
                         "temperature": latest.temperature,
                         "relative_humidity": latest.relative_humidity,
                         "relay1_status": latest.relay1_status,
                         "relay2_status": latest.relay2_status}
        except Exception as e:
            logging.exception(e)
        finally:
            db.session.remove()
        return jsonify(json_data)

    @auth.login_required
    def post(self):
        json_data = request.get_json(force=True)
        new_data = DeviceData()
        if json_data['code'] == 0:
            new_data.set_data(json_data['temperature'],
                              json_data['relative_humidity'],
                              json_data['relay1'],
                              json_data['relay2'],
                              datetime.strptime(json_data['time'], "%Y-%m-%d %H:%M:%S"))
        else:
            g.data = json_data #如果是直接请求获取设备状态，则把数据保存在data中
        try:
            db.session.add(new_data)
            db.session.commit()
            return jsonify({ "message": "succeed" })
        except Exception as e:
            logging.exception(e)
        return jsonify({ "message": "failed" })

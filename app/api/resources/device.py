import logging
from datetime import datetime, timedelta

from flask import jsonify
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
            u = db.session.query(DeviceData).get(max_id)
            json_data = {"time" : u.time,
                    "temperature": u.temperature,
                    "relative_humidity": u.relative_humidity,
                    "relay1_status": u.relay1_status,
                    "relay2_status": u.relay2_status}
        except Exception as e:
            logging.exception(e)
        finally:
            db.session.remove() 
        return jsonify(json_data)
    
    # @auth.login_required
    # def post(self):
    #     device_data = request.data.decode().split(",")
    #     u = DeviceData()
    #     if device_data[0] == "0":
    #         u.set_data(device_data[1],
    #                 device_data[2],
    #                 True if device_data[3] == "ON" else False,
    #                 True if device_data[4] == "ON" else False,
    #                 datetime.strptime(device_data[5], "%Y-%m-%d %H:%M:%S"))
    #     else:
    #         g.data = device_data #如果是直接请求获取设备状态，则把数据保存在data中
    #     try:
    #         db.session.add(u)
    #         db.session.commit()
    #         return jsonify({ "status": "succeed" })
    #     except Exception as e:
    #         logging.exception(e)
    #     finally:
    #         db.session.remove()
    #     return jsonify({ "status": "failed" })

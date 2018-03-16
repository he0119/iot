import logging
import os
from datetime import datetime, timedelta

from flask import (abort, flash, g, jsonify, make_response, redirect,
                   render_template, request, send_from_directory, url_for)
from flask_httpauth import HTTPBasicAuth
from sqlalchemy.sql.expression import and_

from app import app, db
from app.models import DeviceData, User

auth = HTTPBasicAuth()
@auth.verify_password
def verify_password(username, password):
    user = User.query.filter_by(username = username).first()
    if not user or not user.check_password(password):
        return False
    g.user = user
    return True

@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html")

@app.route('/history')
def history():
    return render_template("history.html")

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/api/status', methods=['POST'])
@auth.login_required
def set_data():
    device_data = request.data.decode().split(",")
    u = DeviceData()
    if device_data[0] == "0":
        u.set_data(device_data[1], device_data[2], True if device_data[3]
               == "ON" else False, True if device_data[4] == "ON" else False, datetime.strptime(device_data[5], "%Y-%m-%d %H:%M:%S"))
    else:
        g.data = device_data #如果是直接请求获取设备状态，则把数据保存在data中
    try:
        db.session.add(u)
        db.session.commit()
        return jsonify({ "status": "succeed" })
    except Exception as e:
        logging.exception(e)
    finally:
        db.session.remove()
    return jsonify({ "status": "failed" })

@app.route('/api/status', methods=['GET'])
def status():
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

@app.route('/api/history/<int:days_start>:<int:days_end>:<int:interval>')
def history_data(days_start, days_end, interval):
    json_data = [] #初始数组
    try:
        days_start = datetime.fromtimestamp(days_start)
        days_end = datetime.fromtimestamp(days_end)
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

                if data["temperature"] == "Error" or data["relative_humidity"] == "Error":
                    continue #跳过错误数据
                time = data["time"] + timedelta(hours = 8) #UTC+8
                history["time"] = time.strftime("%d-%m-%Y %H:%M:%S") #24-02-2018 02:41:56
                history["temperature"] = float(data["temperature"])
                history["relative_humidity"] = float(data["relative_humidity"])
                json_data.append(history)
    except Exception as e:
        logging.exception(e)
    finally:
        db.session.remove()
    
    return jsonify(json_data)

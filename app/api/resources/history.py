from flask_restful import Resource
from sqlalchemy.sql.expression import and_

# class History(Resource):
#     def get(self, days_start, days_end, interval):
#         json_data = [] #初始数组
#         try:
#             days_start = datetime.fromtimestamp(days_start)
#             days_end = datetime.fromtimestamp(days_end)
#             q = db.session.query(DeviceData).filter(and_(DeviceData.time >= days_start, DeviceData.time <= days_end))
#             number = interval - (q.count() % interval)#初始取值，使最后一个为最新数据
#             for u in q:
#                 number += 1
#                 if number >= interval:
#                     number = 0
#                     history = {}
#                     #"Sat, 24 Feb 2018 02:41:56 GMT"
#                     data = {"time" : u.time,
#                             "temperature": u.temperature,
#                             "relative_humidity": u.relative_humidity,
#                             "relay1_status": u.relay1_status,
#                             "relay2_status": u.relay2_status}

#                     if data["temperature"] == "Error" or data["relative_humidity"] == "Error":
#                         continue #跳过错误数据
#                     time = data["time"] + timedelta(hours = 8) #UTC+8
#                     history["time"] = time.strftime("%d-%m-%Y %H:%M:%S") #24-02-2018 02:41:56
#                     history["temperature"] = float(data["temperature"])
#                     history["relative_humidity"] = float(data["relative_humidity"])
#                     json_data.append(history)
#         except Exception as e:
#             logging.exception(e)
#         finally:
#             db.session.remove()
        
#         return jsonify(json_data)


# @app.route('/api/history/<int:days_start>:<int:days_end>:<int:interval>')

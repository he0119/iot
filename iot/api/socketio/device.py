'''
Deivce
'''
from datetime import datetime

from flask_login import current_user

from iot import db, socketio
from iot.common.auth import authenticated_only
from iot.models.devicedata import DeviceData


@socketio.on('device status')
@authenticated_only
def handle_status_event(msg):
    '''Handle status data from IOT devices'''
    print(f'device data: {msg["data"]}')
    device_data = msg['data'].split('|')
    time, device_id = device_data[0].split(',')
    data = device_data[1]

    device = current_user.devices.filter_by(id=device_id).first()
    if not device:
        pass
    elif int(time) > 1500000000:  # 确认时间是正确的(2017/7/14 10:40:0)
        time = datetime.utcfromtimestamp(int(time))
        new_data = DeviceData(time=time, data=data, device=device)
        if len(device.data.filter(DeviceData.time == time).all()) < 2:
            db.session.add(new_data)
            db.session.commit()
        socketio.emit('status', new_data.get_data())

'''
Deivce
'''
from datetime import datetime

from iot import db, socketio
from iot.common.auth import authenticated_only
from iot.models.device import Device, DeviceData


@socketio.on('device status')
@authenticated_only
def handle_status_event(msg):
    '''Handle status data from IOT devices'''
    print(f'device status:{msg["data"]}')
    device_data = msg['data'].split('|')
    time, name = device_data[0].split(',')
    data = device_data[1]

    device = db.session.query(Device).filter_by(name=name).first()
    if not device:
        pass
    elif int(time) > 1500000000:  # 确认时间是正确的(2017/7/14 10:40:0)
        time = datetime.utcfromtimestamp(int(time))
        new_data = DeviceData(time=time, data=data, device=device)
        if len(device.data.filter(DeviceData.time == time).all()) < 2:
            db.session.add(new_data)
            db.session.commit()
        socketio.emit('status', new_data.get_data())
'''
website
'''
from iot import socketio
from iot.common.auth import authenticated_only
from iot.common.db import db
from iot.models.device import Device, DeviceData


@socketio.on('website')
def handle_website_event(msg):
    '''Handle request from website'''
    if msg['type'] == 'request':
        devices = db.session.query(Device).all()
        for device in devices:
            latest = device.data.order_by(DeviceData.id.desc()).first()
            if latest:
                data = latest.get_data()
                socketio.emit('status', data)
            else:
                socketio.emit('status', {'name': device.name,
                                         'data': None})

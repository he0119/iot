'''
website
'''
from iot import socketio
from iot.common.auth import authenticated_only
from iot.common.db import db
from iot.models.device import Device


@socketio.on('website')
def handle_website_event(msg):
    '''Handle request from website'''
    if msg['type'] == 'request':
        devices = db.session.query(Device).all()
        for device in devices:
            socketio.emit('status', device.get_latest_data())

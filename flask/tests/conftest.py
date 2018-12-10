'''pytest config'''
import os
from datetime import datetime

import pytest
from flask_jwt_extended import create_access_token, create_refresh_token

from iot.models.device import Device
from iot.models.devicedata import DeviceData
from iot.models.user import User
from run import app, db, socketio
from tests.utils.http import AuthType, MyHttpClient


@pytest.fixture
def client():
    app.config['TESTING'] = True
    # app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(
        # os.path.abspath(os.path.dirname(__file__)), 'test.db')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://test:Test12345678!@localhost/iot_test'

    http_client = app.test_client()
    socketio_client = socketio.test_client(app)

    with app.app_context():
        db.create_all()

        # Add test user
        user = User(username='test', email='test@test.com')
        user.set_password('test')
        db.session.add(user)
        db.session.commit()

        # Add test device
        device = Device(
            name='test', display_name='test', user=user)
        db.session.add(device)
        db.session.commit()

        schema = {
            'test1': ['test1', 2, 1, 0],
            'test2': ['test2', 2, 1, 0],
            'control': ['control', 3, 1, 1],
        }
        device.set_schema(schema)

        # Add test data
        new_data = DeviceData(
            time=datetime.utcfromtimestamp(1500000000), data='10, 12, 0', device=device)
        db.session.add(new_data)
        db.session.commit()

        # Get token
        access_token = create_access_token(
            identity='test')
        refresh_token = create_refresh_token(
            identity='test')

        my_client = MyHttpClient(http_client, socketio_client,
                                 access_token, refresh_token, default_auth=AuthType.access)

    yield my_client

    with app.app_context():
        db.session.remove()
        db.drop_all()

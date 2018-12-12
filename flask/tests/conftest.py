'''pytest config'''
from datetime import datetime

import pytest
from flask_jwt_extended import create_access_token, create_refresh_token

from iot.models.device import Device
from iot.models.devicedata import DeviceData
from iot.models.user import User
from run import app, db, socketio
from tests.utils.http import AuthType, MyTestClient


@pytest.fixture
def client():
    '''My custom test client'''
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
    # app.config['SQLALCHEMY_DATABASE_URI'] = \
    #     'mysql+mysqlconnector://test:Test12345678!@localhost/iot_test'

    http_client = app.test_client()
    socketio_client = socketio.test_client(
        app, headers={'Authorization': 'Basic dGVzdDp0ZXN0'})

    with app.app_context():
        db.drop_all()
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
            time=datetime.utcfromtimestamp(1500000000),
            data={
                'test1': 10.0,
                'test2': 12.0,
                'control': False,
            },
            device=device)
        db.session.add(new_data)
        db.session.commit()

        # Get token
        access_token = create_access_token(
            identity='test')
        refresh_token = create_refresh_token(
            identity='test')

        my_client = MyTestClient(http_client, socketio_client,
                                 access_token, refresh_token, default_auth=AuthType.access)

    yield my_client

    with app.app_context():
        db.session.remove()
        db.drop_all()

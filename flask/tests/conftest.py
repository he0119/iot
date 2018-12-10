'''pytest config'''
import pytest
from flask_jwt_extended import create_access_token, create_refresh_token

from iot.models.user import User
from iot.models.device import Device
from run import app, db
from tests.utils.http import MyHttpClient

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
    client = app.test_client()


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
            "test1": ["test1", 2, 1, 0],
            "test2": ["test2", 2, 1, 0]
        }
        device.set_schema(schema)

        # Get token
        access_token = create_access_token(
            identity='test')
        refresh_token = create_refresh_token(
            identity='test')

        client = MyHttpClient(client, access_token, refresh_token, default_auth='access')

    yield client

    with app.app_context():
        db.drop_all()

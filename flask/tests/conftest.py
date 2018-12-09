'''pytest config'''
import pytest
from flask_jwt_extended import create_access_token, create_refresh_token

from iot.models.user import User
from run import app, db


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

        # Get token
        client.environ_base['ACCESS_TOKEN'] = create_access_token(identity='test')
        client.environ_base['REFRESH_TOKEN'] = create_refresh_token(identity='test')

    yield client

    with app.app_context():
        db.drop_all()

'''pytest config'''
import pytest

from run import app, db
from iot.models.user import User

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
    client = app.test_client()

    with app.app_context():
        db.create_all()
        user = User(username='test', email='test@test.com')
        user.set_password('test')
        db.session.add(user)
        db.session.commit()

    yield client

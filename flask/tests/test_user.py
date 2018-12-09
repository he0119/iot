'''Test user login'''
import json


def test_login(client):
    """test login to get token"""

    res = client.post('/api/login', data=json.dumps(
        {'username': 'test', 'password': 'test'}), headers={'content-type': 'application/json'})

    assert res.json['access_token'] is not None
    assert res.json['refresh_token'] is not None

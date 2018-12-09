'''Test JWT Token'''
import json


def test_login_to_get_token(client):
    '''test login to get token'''

    res = client.post(
        '/api/login',
        data=json.dumps(
            {'username': 'test', 'password': 'test'}),
        headers={'content-type': 'application/json'})

    assert res.status_code == 200
    assert res.json['access_token'] is not None
    assert res.json['refresh_token'] is not None


def test_refresh_token(client):
    '''test refresh token'''
    refresh_token = client.environ_base['REFRESH_TOKEN']

    res = client.get(
        '/api/refresh',
        headers={'Authorization': f'Bearer {refresh_token}'})

    assert res.status_code == 200
    assert res.json['access_token'] is not None

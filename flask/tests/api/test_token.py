'''Test JWT Token'''


def test_login_to_get_token(client):
    '''test login to get token'''
    client.set_auth(None)

    res = client.post(
        '/api/login',
        data={'username': 'test', 'password': 'test'})

    assert res.status_code == 200
    assert res.json['access_token'] is not None
    assert res.json['refresh_token'] is not None


def test_refresh_token(client):
    '''test refresh token'''
    client.set_auth('refresh')

    res = client.get('/api/refresh')

    assert res.status_code == 200
    assert res.json['access_token'] is not None

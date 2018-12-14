"""Test JWT Token"""
from tests.utils.client import TokenType


def test_login_to_get_token(client):
    """Test login to get token."""
    client.set_auth(TokenType.empty)

    res = client.post(
        '/api/login',
        data={'username': 'test', 'password': 'test'})

    assert res.status_code == 200
    assert res.json['access_token'] is not None
    assert res.json['refresh_token'] is not None


def test_login_with_wrong_password(client):
    """Test login with incorrect password."""
    client.set_auth(TokenType.empty)

    res = client.post(
        '/api/login',
        data={'username': 'test', 'password': '123123'})

    assert res.status_code == 401
    assert 'access_token' not in res.json
    assert 'refresh_token' not in res.json
    assert res.json['message'] == 'Username or password is incorrect'


def test_refresh_token(client):
    """Test refresh token."""
    client.set_auth(TokenType.refresh)

    res = client.get('/api/refresh')

    assert res.status_code == 200
    assert res.json['access_token'] is not None

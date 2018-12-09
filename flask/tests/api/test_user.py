'''Test User API'''
import json

API_URL = '/api/users'

def test_get_username(client):
    '''get user info'''
    access_token = client.environ_base['ACCESS_TOKEN']
    res = client.get(
        API_URL,
        headers={'Authorization': f'Bearer {access_token}'})

    assert res.json['username'] == 'test'
    assert res.json['email'] == 'test@test.com'


def test_create_user(client):
    '''create new user'''
    access_token = client.environ_base['ACCESS_TOKEN']
    res = client.post(
        API_URL,
        data=json.dumps(
            {'username': 'test1', 'password': 'test1', 'email': 'test1@test.com'}),
        headers={'Authorization': f'Bearer {access_token}', 'content-type': 'application/json'})

    assert res.status_code == 201
    assert res.json['username'] == 'test1'
    assert res.json['message'] == 'Account Created'


def test_modify_user(client):
    '''modify user info'''
    access_token = client.environ_base['ACCESS_TOKEN']
    res = client.put(
        API_URL,
        data=json.dumps(
            {'email': 'test1@test.com'}),
        headers={'Authorization': f'Bearer {access_token}', 'content-type': 'application/json'})

    assert res.status_code == 201

    res = client.get(
        API_URL,
        headers={'Authorization': f'Bearer {access_token}'})

    assert res.json['email'] == 'test1@test.com'


def test_delete_user(client):
    '''delete current user'''
    access_token = client.environ_base['ACCESS_TOKEN']
    res = client.delete(
        API_URL,
        headers={'Authorization': f'Bearer {access_token}', 'content-type': 'application/json'})

    assert res.status_code == 204

'''Test User API'''
import json


def test_get_username(client):
    ''''''
    access_token = client.environ_base['ACCESS_TOKEN']
    res = client.get(
        '/api/users', headers={'Authorization': f'Bearer {access_token}'})

    assert res.json['username'] == 'test'
    assert res.json['email'] == 'test@test.com'


def test_create_user(client):
    ''''''
    access_token = client.environ_base['ACCESS_TOKEN']
    res = client.post(
        '/api/users',
        data=json.dumps(
            {'username': 'test1', 'password': 'test1', 'email': 'test1@test.com'}),
        headers={'Authorization': f'Bearer {access_token}', 'content-type': 'application/json'})

    assert res.status_code == 201
    assert res.json['username'] == 'test1'
    assert res.json['message'] == 'Account Created'


def test_modify_user(client):
    ''''''
    access_token = client.environ_base['ACCESS_TOKEN']
    res = client.put(
        '/api/users',
        data=json.dumps(
            {'email': 'test1@test.com'}),
        headers={'Authorization': f'Bearer {access_token}', 'content-type': 'application/json'})

    assert res.status_code == 201

    res = client.get(
        '/api/users', headers={'Authorization': f'Bearer {access_token}'})

    assert res.json['email'] == 'test1@test.com'


def test_delete_user(client):
    ''''''
    access_token = client.environ_base['ACCESS_TOKEN']
    res = client.delete(
        '/api/users',
        headers={'Authorization': f'Bearer {access_token}', 'content-type': 'application/json'})

    assert res.status_code == 204

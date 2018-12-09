'''Test Device API'''
import json

API_URL = '/api/devices'


def test_get_device(client):
    '''get device info'''
    access_token = client.environ_base['ACCESS_TOKEN']
    res = client.get(
        API_URL,
        headers={'Authorization': f'Bearer {access_token}'})

    assert res.status_code == 200
    assert res.json[0]['id'] == 1
    assert res.json[0]['name'] == 'test'
    assert res.json[0]['displayName'] == 'test'
    assert res.json[0]['schema'][0] == {
        'name': 'test1',
        'displayName': 'test1',
        'dataType': 2,
        'show': True,
        'allowControl': False
    }

    res = client.get(
        f'{API_URL}?id=1',
        headers={'Authorization': f'Bearer {access_token}'})

    assert res.status_code == 200
    assert res.json['id'] == 1
    assert res.json['name'] == 'test'
    assert res.json['displayName'] == 'test'
    assert res.json['schema'][0] == {
        'name': 'test1',
        'displayName': 'test1',
        'dataType': 2,
        'show': True,
        'allowControl': False
    }

    res = client.get(
        f'{API_URL}?id=10',
        headers={'Authorization': f'Bearer {access_token}'})

    assert res.status_code == 404


def test_create_device(client):
    '''create new device'''
    access_token = client.environ_base['ACCESS_TOKEN']
    data = {
        "name": "test1",
        "display_name": "test1",
        "schema": {
            "test11": ["test11", 1, 1, 0],
            "test22": ["test22", 1, 1, 0],
        }
    }
    res = client.post(
        API_URL,
        data=json.dumps(data),
        headers={'Authorization': f'Bearer {access_token}', 'content-type': 'application/json'})

    assert res.status_code == 201
    assert res.json['id'] == 2
    assert res.json['name'] == 'test1'
    assert res.json['displayName'] == 'test1'
    assert res.json['schema'][0] == {
        'name': 'test11',
        'displayName': 'test11',
        'dataType': 1,
        'show': True,
        'allowControl': False
    }


def test_modify_device(client):
    '''modify device info'''
    access_token = client.environ_base['ACCESS_TOKEN']
    data = {
        'id': 1,
        'name': 'testtt',
        'display_name': 'testtt'
    }
    res = client.put(
        API_URL,
        data=json.dumps(data),
        headers={'Authorization': f'Bearer {access_token}', 'content-type': 'application/json'})

    assert res.status_code == 201

    res = client.get(
        f'{API_URL}?id=1',
        headers={'Authorization': f'Bearer {access_token}'})

    assert res.status_code == 200
    assert res.json['id'] == 1
    assert res.json['name'] == 'testtt'
    assert res.json['displayName'] == 'testtt'


def test_delete_device(client):
    '''delete current user'''
    access_token = client.environ_base['ACCESS_TOKEN']
    res = client.delete(
        API_URL,
        data=json.dumps({'id': 1}),
        headers={'Authorization': f'Bearer {access_token}', 'content-type': 'application/json'})

    assert res.status_code == 204

    res = client.delete(
        API_URL,
        data=json.dumps({'id': 1}),
        headers={'Authorization': f'Bearer {access_token}', 'content-type': 'application/json'})

    assert res.status_code == 404

"""Test Device API"""
API_URL = '/api/devices'


def test_get_device(client):
    """Get device info."""
    res = client.get(API_URL)

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

    res = client.get(f'{API_URL}?id=1')

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

    res = client.get(f'{API_URL}?id=10')

    assert res.status_code == 404


def test_create_device(client):
    """Create new device."""
    data = {
        "name": "test1",
        "display_name": "test1",
        "schema": {
            "test11": ["test11", 1, 1, 0],
            "test22": ["test22", 1, 1, 0],
        }
    }
    res = client.post(API_URL, data=data)

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
    """Modify device info."""
    data = {
        'id': 1,
        'name': 'testt',
        'display_name': 'testtt'
    }
    res = client.put(API_URL, data=data)

    assert res.status_code == 201

    res = client.get(f'{API_URL}?id=1')

    assert res.status_code == 200
    assert res.json['id'] == 1
    assert res.json['name'] == 'testt'
    assert res.json['displayName'] == 'testtt'


def test_delete_device(client):
    """Delete current user."""
    res = client.delete(
        API_URL,
        data={'id': 1})

    assert res.status_code == 204

    res = client.delete(
        API_URL,
        data={'id': 1})

    assert res.status_code == 404

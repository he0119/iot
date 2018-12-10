'''Test User API'''
API_URL = '/api/users'


def test_get_username(client):
    '''get user info'''
    res = client.get(API_URL)

    assert res.json['username'] == 'test'
    assert res.json['email'] == 'test@test.com'


def test_create_user(client):
    '''create new user'''
    res = client.post(
        API_URL,
        data={'username': 'test1', 'password': 'test1', 'email': 'test1@test.com'})

    assert res.status_code == 201
    assert res.json['username'] == 'test1'
    assert res.json['message'] == 'Account Created'


def test_modify_user(client):
    '''modify user info'''
    res = client.put(
        API_URL,
        data={'email': 'test1@test.com'})
    assert res.status_code == 201

    res = client.get(API_URL)

    assert res.json['email'] == 'test1@test.com'


def test_delete_user(client):
    '''delete current user'''
    res = client.delete(API_URL)

    assert res.status_code == 204

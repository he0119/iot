'''Test Website Socketio'''


def test_website(client):
    '''request data through socketio'''
    client.socketio.emit('website', {'type': 'request'})

    res = client.socketio.get_received()

    assert res[0]['name'] == 'status'
    assert res[0]['args'][0]['id'] == 1
    assert res[0]['args'][0]['time'] == '2017-07-14T02:40:00+00:00'
    assert res[0]['args'][0]['data'] == {
        'control': False,
        'test1': 10.0,
        'test2': 12.0
        }

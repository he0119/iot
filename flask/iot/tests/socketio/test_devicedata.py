'''Test Device Socketio'''

def test_add_devicedata(client):
    '''add data through socketio'''
    client.socketio.emit('devicedata', {'data': "1500000010,1|12,22,1"})

    res = client.socketio.get_received()

    assert res[0]['name'] == 'status'
    assert res[0]['args'][0]['id'] == 1
    assert res[0]['args'][0]['time'] == '2017-07-14T02:40:10+00:00'
    assert res[0]['args'][0]['data'] == {
        'control': True,
        'test1': 12.0,
        'test2': 22.0
        }

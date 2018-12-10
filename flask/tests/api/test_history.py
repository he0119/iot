'''Test History API'''
API_URL = '/api/history'


def test_get_history(client):
    '''get status'''
    # FIXME: Won't pass when using sqlite, because func.row_number isn't available
    add_some_data(client)
    res = client.get(
        f'{API_URL}?id=1&start=1500000000&end=1500000010&interval=1')

    assert res.status_code == 200


def add_some_data(client):
    '''Add some test data'''
    api_url = '/api/status'
    data = {
        "id": 1,
        "time": 1500000010,
        "data": '12, 22, 1',
    }
    client.post(api_url, data=data)

    data = {
        "id": 1,
        "time": 1500050000,
        "data": '10, 12, 0',
    }
    client.post(api_url, data=data)

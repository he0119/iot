"""Test History API"""
import pytest

API_URL = '/api/history'


@pytest.mark.skip(reason='Do not support sqlite3')
def test_get_history(client):
    """Test history data.

    Won't pass when using sqlite,
    because func.row_number isn't available(will support in SQLite 3.25.0),
    but current version in python3.7 is 3.21.0
    """

    add_some_data(client)
    res = client.get(
        f'{API_URL}?id=1&start=1500000000&end=1500000010&interval=1')

    assert res.status_code == 200
    assert res.json[0]['id'] == 1
    assert res.json[0]['time'] == '2017-07-14T02:40:00+00:00'
    assert res.json[0]['data'] == {
        'test1': 10.0,
        'test2': 12.0,
        'control': False,
    }


def add_some_data(client):
    """Add some test data."""
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

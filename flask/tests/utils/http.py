'''HTTP Client'''
import json


class MyHttpClient():
    '''Add JWT Support'''

    def __init__(self, client, access_token, refresh_token, default_auth=None):
        self.client = client
        self.headers = {}
        self.access_token = access_token
        self.refresh_token = refresh_token

        if default_auth:
            self.set_auth(default_auth)

    def set_auth(self, auth):
        '''set auth'''
        if not auth:
            self.headers.pop('Authorization')
        if auth == 'access':
            self.headers['Authorization'] = f'Bearer {self.access_token}'
        if auth == 'refresh':
            self.headers['Authorization'] = f'Bearer {self.refresh_token}'

    def get(self, url, headers=None, data=None):
        '''get'''
        _headers = self.headers

        if headers:
            _headers = {**self.headers, **headers}

        return self.client.get(url, data=data, headers=_headers)

    def post(self, url, headers=None, data=None):
        '''post'''
        _headers = {**{'content-type': 'application/json'}, **self.headers}

        if headers:
            _headers = {**_headers, **headers}

        return self.client.post(url, data=json.dumps(data), headers=_headers)

    def put(self, url, headers=None, data=None):
        '''put'''
        _headers = {**{'content-type': 'application/json'}, **self.headers}

        if headers:
            _headers = {**_headers, **headers}

        return self.client.put(url, data=json.dumps(data), headers=_headers)

    def delete(self, url, headers=None, data=None):
        '''delete'''
        _headers = {**{'content-type': 'application/json'}, **self.headers}

        if headers:
            _headers = {**_headers, **headers}

        return self.client.delete(url, data=json.dumps(data), headers=_headers)

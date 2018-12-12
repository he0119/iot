'''HTTP Client'''
import json
from enum import IntEnum, unique


@unique
class AuthType(IntEnum):
    '''Authorization Type'''
    empty = 1
    access = 2
    refresh = 3


class MyTestClient():
    '''Add JWT Support'''

    def __init__(self,
                 http_client, socketio_client,
                 access_token, refresh_token, default_auth=None):

        self.http = http_client
        self.socketio = socketio_client
        self.headers = {}
        self.access_token = access_token
        self.refresh_token = refresh_token

        if default_auth:
            self.set_auth(default_auth)

    def set_auth(self, auth):
        '''set auth'''
        if auth == AuthType.empty:
            if 'Authorization' in self.headers:
                self.headers.pop('Authorization')
        if auth == AuthType.access:
            self.headers['Authorization'] = f'Bearer {self.access_token}'
        if auth == AuthType.refresh:
            self.headers['Authorization'] = f'Bearer {self.refresh_token}'

    def get(self, url, headers=None, data=None):
        '''get'''
        _headers = self.headers

        if headers:
            _headers = {**self.headers, **headers}

        return self.http.get(url, data=data, headers=_headers)

    def post(self, url, headers=None, data=None):
        '''post'''
        _headers = {**{'content-type': 'application/json'}, **self.headers}

        if headers:
            _headers = {**_headers, **headers}

        return self.http.post(url, data=json.dumps(data), headers=_headers)

    def put(self, url, headers=None, data=None):
        '''put'''
        _headers = {**{'content-type': 'application/json'}, **self.headers}

        if headers:
            _headers = {**_headers, **headers}

        return self.http.put(url, data=json.dumps(data), headers=_headers)

    def delete(self, url, headers=None, data=None):
        '''delete'''
        _headers = {**{'content-type': 'application/json'}, **self.headers}

        if headers:
            _headers = {**_headers, **headers}

        return self.http.delete(url, data=json.dumps(data), headers=_headers)

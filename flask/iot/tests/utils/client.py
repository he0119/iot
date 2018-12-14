"""Custom HTTP&SocketIO Test Client"""
import json
from enum import IntEnum, unique

from run import socketio
from tests.conftest import app


@unique
class TokenType(IntEnum):
    """Authorization Type"""
    empty = 1
    access = 2
    refresh = 3


class MyTestClient():
    """Add JWT Support"""

    def __init__(self,
                 access_token, refresh_token, default_auth=None):

        # Use basic auth for socketio client
        self.socketio = socketio.test_client(
            app, headers={'Authorization': 'Basic dGVzdDp0ZXN0'})

        self.http = app.test_client()
        self.headers = {}
        self.access_token = access_token
        self.refresh_token = refresh_token

        if default_auth:
            self.set_auth(default_auth)

    def set_auth(self, auth):
        """Set Authorization Token Type."""
        if auth == TokenType.empty:
            if 'Authorization' in self.headers:
                self.headers.pop('Authorization')
        if auth == TokenType.access:
            self.headers['Authorization'] = f'Bearer {self.access_token}'
        if auth == TokenType.refresh:
            self.headers['Authorization'] = f'Bearer {self.refresh_token}'

    def get(self, url, headers=None, data=None):
        """Get"""
        _headers = self.headers

        if headers:
            _headers = {**self.headers, **headers}

        return self.http.get(url, data=data, headers=_headers)

    def post(self, url, headers=None, data=None):
        """Post"""
        _headers = {**{'content-type': 'application/json'}, **self.headers}

        if headers:
            _headers = {**_headers, **headers}

        return self.http.post(url, data=json.dumps(data), headers=_headers)

    def put(self, url, headers=None, data=None):
        """Put"""
        _headers = {**{'content-type': 'application/json'}, **self.headers}

        if headers:
            _headers = {**_headers, **headers}

        return self.http.put(url, data=json.dumps(data), headers=_headers)

    def delete(self, url, headers=None, data=None):
        """Delete"""
        _headers = {**{'content-type': 'application/json'}, **self.headers}

        if headers:
            _headers = {**_headers, **headers}

        return self.http.delete(url, data=json.dumps(data), headers=_headers)

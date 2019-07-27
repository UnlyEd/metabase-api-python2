from __future__ import absolute_import
import os
import time
import requests


class Metabase(object):

    def __init__(self, *args, **kwargs):
        if 'session' in kwargs: session = kwargs['session']; del kwargs['session']
        else: session = None
        if 'password' in kwargs: password = kwargs['password']; del kwargs['password']
        else: password = None
        if 'email' in kwargs: email = kwargs['email']; del kwargs['email']
        else: email = None
        if 'endpoint' in kwargs: endpoint = kwargs['endpoint']; del kwargs['endpoint']
        else: endpoint = None
        self.endpoint = endpoint or os.getenv(u'METABASE_ENDPOINT') + u'/api'
        self.email = email or os.getenv(u'METABASE_AUTH_EMAIL')
        self.password = password or os.getenv(u'METABASE_AUTH_PASSWORD')
        self.session = session or os.getenv(u'METABASE_SESSION')
        self.auth_callback = kwargs.pop(u'auth_callback', None)

        if self.session is None:
            self.auth()

    def session_header(self):
        return {u'X-Metabase-Session': self.session}

    def get_session_headers(self, *args, **kwargs):
        res = requests.get(self.endpoint + u'/user/current',
                           headers=self.session_header())
        if res.status_code == 401:
            self.auth()
        return self.session_header()

    def fetch_header(self, r):
        if r.status_code == 200:
            return True
        else:
            return False

    def fetch_body(self, r):
        if r.status_code == 200:
            return True, r.json()
        else:
            return False, None

    def _get_session_headers(self, kwargs):
        if not kwargs.pop(u'check_session', True):
            return self.get_session_header(**kwargs)
        return headers or {}

    def get(self, *args, **kwargs):
        if 'headers' in kwargs: headers = kwargs['headers']; del kwargs['headers']
        else: headers = None
        headers = self.get_session_headers(headers, kwargs)
        r = requests.get(self.endpoint + args[0], headers=headers, **kwargs)
        return self.fetch_body(r)

    def post(self, *args, **kwargs):
        if 'headers' in kwargs: headers = kwargs['headers']; del kwargs['headers']
        else: headers = None
        headers = self.get_session_headers(headers, kwargs)
        r = requests.post(self.endpoint + args[0], headers=headers, **kwargs)
        return self.fetch_body(r)

    def put(self, *args, **kwargs):
        if 'headers' in kwargs: headers = kwargs['headers']; del kwargs['headers']
        else: headers = None
        headers = self.get_session_headers(headers, kwargs)
        r = requests.put(self.endpoint + args[0], headers=headers, **kwargs)
        return self.fetch_header(r)

    def delete(self, *args, **kwargs):
        if 'headers' in kwargs: headers = kwargs['headers']; del kwargs['headers']
        else: headers = None
        headers = self.get_session_headers(headers, kwargs)
        r = requests.put(self.endpoint + args[0], headers=headers, **kwargs)
        return self.fetch_header(r)

    def auth(self, **kwargs):
        payload = {
            u'username': self.email,
            u'password': self.password
        }

        res = requests.post(self.endpoint + u'/session', json=payload)

        if res.status_code == 200:
            data = res.json()
            self.session = data[u'id']
        else:
            raise Exception(res)

        if hasattr(self, u'auth_callback') and callable(self.auth_callback):
            self.auth_callback(self)

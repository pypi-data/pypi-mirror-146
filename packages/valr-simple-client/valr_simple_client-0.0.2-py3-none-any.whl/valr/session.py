from hashlib import sha512
from hmac import new as hmac_new
from time import time

import requests
from requests import Session, Request
from urllib.parse import urljoin


class ValrAPISession(Session):

    def __init__(self, key: str, secret: str, sub_account_id: str = None):
        super(ValrAPISession, self).__init__()

        self.headers.update({
            'X-VALR-API-KEY': key,
            'Content-Type': 'application/json',
        })

        self.api_key_secret = secret

        # This allows the primary account to transact on the impersonated sub account
        if sub_account_id:
            self.headers.update({
                'X-VALR-SUB-ACCOUNT-ID': sub_account_id
            })

        self.base_api_endpoint = 'https://api.valr.com/v1/'

    @staticmethod
    def _sign_request(api_key_secret, timestamp, verb, path, body=""):
        """Signs the request payload using the api key secret
        api_key_secret - the api key secret
        timestamp - the unix timestamp of this request e.g. int(time.time()*1000)
        verb - Http verb - GET, POST, PUT or DELETE
        path - path excluding host name, e.g. '/v1/withdraw
        body - http request body as a string, optional
        """
        payload = f"{timestamp}{verb.upper()}{path}{body}"
        message = bytearray(payload, 'utf-8')
        signature = hmac_new(bytearray(api_key_secret, 'utf-8'), message, digestmod=sha512).hexdigest()
        return signature

    def _update_headers(self, verb: str, path: str):
        timestamp = int(time() * 1000)
        self.headers.update({
            'X-VALR-SIGNATURE': self._sign_request(
                api_key_secret=self.api_key_secret,
                timestamp=timestamp,
                verb=verb,
                path=f'/v1/{path}'
            ),
            'X-VALR-TIMESTAMP': str(timestamp),
        })

    def post(self, path: str, *args, **kwargs):
        base_path = urljoin(self.base_api_endpoint, path)
        self._update_headers(verb='POST', path=base_path)
        return self.request('POST', base_path, *args, **kwargs)

    def get(self, path: str, *args, **kwargs):
        base_path = urljoin(self.base_api_endpoint, path)
        self._update_headers(verb='GET', path=path)
        kwargs.setdefault('allow_redirects', True)
        return self.request(method='GET', url=base_path, headers=self.headers, *args, **kwargs)

    def put(self, path: str, *args, **kwargs):
        base_path = urljoin(self.base_api_endpoint, path)
        self._update_headers(verb='PUT', path=path)
        return self.request('PUT', url=base_path, *args, **kwargs)

    def delete(self, path: str, *args, **kwargs):
        base_path = urljoin(self.base_api_endpoint, path)
        self._update_headers(verb='DELETE', path=path)
        return self.request('DELETE', url=base_path, *args, **kwargs)

    def patch(self, path: str, *args, **kwargs):
        base_path = urljoin(self.base_api_endpoint, path)
        self._update_headers(verb='PATCH', path=path)
        return self.request('PATCH', url=base_path, *args, **kwargs)

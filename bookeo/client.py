import json

import requests

from .availability import Availability
from .request import BookeoRequest

# https://www.bookeo.com/apiref


# TODO: Figure out some standard way of passing datetimes back to the user.


class BookeoClientException(Exception):
    def __init__(self, error_msg):
        self.error_msg = error_msg

    def __str__(self):
        return self.error_msg


class BookeoClient:
    BASE_URL = "https://api.bookeo.com/v2"

    def __init__(self, secret_key: str, api_key: str):
        if secret_key is None:
            raise ValueError("secret_key cannot be None")
        if api_key is None:
            raise ValueError("api_key cannot be None")
        self.secret_key = secret_key
        self.api_key = api_key

    def request(self, *args, **kwargs):
        r = BookeoRequest(self, *args, **kwargs)
        return r.request()

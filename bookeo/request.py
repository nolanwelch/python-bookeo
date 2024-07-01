import requests
import json

from .client import BookeoClient


class BookeoRequestException(Exception):
    def __init__(self, error_msg: str = "", url: str = None):
        self.error_msg = error_msg
        self.url = url

    def __str__(self):
        if self.url is None:
            return f"{self.error_msg}"
        return f"{self.error_msg} : {self.error_msg}"


class BookeoRequest:
    HTTP_METHODS = {  # HACK: Yeah this feels really bad lol
        "GET": requests.get,
        "POST": requests.post,
        "PUT": requests.put,
        "DELETE": requests.delete,
    }

    def __init__(
        self,
        client: BookeoClient,
        path: str,
        params: dict,
        data: dict | str,
        success_codes: list[int] = [200],
        method: str = "GET",
    ):
        self.params = params
        self.params.update(
            client.query_dict
        )  # TODO: Modify as needed to include API token etc.
        self.data = data
        if self.data is str:
            self.data = json.loads(self.data)
        self.host = client.BASE_URL
        self.headers = client.headers
        self.path = path
        self.method = method.upper()
        if self.method not in self.HTTP_METHODS:
            raise BookeoRequestException(f"{self.method} is not a valid HTTP method")
        self.success_codes = success_codes

    def request(self):
        url = self.host + self.path
        http_method = self.HTTP_METHODS[self.method]
        r = http_method(url, params=self.params, headers=self.headers, data=self.data)

        if r.status_code not in self.success_codes:
            raise BookeoRequestException(r.reason, self.path)

        # TODO: Handle and return JSON body
        data = r.json()

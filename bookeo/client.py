import json
from datetime import datetime
from typing import Optional, Union
from urllib.parse import urljoin

import pytz
import requests

VERSION = "0.1.0"
BOOKEO_TS_FORMAT = r"%Y-%m-%dT%H:%M:%SZ"


class BookeoClientException(Exception):
    """Class for exceptions related to the Bookeo client."""

    pass


class BookeoClient:
    def __init__(self, secret_key: str, api_key: str):
        if secret_key is None or api_key is None:
            raise TypeError("Must initialize secret_key and api_key")
        self._secret_key = secret_key
        self._api_key = api_key

    def query_dict(self) -> dict:
        """Returns the base query dictionary for Bookeo API requests."""
        return {"secretKey": self._secret_key, "apiKey": self._api_key}

    def base_url(self) -> str:
        """Returns the base URL for Bookeo API requests."""
        return "https://api.bookeo.com/v2"

    def headers(self) -> dict:
        """Returns the standard headers for Bookeo API requests."""
        return {
            "Cache-Control": "no-cache",
            "User-Agent": f"PythonBookeo/{VERSION}",
            "Accept": "text/html,application/json",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
        }

    def _request(self, *args, **kwargs) -> requests.Response:
        r = BookeoRequest(self, *args, **kwargs)
        return r.request()


def bookeo_timestamp_to_dt(timestamp: Optional[str]) -> Optional[datetime]:
    if timestamp is None:
        return None

    dt = datetime.strptime(timestamp, BOOKEO_TS_FORMAT)
    return pytz.utc.localize(dt)


def dt_to_bookeo_timestamp(dt: Optional[datetime]) -> Optional[str]:
    if dt is None:
        return None

    if dt.tzinfo is not None:
        # assume naive datetimes are in UTC
        dt = dt.astimezone(pytz.timezone("UTC"))
    return datetime.strftime(dt, BOOKEO_TS_FORMAT)


class BookeoRequestException(Exception):
    """Class for errors relating to Bookeo API calls."""

    def __init__(self, error_msg: str = "", url: str = None):
        self.error_msg = error_msg
        self.url = url

    def __str__(self):
        if self.url is None:
            return f"{self.error_msg}"
        return f"{self.error_msg} : {self.error_msg}"


class BookeoRequest:
    _HTTP_METHODS = ["GET", "POST", "PUT", "DELETE"]

    def __init__(
        self,
        client: BookeoClient,
        path: str,
        params: dict = None,
        data: Union[dict, str] = {},
        method: str = "GET",
    ):
        self.params = params or {}
        self.params.update(client.query_dict())
        self.data = data
        if self.data is str:
            self.data = json.loads(self.data)
        self.host = client.base_url()
        self.headers = client.headers()
        self.path = path
        self.method = method.upper()
        if self.method not in self._HTTP_METHODS:
            raise ValueError(f"{self.method} is not a valid HTTP method.")

    def request(self) -> requests.Response:
        url = urljoin(self.host, self.path)
        match self.method:
            case "GET":
                return requests.get(
                    url, params=self.params, headers=self.headers, data=self.data
                )
            case "POST":
                return requests.post(
                    url, params=self.params, headers=self.headers, data=self.data
                )
            case "PUT":
                return requests.put(
                    url, params=self.params, headers=self.headers, data=self.data
                )
            case "DELETE":
                return requests.delete(
                    url, params=self.params, headers=self.headers, data=self.data
                )


class BookeoRequestPager:
    """Pages the requested Bookeo API method and returns the JSON data of each response."""

    def __init__(self, request: BookeoRequest, items_per_page: int = 50):
        if "pageNavigationToken" in request.params.keys():
            raise BookeoRequestException("Paged URL cannot include navigation token")
        self._request = request
        self._items_per_page = items_per_page

    def __iter__(self):
        resp = self._request.request()
        page_data = resp.json()["info"]
        if not isinstance(page_data, dict):
            raise BookeoRequestException("Pagination info is invalid")
        self._total_items = page_data["totalItems"]
        self._total_pages = page_data["totalPages"]
        self._current_page = page_data["currentPage"]
        self._nav_token = page_data.get("pageNavigationToken")
        return self

    def __next__(self) -> dict:
        next_page = self._current_page + 1
        if next_page > self._total_pages:
            raise StopIteration

        self._current_page = next_page
        new_params = {
            "pageNavigationToken": self._nav_token,
            "pageNumber": self._current_page,
            "itemsPerPage": self._items_per_page,
        }
        self._request.params.update(new_params)
        resp = self._request.request()
        return resp.json()["info"]

    def num_items(self) -> int:
        return self._total_items

    def __len__(self) -> int:
        return self._total_pages

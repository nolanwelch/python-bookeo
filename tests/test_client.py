from datetime import datetime

import pytest
import pytz
from httmock import HTTMock, all_requests

from bookeo import client


class TestTimestampConversion:
    def test_bookeo_timestamp_to_dt_None(self):
        assert client.bookeo_timestamp_to_dt(None) is None

    def test_bookeo_timestamp_to_dt(self):
        dt = client.bookeo_timestamp_to_dt("2019-08-24T14:15:22Z")
        assert dt == datetime(
            year=2019,
            month=8,
            day=24,
            hour=14,
            minute=15,
            second=22,
            tzinfo=pytz.utc,
        )

    def test_dt_to_bookeo_timestamp_None(self):
        assert client.dt_to_bookeo_timestamp(None) is None

    def test_naive_dt_to_bookeo_timestamp(self):
        dt = datetime(
            year=2024,
            month=3,
            day=14,
            hour=15,
            minute=9,
            second=26,
        )
        assert client.dt_to_bookeo_timestamp(dt) == "2024-03-14T15:09:26Z"

    def test_aware_dt_to_bookeo_timestamp(self):
        tz = pytz.timezone("US/Eastern")
        dt = datetime(
            year=2020,
            month=10,
            day=31,
            hour=23,
            minute=55,
            second=29,
        )
        dt = tz.localize(dt)
        assert client.dt_to_bookeo_timestamp(dt) == "2020-11-01T03:55:29Z"


@pytest.fixture
def example_client():
    return client.BookeoClient("X", "X")


class TestBookeoClient:

    def test_init(self):
        with pytest.raises(TypeError):
            client.BookeoClient("X", None)
        with pytest.raises(TypeError):
            client.BookeoClient(None, "X")

    def test_query_dict(self):
        secret_key = "hunter2"
        api_key = "ABC123"
        c = client.BookeoClient(secret_key, api_key)
        assert c.query_dict() == {"secretKey": secret_key, "apiKey": api_key}

    def test_base_url(self, example_client):
        assert example_client.base_url() == "https://api.bookeo.com/v2"

    def test_headers(self, example_client):
        assert example_client.headers() == {
            "Cache-Control": "no-cache",
            "User-Agent": f"PythonBookeo/0.1.0",
            "Accept": "text/html,application/json",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
        }


@all_requests
def google_mock(url, request):
    match request.method:
        case "GET":
            status_code = 200
        case "PUT":
            status_code = 207
        case "POST":
            status_code = 201
        case "DELETE":
            status_code = 204
    return {
        "content": request.method,
        "status_code": status_code,
    }


class TestBookeoRequest:
    def test_init(self, example_client):
        with pytest.raises(ValueError):
            r = client.BookeoRequest(example_client, "test", method="INVALIDVERB")
        r = client.BookeoRequest(example_client, "test")
        r = client.BookeoRequest(example_client, "test", method="GET")
        r = client.BookeoRequest(example_client, "test", method="PUT")
        r = client.BookeoRequest(example_client, "test", method="POST")
        r = client.BookeoRequest(example_client, "test", method="DELETE")

    def test_get_request(self, example_client):
        with HTTMock(google_mock):
            r = client.BookeoRequest(example_client, "google.com")
            resp = r.request()
        assert resp.content == b"GET"
        assert resp.status_code == 200

        with HTTMock(google_mock):
            r = client.BookeoRequest(example_client, "google.com", method="GET")
            resp = r.request()
        assert resp.content == b"GET"
        assert resp.status_code == 200

    def test_put_request(self, example_client):
        with HTTMock(google_mock):
            r = client.BookeoRequest(example_client, "google.com", method="PUT")
            resp = r.request()
        assert resp.content == b"PUT"
        assert resp.status_code == 207

    def test_post_request(self, example_client):
        with HTTMock(google_mock):
            r = client.BookeoRequest(example_client, "google.com", method="POST")
            resp = r.request()
        assert resp.content == b"POST"
        assert resp.status_code == 201

    def test_delete_request(self, example_client):
        with HTTMock(google_mock):
            r = client.BookeoRequest(example_client, "google.com", method="DELETE")
            resp = r.request()
        assert resp.content == b"DELETE"
        assert resp.status_code == 204


class TestBookeoRequestPager:
    def test_init(self, example_client):
        with pytest.raises(client.BookeoRequestException):
            request = client.BookeoRequest(
                example_client, "google.com", params={"pageNavigationToken": "X"}
            )
            p = client.BookeoRequestPager(request)

    # TODO: Write remaining tests           

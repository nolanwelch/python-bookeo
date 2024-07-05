from datetime import datetime
from typing import Optional

import pytz
import requests

from .client import BookeoClient
from .request import BookeoRequest

# TODO: Decide how to handle pagination
# Idea: something like below
# def some_method(
#     *args,
#     nav_token: Optional[str],
#     page_number: Optional[int],
#     items_per_page: Optional[int],
#     use_paging: bool = True,
#     use_iterator: bool = False,
# ):
#     params = {...}
#     iterator = BookeoRequestIterable(request(params))
#     if use_iterator:
#         return iterator
#     if use_paging:
#         params.update(
#             {
#                 "pageNavigationToken": nav_token,
#                 "pageNumber": page_number,
#                 "itemsPerPage": items_per_page,
#             }
#         )
#     else:
#         data = []
#         while iterator.has_next():
#             data.extend(iterator.next())


class BookeoAPI:
    def __init__(self, client: BookeoClient):
        self.client = client

    def _request(self, *args, **kwargs) -> requests.Response:
        r = BookeoRequest(self.client, *args, **kwargs)
        return r.request()


def bookeo_timestamp_to_dt(timestamp: str) -> Optional[datetime]:
    if timestamp is None:
        return None
    dt = datetime.strptime(timestamp, r"%Y-%m-%dT%H:%M:%SZ")
    return pytz.utc.localize(dt)


def dt_to_bookeo_timestamp(dt: datetime) -> Optional[str]:
    if dt is None:
        return None
    utc_dt = dt.astimezone(pytz.utc)
    return datetime.strftime(utc_dt, r"%Y-%m-%dT%H:%M:%SZ")

from datetime import datetime
from typing import Optional

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


# TODO: Implement this method
def dt_from_bookeo_str(timestamp: str) -> Optional[datetime]:
    pass


# TODO: Implement this method
def bookeo_timestamp_from_dt(dt: datetime) -> Optional[str]:
    pass

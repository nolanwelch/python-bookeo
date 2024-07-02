# https://www.bookeo.com/apiref/#tag/Availability

from datetime import datetime

import requests

from .client import BookeoClient
from .core import BookeoAPI
from .schemas import BookeoProduct

# TODO: Finish implementing availability methods


class BookeoAvailability(BookeoAPI):
    def __init__(self, client: BookeoClient):
        super.__init__(client)

    def _product_availability_info(
        productId: str,
        startTime: datetime,
        endTime: datetime,
        pageNavigationToken: str,
        mode: str,
        itemsPerPage: int = 50,
        pageNumber: int = 1,
    ) -> list[BookeoProduct]:
        """Performs a basic search to find available slots and number of seats in each."""
        params = {}

        res = requests.get(
            url="https://api.bookeo.com/v2/availability/slots", params=params
        )

        if res.status_code != 200:
            raise

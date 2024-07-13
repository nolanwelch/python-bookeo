from datetime import datetime

from .client import BookeoClient, BookeoRequestException, dt_to_bookeo_timestamp
from .schemas import (
    BookeoBookingOption,
    BookeoMatchingSlot,
    BookeoPagination,
    BookeoPeopleNumber,
    BookeoProduct,
    BookeoResource,
)


class BookeoAvailability(BookeoClient):

    def product_availability_info(
        self,
        product_id: str = None,
        start_time: datetime = None,
        end_time: datetime = None,
        items_per_page: int = None,
        nav_token: str = None,
        page_number: int = None,
        mode: str = None,
    ) -> tuple[list[BookeoProduct], BookeoPagination]:
        """Performs a basic search to find available slots and number of seats in each."""
        resp = self._request(
            "/availability/slots",
            params={
                "productId": product_id,
                "startTime": dt_to_bookeo_timestamp(start_time),
                "endTime": dt_to_bookeo_timestamp(end_time),
                "itemsPerPage": items_per_page,
                "pageNavigationToken": nav_token,
                "pageNumber": page_number,
                "mode": mode,
            },
        )
        if resp.status_code != 200:
            raise BookeoRequestException(
                f"Could not get product availability information.", resp.request.url
            )
        data = resp.json()
        blocks = [BookeoProduct(**p) for p in data["data"]]
        info = data["info"]
        pager = BookeoPagination(**info)
        return (blocks, pager)

    def search_open_slots(
        self,
        product_id: str,
        start_time: datetime,
        end_time: datetime,
        people_numbers: list[BookeoPeopleNumber],
        items_per_page: int = None,
        mode: str = None,
        options: list[BookeoBookingOption] = [],
        resources: list[BookeoResource] = [],
    ) -> tuple[list[BookeoMatchingSlot], str, BookeoPagination]:
        """Creates a search for available slots that match the given search parameters."""
        if product_id is None:
            raise TypeError("product_id cannot be None.")
        if start_time is None:
            raise TypeError("start_time cannot be None.")
        if end_time is None:
            raise TypeError("end_time cannot be None.")
        resp = self._request(
            "/availability/matchingslots",
            params={
                "itemsPerPage": items_per_page,
                "mode": mode,
            },
            data={
                "productId": product_id,
                "startTime": dt_to_bookeo_timestamp(start_time),
                "endTime": dt_to_bookeo_timestamp(end_time),
                "peopleNumbers": [p.model_dump() for p in people_numbers],
                "options": [o.model_dump() for o in options],
                "resources": [r.model_dump() for r in resources],
            },
            method="POST",
        )
        if resp.status_code != 201:
            raise BookeoRequestException(
                "Could not create the specified search for product availability information.",
                resp.request.url,
            )
        data = resp.json()
        slots = [BookeoMatchingSlot(**s) for s in data["data"]]
        location = resp.headers["Location"]
        info = data["info"]
        pager = BookeoPagination(**info)
        return (slots, location, pager)

    def nav_slot_search(self, nav_token: str, page_number: str = None):
        if nav_token is None:
            raise TypeError("nav_token cannot be None.")
        resp = self._request(
            f"/availability/matchingslots/{nav_token}",
            params={
                "pageNumber": page_number,
            },
        )
        if resp.status_code != 200:
            raise BookeoRequestException(
                "Could not navigate specified search for product availability information.",
                resp.request.url,
            )
        data = resp.json()
        slots = [BookeoMatchingSlot(**s) for s in data["data"]]
        info = data["info"]
        pager = BookeoPagination(**info)
        return (slots, pager)

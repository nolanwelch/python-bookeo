from datetime import datetime
from typing import Optional

from .core import BookeoAPI, dt_to_bookeo_timestamp
from .schemas import (
    BookeoBookingOption,
    BookeoMatchingSlot,
    BookeoPagination,
    BookeoPeopleNumber,
    BookeoProduct,
    BookeoResource,
)


class BookeoAvailability(BookeoAPI):
    def product_availability_info(
        self,
        product_id: Optional[str],
        start_time: Optional[datetime],
        end_time: Optional[datetime],
        items_per_page: Optional[int],
        nav_token: Optional[str],
        page_number: Optional[int],
        mode: Optional[str],
    ) -> Optional[tuple[list[BookeoProduct], BookeoPagination]]:
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
            return []
        data = resp.json()
        blocks = [BookeoProduct(**p) for p in data["data"]]
        info = data["info"]
        pager = BookeoPagination(**info)
        return (blocks, pager)

    def search_open_slots(
        self,
        items_per_page: Optional[int],
        mode: Optional[str],
        product_id: str,
        start_time: datetime,
        end_time: datetime,
        people_numbers: list[BookeoPeopleNumber],
        options: Optional[list[BookeoBookingOption]],
        resources: Optional[list[BookeoResource]],
    ) -> Optional[tuple[list[BookeoMatchingSlot], str, BookeoPagination]]:
        """Creates a search for available slots that match the given search parameters."""
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
            return None
        data = resp.json()
        slots = [BookeoMatchingSlot(**s) for s in data["data"]]
        location = resp.headers.get("Location")
        info = data["info"]
        pager = BookeoPagination(**info)
        return (slots, location, pager)

    def nav_slot_search(self, nav_token: str, page_number: Optional[str]):
        resp = self._request(
            f"/availability/matchingslots/{nav_token}",
            params={
                "pageNumber": page_number,
            },
        )
        if resp.status_code != 200:
            return None
        data = resp.json()
        slots = [BookeoMatchingSlot(**s) for s in data["data"]]
        info = data["info"]
        pager = BookeoPagination(**info)
        return (slots, pager)

from datetime import datetime
from typing import Optional

from .core import BookeoAPI, dt_to_bookeo_timestamp
from .schemas import BookeoPagination, BookeoSeatBlock


class BookeoSeatblocks(BookeoAPI):
    def get_seat_blocks(
        self,
        start_time: Optional[datetime],
        end_time: Optional[datetime],
        last_updated_start_time: Optional[datetime],
        last_updated_end_time: Optional[datetime],
        product_id: Optional[str],
        items_per_page: Optional[int],
        nav_token: Optional[str],
        page_number: Optional[int],
    ) -> Optional[tuple[list[BookeoSeatBlock], BookeoPagination]]:
        resp = self._request(
            "/seatblocks",
            params={
                "startTime": dt_to_bookeo_timestamp(start_time),
                "endTime": dt_to_bookeo_timestamp(end_time),
                "lastUpdatedStartTime": dt_to_bookeo_timestamp(last_updated_start_time),
                "lastUpdatedEndTime": dt_to_bookeo_timestamp(last_updated_end_time),
                "productId": str(product_id),
                "itemsPerPage": items_per_page,
                "pageNavigationToken": nav_token,
                "pageNumber": page_number,
            },
        )
        if resp.status_code != 200:
            return None
        data = resp.json()
        seat_blocks = [BookeoSeatBlock(**sb) for sb in data["data"]]
        info = data["info"]
        pager = BookeoPagination(**info)
        return (seat_blocks, pager)

    def create_seat_block(
        self, event_id: str, product_id: str, reason: Optional[str], num_seats: int
    ) -> Optional[tuple[str, BookeoSeatBlock]]:
        """Creates a new seat block, "blocking" a given number of seats so that they're not available for booking."""
        resp = self._request(
            "/seatblocks",
            data={
                "eventId": event_id,
                "productId": product_id,
                "reason": reason,
                "numSeats": num_seats,
            },
            method="POST",
        )
        if resp.status_code != 201:
            return None
        location = resp.headers.get("Location")
        data = resp.json()
        return (location, BookeoSeatBlock(**data))

    def get_seat_block(self, id: str) -> Optional[BookeoSeatBlock]:
        """Retrieves a seat block by its id."""
        resp = self._request(f"/seatblocks/{id}")
        if resp.status_code != 200:
            return None
        data = resp.json()
        return BookeoSeatBlock(**data)

    def update_seat_block(
        self, event_id: str, product_id: str, reason: Optional[str], num_seats: int
    ) -> Optional[tuple[str, BookeoSeatBlock]]:
        resp = self._request(
            f"/seatblocks/{id}",
            data={
                "eventId": event_id,
                "productId": product_id,
                "reason": reason,
                "numSeats": num_seats,
            },
            method="PUT",
        )
        if resp.status_code != 200:
            return None
        location = resp.headers.get("Location")
        data = resp.json()
        return (location, BookeoSeatBlock(**data))

    def delete_seat_block(self, id: str) -> bool:
        """Deletes a seat block, returning True if successful."""
        resp = self._request(f"/seatblocks/{id}", method="DELETE")
        return resp.status_code == 204

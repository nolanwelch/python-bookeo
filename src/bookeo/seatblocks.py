from datetime import datetime

from .core import BookeoAPI, dt_to_bookeo_timestamp
from .request import BookeoRequestException
from .schemas import BookeoPagination, BookeoSeatBlock


class BookeoSeatblocks(BookeoAPI):

    def get_seat_blocks(
        self,
        start_time: datetime = None,
        end_time: datetime = None,
        last_updated_start_time: datetime = None,
        last_updated_end_time: datetime = None,
        product_id: str = None,
        items_per_page: int = None,
        nav_token: str = None,
        page_number: int = None,
    ) -> tuple[list[BookeoSeatBlock], BookeoPagination]:
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
            raise BookeoRequestException(
                "Could not get requested seat blocks.", resp.request.url
            )
        data = resp.json()
        seat_blocks = [BookeoSeatBlock(**sb) for sb in data["data"]]
        info = data["info"]
        pager = BookeoPagination(**info)
        return (seat_blocks, pager)

    def create_seat_block(
        self, event_id: str, product_id: str, num_seats: int, reason: str = None
    ) -> tuple[str, BookeoSeatBlock]:
        """Creates a new seat block, "blocking" a given number of seats so that they're not available for booking."""
        if event_id is None:
            raise TypeError("event_id cannot be None.")
        if product_id is None:
            raise TypeError("product_id cannot be None.")
        if num_seats is None:
            raise TypeError("num_seats cannot be None.")
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
            raise BookeoRequestException(
                "Could not create requested seat block.", resp.request.url
            )
        location = resp.headers["Location"]
        data = resp.json()
        return (location, BookeoSeatBlock(**data))

    def get_seat_block(self, id: str) -> BookeoSeatBlock:
        """Retrieves a seat block by its id."""
        if id is None:
            raise TypeError("id cannot be None.")
        resp = self._request(f"/seatblocks/{id}")
        if resp.status_code != 200:
            raise BookeoRequestException(
                f"Could not get seat block with id {id}.", resp.request.url
            )
        data = resp.json()
        return BookeoSeatBlock(**data)

    def update_seat_block(
        self, event_id: str, product_id: str, num_seats: int, reason: str = None
    ) -> tuple[str, BookeoSeatBlock]:
        if event_id is None:
            raise TypeError("event_id cannot be None.")
        if product_id is None:
            raise TypeError("product_id cannot be None.")
        if num_seats is None:
            raise TypeError("num_seats cannot be None.")
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
            raise BookeoRequestException(
                f"Could not update seat block with id {id}.", resp.request.url
            )
        location = resp.headers["Location"]
        data = resp.json()
        return (location, BookeoSeatBlock(**data))

    def delete_seat_block(self, id: str) -> None:
        """Deletes a seat block."""
        if id is None:
            raise TypeError("id cannot be None.")
        resp = self._request(f"/seatblocks/{id}", method="DELETE")
        if resp.status_code != 204:
            raise BookeoRequestException(
                f"Could not delete seat block with id {id}.", resp.request.url
            )
        return

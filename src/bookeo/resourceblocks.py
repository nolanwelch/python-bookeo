from datetime import datetime

from .core import BookeoAPI, dt_to_bookeo_timestamp
from .request import BookeoRequestException
from .schemas import BookeoPagination, BookeoResource, BookeoResourceBlock


class BookeoResourceBlocks(BookeoAPI):

    def get_resource_blocks(
        self,
        start_time: datetime = None,
        end_time: datetime = None,
        last_updated_start_time: datetime = None,
        last_updated_end_time: datetime = None,
        resource_id: str = None,
        items_per_page: int = None,
        nav_token: str = None,
        page_number: int = None,
    ) -> tuple[list[BookeoResourceBlock], BookeoPagination]:
        resp = self._request(
            "/resourceblocks",
            params={
                "startTime": start_time,
                "endTime": end_time,
                "lastUpdatedStartTime": last_updated_start_time,
                "lastUpdatedEndTime": last_updated_end_time,
                "resource_id": resource_id,
                "itemsPerPage": items_per_page,
                "pageNavigationToken": nav_token,
                "pageNumber": page_number,
            },
        )
        if resp.status_code != 200:
            raise BookeoRequestException(
                f"Could not get requested resource blocks.", resp.request.url
            )
        data = resp.json()
        blocks = [BookeoResourceBlock(**rb) for rb in data["data"]]
        info = data["info"]
        pager = BookeoPagination(**info)
        return (blocks, pager)

    def create_new_resource_block(
        self,
        start_time: datetime,
        end_time: datetime,
        resources: list[BookeoResource],
        reason: str = None,
    ) -> tuple[str, BookeoResourceBlock]:
        """Creates a new resource block."""
        if start_time is None:
            raise TypeError("start_time cannot be None.")
        if end_time is None:
            raise TypeError("end_time cannot be None.")
        if resources is None:
            raise TypeError("resources cannot be None.")
        resp = self._request(
            "/resourceblocks",
            data={
                "startTime": dt_to_bookeo_timestamp(start_time),
                "endTime": dt_to_bookeo_timestamp(end_time),
                "reason": reason,
                "resources": [r.model_dump() for r in resources],
            },
            method="POST",
        )
        if resp.status_code != 201:
            raise BookeoRequestException(
                "Could not create requested resource block.", resp.request.url
            )
        location = resp.headers["Location"]
        data = resp.json()
        return (location, BookeoResourceBlock(**data))

    def get_resource_block(self, id: str) -> BookeoResourceBlock:
        """Retrieves a resource block by its id."""
        if id is None:
            raise TypeError("id cannot be None.")
        resp = self._request(f"/resourceblocks/{id}")
        if resp.status_code != 200:
            raise BookeoRequestException(
                f"Could not get resource block with id {id}.", resp.request.url
            )
        data = resp.json()
        return BookeoResourceBlock(**data)

    def update_resource_block(
        self,
        id: str,
        start_time: datetime,
        end_time: datetime,
        resources: list[BookeoResource],
        reason: str = None,
    ) -> None:
        if start_time is None:
            raise TypeError("start_time cannot be None.")
        if end_time is None:
            raise TypeError("end_time cannot be None.")
        if resources is None:
            raise TypeError("resources cannot be None.")
        """Updates an existing resource block."""
        resp = self._request(
            f"/resourceblocks/{id}",
            data={
                "startTime": dt_to_bookeo_timestamp(start_time),
                "endTime": dt_to_bookeo_timestamp(end_time),
                "reason": reason,
                "resources": [r.model_dump() for r in resources],
            },
            method="PUT",
        )
        if resp.status_code != 200:
            raise BookeoRequestException(
                f"Could not update resource block with id {id}.", resp.request.url
            )
        return

    def delete_resource_block(self, id: str) -> None:
        """Deletes an existing resource block."""
        if id is None:
            raise TypeError("id cannot be None.")
        resp = self._request(f"/resourceblocks/{id}", method="DELETE")
        if resp.status_code != 204:
            raise BookeoRequestException(
                f"Could not delete resource block with id {id}", resp.request.url
            )
        return

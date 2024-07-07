from datetime import datetime
from typing import Optional

from .core import BookeoAPI, dt_to_bookeo_timestamp
from .schemas import BookeoPagination, BookeoResource, BookeoResourceBlock


class BookeoResourceBlocks(BookeoAPI):
    def get_resource_blocks(
        self,
        start_time: Optional[datetime],
        end_time: Optional[datetime],
        last_updated_start_time: Optional[datetime],
        last_updated_end_time: Optional[datetime],
        resource_id: Optional[str],
        items_per_page: Optional[int],
        nav_token: Optional[str],
        page_number: Optional[int],
    ) -> Optional[tuple[list[BookeoResourceBlock], BookeoPagination]]:
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
            return None
        data = resp.json()
        blocks = [BookeoResourceBlock.from_dict(rb) for rb in data["data"]]
        pager = BookeoPagination.from_dict(data["info"])
        return (blocks, pager)

    def create_new_resource_block(
        self,
        start_time: datetime,
        end_time: datetime,
        reason: Optional[str],
        resources: list[BookeoResource],
    ) -> Optional[tuple[str, BookeoResourceBlock]]:
        """Creates a new resource block."""
        resp = self._request(
            "/resourceblocks",
            data={
                "startTime": dt_to_bookeo_timestamp(start_time),
                "endTime": dt_to_bookeo_timestamp(end_time),
                "reason": reason,
                "resources": [r.to_dict() for r in resources],
            },
            method="POST",
        )
        if resp.status_code != 201:
            return None
        location = resp.headers.get("Location")
        data = resp.json()
        return (location, BookeoResourceBlock.from_dict(data))

    def get_resource_block(self, id: str) -> Optional[BookeoResourceBlock]:
        """Retrieves a resource block by its id."""
        resp = self._request(f"/resourceblocks/{id}")
        if resp.status_code != 200:
            return None
        return BookeoResourceBlock.from_dict(resp.json())

    def update_resource_block(
        self,
        id: str,
        start_time: datetime,
        end_time: datetime,
        reason: Optional[str],
        resources: list[BookeoResource],
    ) -> bool:
        """Updates an existing resource block, returning True if successful."""
        resp = self._request(
            f"/resourceblocks/{id}",
            data={
                "startTime": dt_to_bookeo_timestamp(start_time),
                "endTime": dt_to_bookeo_timestamp(end_time),
                "reason": reason,
                "resources": [r.to_dict() for r in resources],
            },
            method="PUT",
        )
        return resp.status_code == 200

    def delete_resource_block(self, id: str) -> bool:
        """Deletes an existing resource block, returning True if successful."""
        resp = self._request(f"/resourceblocks/{id}", method="DELETE")
        return resp.status_code == 204

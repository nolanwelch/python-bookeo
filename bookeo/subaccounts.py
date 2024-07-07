from typing import Optional

from .core import BookeoAPI
from .request import BookeoRequestException
from .schemas import BookeoPagination, BookeoSubaccount


class BookeoSubaccountException(BookeoRequestException):
    def __init__(self, error_msg):
        self.error_msg = error_msg

    def __str__(self):
        return self.error_msg


class BookeoSubaccounts(BookeoAPI):
    def get_subaccounts(
        self,
        nav_token: Optional[str],
        page_number: Optional[int],
        items_per_page: Optional[int],
    ) -> Optional[tuple[list[BookeoSubaccount], BookeoPagination]]:
        """Returns a list of all subaccounts in the portal."""
        resp = self._request(
            "/subaccounts",
            params={
                "itemsPerPage": items_per_page,
                "pageNavigationToken": nav_token,
                "pageNumber": page_number,
            },
        )
        if resp.status_code != 200:
            return None
        data = resp.json()
        accounts = [BookeoSubaccount.from_dict(a) for a in data["data"]]
        pager = BookeoPagination.from_dict(data["info"])
        return (accounts, pager)

    def create_new_subaccount_key(self, id: str) -> Optional[str]:
        """Creates a new API Key for this application to access a subaccount."""
        resp = self._request(
            f"/subaccounts/{id}/apikeys",
            method="POST",
        )
        return resp.headers.get("Location")

    def delete_subaccount_key(self, account_id: str, api_key: str) -> bool:
        """Uninstalls this application from a subaccount, returning True if successful."""
        resp = self._request(
            f"/subaccounts/{account_id}/apikeys/{api_key}",
            method="DELETE",
        )
        return resp.status_code == 204

from .core import BookeoAPI
from .request import BookeoRequestException
from .schemas import BookeoPagination, BookeoSubaccount


class BookeoSubaccounts(BookeoAPI):

    def get_subaccounts(
        self,
        nav_token: str = None,
        page_number: int = None,
        items_per_page: int = None,
    ) -> tuple[list[BookeoSubaccount], BookeoPagination]:
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
            raise BookeoRequestException("Could not get subaccounts.", resp.request.url)
        data = resp.json()
        accounts = [BookeoSubaccount(**a) for a in data["data"]]
        info = data["info"]
        pager = BookeoPagination(**info)
        return (accounts, pager)

    def create_new_subaccount_key(self, id: str) -> str:
        """Creates a new API Key for this application to access a subaccount."""
        if id is None:
            raise TypeError("id cannot be None.")
        resp = self._request(
            f"/subaccounts/{id}/apikeys",
            method="POST",
        )
        if resp.status_code != 201:
            raise BookeoRequestException(
                f"Could not create new API key for subaccount with id {id}.",
                resp.request.url,
            )
        return resp.headers["Location"]

    def delete_subaccount_key(self, account_id: str, api_key: str) -> None:
        """Uninstalls this application from a subaccount."""
        if account_id is None:
            raise TypeError("account_id cannot be None.")
        if api_key is None:
            raise TypeError("api_key cannot be None.")
        resp = self._request(
            f"/subaccounts/{account_id}/apikeys/{api_key}",
            method="DELETE",
        )
        if resp.status_code != 204:
            raise BookeoRequestException(
                f"Could not delete application from subaccount with id {id}.",
                resp.request.url,
            )
        return

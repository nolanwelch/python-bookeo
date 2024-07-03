from typing import Optional

from .client import BookeoClient
from .core import BookeoAPI
from .request import BookeoRequestException
from .schemas import BookeoSubaccount


class BookeoSubaccountException(BookeoRequestException):
    def __init__(self, error_msg):
        self.error_msg = error_msg

    def __str__(self):
        return self.error_msg


class BookeoSubaccounts(BookeoAPI):
    # TODO: Write this method
    def get_subaccounts(self) -> list[BookeoSubaccount]:
        """Returns a list of all subaccounts in the portal."""
        resp = self.client.request("/subaccounts")

    def create_new_subaccount_key(self, subaccountId: str) -> Optional[str]:
        """Creates a new API Key for this application to access a subaccount."""
        resp = self.client.request(
            f"/subaccounts/{subaccountId}/apikeys", method="POST"
        )
        return resp.headers.get("Location")

    def delete_subaccount_key(self, subaccountId: str, apiKey: str) -> bool:
        """Uninstalls this application from a subaccount.
        Returns True if successful, otherwise False."""
        resp = self.client.request(
            f"/subaccounts/{subaccountId}/apikeys/{apiKey}", method="DELETE"
        )
        return resp.status_code == 204

import requests

from .availability import BookeoAvailability
from .bookings import BookeoBookings
from .customers import BookeoCustomers
from .holds import BookeoHolds
from .payments import BookeoPayments
from .request import BookeoRequest
from .resourceblocks import BookeoResourceBlocks
from .seatblocks import BookeoSeatblocks
from .settings import BookeoSettings
from .setup import VERSION
from .subaccounts import BookeoSubaccounts
from .webhooks import BookeoWebhooks


class BookeoClientException(Exception):
    def __init__(self, error_msg):
        self.error_msg = error_msg

    def __str__(self):
        return self.error_msg


class BookeoClient:
    def __init__(self, secret_key: str, api_key: str):
        if secret_key is None or api_key is None:
            raise BookeoClientException("Must initialize secret_key and api_key")
        self._secret_key = secret_key
        self._api_key = api_key
        # API modules
        self.availability = BookeoAvailability(self)
        self.bookings = BookeoBookings(self)
        self.customers = BookeoCustomers(self)
        self.holds = BookeoHolds(self)
        self.payments = BookeoPayments(self)
        self.resourceblocks = BookeoResourceBlocks(self)
        self.seatblocks = BookeoSeatblocks(self)
        self.settings = BookeoSettings(self)
        self.subaccounts = BookeoSubaccounts(self)
        self.webhooks = BookeoWebhooks(self)

    def query_dict(self) -> dict:
        """Returns the base query dictionary for Bookeo API requests."""
        return {"secretKey": self._secret_key, "apiKey": self._api_key}

    def base_url(self) -> str:
        """Returns the base URL for Bookeo API requests."""
        return "https://api.bookeo.com/v2"

    def headers(self) -> dict:
        """Returns the standard headers for Bookeo API requests."""
        return {
            "Cache-Control": "no-cache",
            "User-Agent": f"PythonBookeo/{VERSION}",
            "Accept": "text/html,application/json",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
        }

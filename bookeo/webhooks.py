from typing import Optional

from .core import BookeoAPI
from .request import BookeoRequestException
from .schemas import (
    BookeoPagination,
    BookeoWebhook,
    BookeoWebhookDomain,
    BookeoWebhookType,
)


class BookeoWebhookException(BookeoRequestException):
    def __init__(self, error_msg):
        self.error_msg = error_msg

    def __str__(self):
        return self.error_msg


class BookeoWebhooks(BookeoAPI):
    def get_webhooks(self) -> Optional[tuple[str, BookeoWebhook]]:
        """Retrieves and returns all webhooks for this API key."""
        resp = self._request("/webhooks")
        if resp.status_code != 200:
            return None
        info = resp["info"]
        webhooks = [BookeoWebhook.from_dict(payment) for payment in info["data"]]
        pager = BookeoPagination.from_dict(info)
        return (webhooks, pager)

    def create_webhook(
        self, url: str, domain: BookeoWebhookDomain, webhook_type: BookeoWebhookType
    ) -> Optional[str]:
        """Creates a new webhook, returning the resource URI if successful."""
        resp = self._request(
            "/webhooks",
            data={
                "url": url,
                "domain": domain,
                "type": webhook_type,
            },
            method="POST",
        )
        return resp.headers.get("Location")

    def get_webhook(self, id: str) -> Optional[BookeoWebhook]:
        """Retrieves the webhook with the specified id. Returns a BookeoWebhook if successful."""
        resp = self._request(f"/webhooks{id}")
        if resp.status_code != 200:
            return None
        return BookeoWebhook.from_dict(resp.json())

    def delete_webhook(self, id) -> bool:
        """Deletes the webhook with the specified id, returning True if successful."""
        resp = self._request(f"/webhooks/{id}", method="DELETE")
        return resp.status_code == 204

from typing import Optional

from .client import BookeoClient
from .core import BookeoAPI, dt_from_bookeo_str
from .request import BookeoRequestException
from .schemas import BookeoWebhook, BookeoWebhookDomain, BookeoWebhookType


class BookeoWebhookException(BookeoRequestException):
    def __init__(self, error_msg):
        self.error_msg = error_msg

    def __str__(self):
        return self.error_msg


class BookeoWebhooks(BookeoAPI):
    def get_webhooks(self) -> list[BookeoWebhook]:
        """Retrieves and returns all webhooks for this API key."""
        resp = self.client.request(self.client, "/webhooks")
        data = resp.json()
        if data is None:
            return []

        # TODO: implement get_webhooks()
        webhooks = []

    def get_webhook(self, id: str) -> Optional[BookeoWebhook]:
        """Retrieves the webhook with the specified id. Returns a BookeoWebhook if successful."""
        if id is None:
            raise BookeoWebhookException("id cannot be None")

        resp = self.client.request(self.client, "/webhooks", params={"webhookId": id})
        data = resp.json()
        if not isinstance(data, dict):
            return None

        return BookeoWebhook(
            data.get("id"),
            data.get("url"),
            BookeoWebhookDomain.from_str(data.get("domain")),
            BookeoWebhookType.from_str(data.get("type")),
            dt_from_bookeo_str(data.get("blockedTime")),
            data.get("blockedReason"),
        )

    def create_webhook(
        self, url: str, domain: BookeoWebhookDomain, type: BookeoWebhookType
    ) -> Optional[str]:
        """Creates a new webhook. Returns the resource URI if successful."""
        data = {"url": url, "domain": domain, "type": type}
        resp = self.client.request(self.client, "/webhooks", data=data, method="POST")
        headers = resp.headers
        return headers.get("Location")

    def delete_webhook(self, id) -> bool:
        """Deletes the webhook with the specified id. Returns True iff successful."""
        resp = self.client.request(
            self.client, "/webhooks", params={"id": id}, method="DELETE"
        )
        return resp.status_code == 204

from .client import BookeoClient, BookeoRequestException
from .schemas import (
    BookeoPagination,
    BookeoWebhook,
    BookeoWebhookDomain,
    BookeoWebhookType,
)


class BookeoWebhooks(BookeoClient):

    def get_webhooks(self) -> tuple[list[BookeoWebhook], BookeoPagination]:
        """Retrieves and returns all webhooks for this API key."""
        resp = self._request("/webhooks")
        if resp.status_code != 200:
            raise BookeoRequestException("Could not get webhooks.", resp.request.url)
        data = resp.json()
        webhooks = [BookeoWebhook(**wh) for wh in data["data"]]
        info = data["info"]
        pager = BookeoPagination(**info)
        return (webhooks, pager)

    def create_webhook(
        self, url: str, domain: BookeoWebhookDomain, webhook_type: BookeoWebhookType
    ) -> str:
        """Creates a new webhook, returning the resource URI."""
        if url is None:
            raise TypeError("url cannot be None.")
        if domain is None:
            raise TypeError("domain cannot be None.")
        if webhook_type is None:
            raise TypeError("webhook_type cannot be None.")
        resp = self._request(
            "/webhooks",
            data={
                "url": url,
                "domain": domain,
                "type": webhook_type,
            },
            method="POST",
        )
        if resp.status_code != 200:
            raise BookeoRequestException(
                "Could not create specified webhook.", resp.request.url
            )
        return resp.headers["Location"]

    def get_webhook(self, id: str) -> BookeoWebhook:
        """Retrieves the webhook with the specified id.."""
        if id is None:
            raise TypeError("id cannot be None.")
        resp = self._request(f"/webhooks{id}")
        if resp.status_code != 200:
            raise BookeoRequestException(
                f"Could not get webhook with id {id}.", resp.request.url
            )
        data = resp.json()
        return BookeoWebhook(**data)

    def delete_webhook(self, id: str) -> None:
        """Deletes the webhook with the specified id."""
        if id is None:
            raise TypeError("id cannot be None.")
        resp = self._request(f"/webhooks/{id}", method="DELETE")
        if resp.status_code != 204:
            raise BookeoRequestException(
                f"Could not delete webhook with id {id}.", resp.request.url
            )
        return

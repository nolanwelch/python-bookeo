from datetime import datetime

from .core import BookeoAPI, dt_to_bookeo_timestamp
from .request import BookeoRequestException
from .schemas import BookeoPagination, BookeoPayment, BookeoPaymentMethod


class BookeoPayments(BookeoAPI):

    def get_payments_received(
        self,
        payment_method: BookeoPaymentMethod = None,
        payment_method_other: str = None,
        start_time: datetime = None,
        end_time: datetime = None,
        items_per_page: int = None,
        nav_token: str = None,
        page_number: int = None,
    ) -> tuple[list[BookeoPayment], BookeoPagination]:
        """Get a list of payments received."""
        resp = self._request(
            "/payments",
            params={
                "paymentMethod": payment_method,
                "paymentMethodOther": payment_method_other,
                "startTime": dt_to_bookeo_timestamp(start_time),
                "endTime": dt_to_bookeo_timestamp(end_time),
                "itemsPerPage": items_per_page,
                "pageNavigationToken": nav_token,
                "pageNumber": page_number,
            },
        )
        if resp.status_code != 200:
            raise BookeoRequestException(
                "Could not get payments received.", resp.request.url
            )
        data = resp.json()
        payments = [BookeoPayment(**payment) for payment in data["data"]]
        info = data["info"]
        pager = BookeoPagination(**info)
        return (payments, pager)

    def get_payment(self, id: str):
        """Retrieve a specific payment."""
        if id is None:
            raise TypeError("id cannot be None.")
        resp = self._request(f"/payments/{id}")
        if resp.status_code != 200:
            raise BookeoRequestException(
                f"Could not get payment with id {id}.", resp.request.url
            )
        data = resp.json()
        return BookeoPayment(**data)

from datetime import datetime
from typing import Optional

from .core import BookeoAPI, bookeo_timestamp_from_dt
from .schemas import BookeoPagination, BookeoPayment, BookeoPaymentMethod


class BookeoPayments(BookeoAPI):
    def get_payments_received(
        self,
        payment_method: Optional[BookeoPaymentMethod],
        payment_method_other: Optional[str],
        start_time: Optional[datetime],
        end_time: Optional[datetime],
        items_per_page: Optional[int],
        nav_token: Optional[str],
        page_number: Optional[int],
    ) -> tuple[list[BookeoPayment], Optional[BookeoPagination]]:
        """Get a list of payments received."""
        resp = self._request(
            "/payments",
            params={
                "paymentMethod": payment_method,
                "paymentMethodOther": payment_method_other,
                "startTime": bookeo_timestamp_from_dt(start_time),
                "endTime": bookeo_timestamp_from_dt(end_time),
                "itemsPerPage": items_per_page,
                "pageNavigationToken": nav_token,
                "pageNumber": page_number,
            },
        )
        info = resp["info"]
        payments = [BookeoPayment.from_dict(payment) for payment in info["data"]]
        pager = BookeoPagination.from_dict(info)
        return (payments, pager)

    def get_payment(self, id: str):
        """Retrieve a specific payment."""
        resp = self._request(f"/payments/{id}")
        return BookeoPayment.from_dict(resp.json())

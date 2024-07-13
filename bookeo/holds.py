from datetime import datetime

from .client import BookeoClient, BookeoRequestException, dt_to_bookeo_timestamp
from .schemas import (
    BookeoBookingOption,
    BookeoCustomer,
    BookeoHold,
    BookeoParticipants,
    BookeoPayment,
    BookeoPriceAdjustment,
    BookeoResource,
)


class BookeoHolds(BookeoClient):

    def create_hold(
        self,
        product_id: str,
        resources: list[BookeoResource],
        participants: BookeoParticipants,
        hold_duration_secs: int = None,
        previous_hold_id: str = None,
        event_id: str = None,
        first_course_enrolled_event_id: str = None,
        dropin_course_enrolled_event_id: str = None,
        start_time: datetime = None,
        end_time: datetime = None,
        customer_id: str = None,
        customer: BookeoCustomer = None,
        external_ref: str = None,
        source_ip: str = None,
        private_event: bool = None,
        source: str = None,
        initial_payments: list[BookeoPayment] = [],
        gift_voucher_codes: list[str] = [],
        promotion_codes: list[str] = [],
        options: list[BookeoBookingOption] = [],
        price_adjustments: list[BookeoPriceAdjustment] = [],
    ) -> tuple[str, BookeoHold]:
        if product_id is None:
            raise TypeError("product_id cannot be None.")
        if resources is None:
            raise TypeError("resources cannot be None.")
        if participants is None:
            raise TypeError("participants cannot be None.")
        resp = self._request(
            "/holds",
            params={
                "holdDurationSeconds": hold_duration_secs,
                "previousHoldId": previous_hold_id,
            },
            data={
                "eventId": event_id,
                "firstCourseEnrolledEventId": first_course_enrolled_event_id,
                "dropinCourseEnrolledEventId": dropin_course_enrolled_event_id,
                "startTime": dt_to_bookeo_timestamp(start_time),
                "endTime": dt_to_bookeo_timestamp(end_time),
                "customerId": customer_id,
                "customer": customer,
                "externalRef": external_ref,
                "participants": participants.model_dump(),
                "resources": [r.model_dump() for r in resources],
                "sourceIp": source_ip,
                "productId": product_id,
                "options": [o.model_dump() for o in options],
                "privateEvent": private_event,
                "priceAdjustments": [pa.model_dump() for pa in price_adjustments],
                "promotionCodeInput": ",".join(promotion_codes),
                "giftVoucherCodeInput": ",".join(gift_voucher_codes),
                "initialPayments": [ip.model_dump() for ip in initial_payments],
                "source": source,
            },
            method="POST",
        )
        if resp.status_code != 201:
            raise BookeoRequestException(
                "Could not create specified hold.", resp.request.url
            )
        location = resp.headers["Location"]
        data = resp.json()
        return (location, BookeoHold(**data))

    def get_hold(self, id: str) -> BookeoHold:
        """Retrieves a previously-generated hold by its id."""
        if id is None:
            raise TypeError("id cannot be None.")
        resp = self._request(f"/holds/{id}")
        data = resp.json()
        if resp.status_code != 200:
            raise BookeoRequestException(
                f"Could not get hold with id {id}.", resp.request.url
            )
        return BookeoHold(**data)

    def delete_hold(self, id: str) -> None:
        """Delete a temporary hold previously created.."""
        if id is None:
            raise TypeError("id cannot be None.")
        resp = self._request(f"/holds/{id}", method="DELETE")
        if resp.status_code != 204:
            raise BookeoRequestException(
                f"Could not delete hold with id {id}.", resp.request.url
            )
        return

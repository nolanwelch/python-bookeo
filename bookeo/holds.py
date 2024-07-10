from datetime import datetime
from typing import Optional

from .core import BookeoAPI, bookeo_timestamp_to_dt, dt_to_bookeo_timestamp
from .schemas import (
    BookeoBookingOption,
    BookeoCustomer,
    BookeoHold,
    BookeoMoney,
    BookeoParticipants,
    BookeoPayment,
    BookeoPrice,
    BookeoPriceAdjustment,
    BookeoResource,
)


class BookeoHolds(BookeoAPI):
    def create_hold(
        self,
        product_id: str,
        resources: list[BookeoResource],
        participants: BookeoParticipants,
        hold_duration_secs: Optional[int],
        previous_hold_id: Optional[str],
        event_id: Optional[str],
        first_course_enrolled_event_id: Optional[str],
        dropin_course_enrolled_event_id: Optional[str],
        start_time: Optional[datetime],
        end_time: Optional[datetime],
        customer_id: Optional[str],
        customer: Optional[BookeoCustomer],
        external_ref: Optional[str],
        source_ip: Optional[str],
        options: Optional[list[BookeoBookingOption]],
        private_event: Optional[bool],
        price_adjustments: Optional[list[BookeoPriceAdjustment]],
        promotion_codes: Optional[list[str]],
        gift_voucher_codes: Optional[list[str]],
        initial_payments: Optional[list[BookeoPayment]],
        source: Optional[str],
    ) -> tuple[Optional[str], Optional[BookeoHold]]:
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
        location = resp.headers.get("Location")
        data = resp.json()
        return (location, BookeoHold(**data))

    def get_hold(self, id: str) -> Optional[BookeoHold]:
        """Retrieves a previously-generated hold by its id."""
        resp = self._request(f"/holds/{id}")
        data = resp.json()
        if resp.status_code != 200 or not isinstance(data, dict):
            return None
        return BookeoHold(**data)

    def delete_hold(self, id: str) -> bool:
        """Delete a temporary hold previously created. Returns True iff successful."""
        resp = self._request(f"/holds/{id}", method="DELETE")
        return resp.status_code == 204

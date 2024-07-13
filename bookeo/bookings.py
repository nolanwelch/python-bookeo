from datetime import datetime

from .client import BookeoClient, BookeoRequestException, dt_to_bookeo_timestamp
from .schemas import (
    BookeoBooking,
    BookeoBookingOption,
    BookeoCustomer,
    BookeoPagination,
    BookeoParticipant,
    BookeoPayment,
    BookeoPriceAdjustment,
    BookeoResource,
)


class BookeoBookings(BookeoClient):

    def create_booking(
        self,
        product_id: str,
        participants: list[BookeoParticipant],
        previous_hold_id: str = None,
        notify_users: bool = None,
        notify_customer: bool = None,
        send_customer_reminders: bool = None,
        send_customer_thankyou: bool = None,
        mode: str = None,
        event_id: str = None,
        first_course_enrolled_event_id: str = None,
        dropin_course_enrolled_event_id: str = None,
        start_time: datetime = None,
        end_time: datetime = None,
        customer_id: str = None,
        customer: BookeoCustomer = None,
        external_ref: str = None,
        resources: list[BookeoResource] = [],
        source_ip: str = None,
        options: list[BookeoBookingOption] = [],
        private_event: bool = None,
        price_adjustments: list[BookeoPriceAdjustment] = [],
        promotion_code_input: str = None,
        gift_voucher_code_input: str = None,
        initial_payments: list[BookeoPayment] = [],
        source: str = None,
    ) -> tuple[str, BookeoBooking]:
        if product_id is None:
            raise TypeError("product_id cannot be None.")
        if not participants:
            raise ValueError("participants cannot be empty.")
        resp = self._request(
            "/bookings",
            params={
                "previousHoldId": previous_hold_id,
                "notifyUsers": notify_users,
                "notifyCustomer": notify_customer,
                "sendCustomerReminders": send_customer_reminders,
                "sendCustomerThankyou": send_customer_thankyou,
                "mode": mode,
            },
            data={
                "eventId": event_id,
                "firstCourseEnrolledEventId": first_course_enrolled_event_id,
                "dropinCourseEnrolledEventId": dropin_course_enrolled_event_id,
                "startTime": dt_to_bookeo_timestamp(start_time),
                "endTime": dt_to_bookeo_timestamp(end_time),
                "customerId": customer_id,
                "customer": customer.model_dump(),
                "externalRef": external_ref,
                "participants": [p.model_dump() for p in participants],
                "resources": [r.model_dump() for r in resources],
                "sourceIp": source_ip,
                "productId": product_id,
                "options": options,
                "privateEvent": private_event,
                "priceAdjustments": [pa.model_dump() for pa in price_adjustments],
                "promotionCodeInput": promotion_code_input,
                "giftVoucherCodeInput": gift_voucher_code_input,
                "initialPayments": [ip.model_dump() for ip in initial_payments],
                "source": source,
            },
            method="POST",
        )
        if resp.status_code != 201:
            raise BookeoRequestException(
                f"Could not create booking for product with id {product_id}.",
                resp.request.url,
            )
        location = resp.headers["Location"]
        data = resp.json()
        return (location, BookeoBooking(**data))

    def get_bookings(
        self,
        start_time: datetime = None,
        end_time: datetime = None,
        last_updated_start_time: datetime = None,
        last_updated_end_time: datetime = None,
        product_id: str = None,
        nav_token: str = None,
        include_canceled: bool = False,
        expand_customer: bool = False,
        expand_participants: bool = False,
        items_per_page: int = 50,
        page_number: int = 1,
    ) -> tuple[list[BookeoBooking], BookeoPagination]:
        resp = self._request(
            "/bookings",
            params={
                "startTime": dt_to_bookeo_timestamp(start_time),
                "endTime": dt_to_bookeo_timestamp(end_time),
                "lastUpdatedStartTime": dt_to_bookeo_timestamp(last_updated_start_time),
                "lastUpdatedEndTime": dt_to_bookeo_timestamp(last_updated_end_time),
                "productId": product_id,
                "includeCanceled": include_canceled,
                "expandCustomer": expand_customer,
                "expandParticipants": expand_participants,
                "itemsPerPage": items_per_page,
                "pageNavigationToken": nav_token,
                "pageNumber": page_number,
            },
        )
        if resp.status_code != 200:
            raise BookeoRequestException("Could not get bookings.", resp.request.url)
        data = resp.json()
        bookings = [BookeoBooking(**b) for b in data["data"]]
        info = data["info"]
        pager = BookeoPagination(**info)
        return (bookings, pager)

    def get_booking(
        self,
        booking_number: str,
        expand_customer: bool = False,
        expand_participants: bool = False,
    ) -> BookeoBooking:
        if booking_number is None:
            raise TypeError("booking_number cannot be None.")
        resp = self._request(
            f"/bookings/{booking_number}",
            params={
                "expandCustomer": expand_customer,
                "expandParticipants": expand_participants,
            },
        )
        if resp.status_code != 200:
            raise BookeoRequestException(
                f"Could not get booking with id {id}.", resp.request.url
            )
        data = resp.json()
        return BookeoBooking(**data)

    def update_booking(
        self,
        booking_number: str,
        product_id: str,
        participants: list[BookeoParticipant],
        notify_users: bool = None,
        notify_customer: bool = None,
        mode: str = None,
        event_id: str = None,
        first_course_enrolled_event_id: str = None,
        dropin_course_enrolled_event_id: str = None,
        start_time: datetime = None,
        end_time: datetime = None,
        customer_id: str = None,
        customer: BookeoCustomer = None,
        external_ref: str = None,
        resources: list[BookeoResource] = [],
        source_ip: str = None,
        options: list[BookeoBookingOption] = [],
        private_event: bool = None,
        price_adjustments: list[BookeoPriceAdjustment] = [],
        promotion_code_input: str = None,
        gift_voucher_code_input: str = None,
        initial_payments: list[BookeoPayment] = [],
        source: str = None,
    ) -> tuple[str, BookeoBooking]:
        if booking_number is None:
            raise TypeError("booking_number cannot be None.")
        if product_id is None:
            raise TypeError("product_id cannot be None.")
        if not participants:
            raise ValueError("participants cannot be empty.")
        resp = self._request(
            f"/bookings/{booking_number}",
            params={
                "notifyUsers": notify_users,
                "notifyCustomer": notify_customer,
                "mode": mode,
            },
            data={
                "eventId": event_id,
                "firstCourseEnrolledEventId": first_course_enrolled_event_id,
                "dropinCourseEnrolledEventId": dropin_course_enrolled_event_id,
                "startTime": dt_to_bookeo_timestamp(start_time),
                "endTime": dt_to_bookeo_timestamp(end_time),
                "customerId": customer_id,
                "customer": customer.model_dump(),
                "externalRef": external_ref,
                "participants": [p.model_dump() for p in participants],
                "resources": [r.model_dump() for r in resources],
                "sourceIp": source_ip,
                "productId": product_id,
                "options": [o.model_dump() for o in options],
                "privateEvent": private_event,
                "priceAdjustments": [pa.model_dump() for pa in price_adjustments],
                "promotionCodeInput": promotion_code_input,
                "giftVoucherCodeInput": gift_voucher_code_input,
                "initialPayments": [ip.model_dump() for ip in initial_payments],
                "source": source,
            },
            method="PUT",
        )
        if resp.status_code != 200:
            raise BookeoRequestException(
                f"Could not update booking with id {booking_number}.", resp.request.url
            )
        location = resp.headers["Location"]
        data = resp.json()
        return (location, BookeoBooking(**data))

    def cancel_booking(
        self,
        booking_number: str,
        reason: str = None,
        notify_users: bool = None,
        notify_customer: bool = None,
        apply_cancellation_policy: bool = None,
        track_in_customer_history: bool = None,
        cancel_remaining_series: bool = None,
    ) -> None:
        if booking_number is None:
            raise TypeError("booking_number cannot be None.")
        resp = self._request(
            f"/bookings/{booking_number}",
            params={
                "reason": reason,
                "notifyUsers": notify_users,
                "notifyCustomer": notify_customer,
                "applyCancellationPolicy": apply_cancellation_policy,
                "trackInCustomerHistory": track_in_customer_history,
                "cancelRemainingSeries": cancel_remaining_series,
            },
            method="DELETE",
        )
        if resp.status_code != 204:
            raise BookeoRequestException(
                f"Could not delete booking with id {id}.", resp.request.url
            )
        return

    def add_booking_payment(
        self, booking_number: str, payment: BookeoPayment
    ) -> tuple[str, BookeoPayment]:
        if booking_number is None:
            raise TypeError("booking_number cannot be None.")
        if payment is None:
            raise TypeError("payment cannot be None.")
        resp = self._request(
            f"/bookings/{booking_number}/payments",
            data=payment.model_dump(),
            method="POST",
        )
        if resp.status_code != 201:
            raise BookeoRequestException(
                f"Could not add payment to booking with id {booking_number}.",
                resp.request.url,
            )
        location = resp.headers["Location"]
        data = resp.json()
        return (location, BookeoBooking(**data))

    def get_received_payments(
        self,
        booking_number: str,
        items_per_page: int = 50,
        nav_token: str = None,
        page_number: int = 1,
    ) -> tuple[list[BookeoPayment], BookeoPagination]:
        if booking_number is None:
            raise TypeError("booking_number cannot be None.")
        resp = self._request(
            f"/bookings/{booking_number}/payments",
            params={
                "itemsPerPage": items_per_page,
                "pageNavigationToken": nav_token,
                "pageNumber": page_number,
            },
        )
        if resp.status_code != 200:
            raise BookeoRequestException(
                f"Could not get received payments for booking with id {booking_number}.",
                resp.request.url,
            )
        data = resp.json()
        payments = [BookeoPayment(**p) for p in data["data"]]
        info = data["info"]
        pager = BookeoPagination(**info)
        return (payments, pager)

    def get_customer(self, booking_number: str) -> BookeoCustomer:
        if booking_number is None:
            raise TypeError("booking_number cannot be None.")
        resp = self._request(f"/bookings/{booking_number}/customer")
        if resp.status_code != 200:
            raise BookeoRequestException(
                f"Could not get customer for booking with id {booking_number}.",
                resp.request.url,
            )
        data = resp.json()
        return BookeoCustomer(**data)

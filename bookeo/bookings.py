from datetime import datetime
from typing import Optional

import requests

from .core import BookeoAPI
from .schemas import (
    BookeoBooking,
    BookeoBookingOption,
    BookeoCustomer,
    BookeoMoney,
    BookeoPagination,
    BookeoParticipant,
    BookeoPayment,
    BookeoPaymentMethod,
    BookeoPriceAdjustment,
    BookeoResource,
)


class BookeoBookings(BookeoAPI):
    def create_booking(
        self,
        productId: str,
        participants: list[BookeoParticipant],
        previousHoldId: Optional[str],
        notifyUsers: Optional[bool],
        notifyCustomer: Optional[bool],
        sendCustomerReminders: Optional[bool],
        sendCustomerThankyou: Optional[bool],
        mode: Optional[str],
        eventId: Optional[str],
        firstCourseEnrolledEventId: Optional[str],
        dropinCourseEnrolledEventId: Optional[str],
        startTime: Optional[datetime],
        endTime: Optional[datetime],
        customerId: Optional[str],
        customer: Optional[BookeoCustomer],
        externalRef: Optional[str],
        resources: Optional[list[BookeoResource]],
        sourceIp: Optional[str],
        options: Optional[list[BookeoBookingOption]],
        privateEvent: Optional[bool],
        priceAdjustments: Optional[list[BookeoPriceAdjustment]],
        promotionCodeInput: Optional[str],
        giftVoucherCodeInput: Optional[str],
        initialPayments: Optional[list[BookeoPayment]],
        source: Optional[str],
    ) -> Optional[BookeoBooking]:
        resp = self._request(
            "/bookings",
            params={
                "previousHoldId": previousHoldId,
                "notifyUsers": notifyUsers,
                "notifyCustomer": notifyCustomer,
                "sendCustomerReminders": sendCustomerReminders,
                "sendCustomerThankyou": sendCustomerThankyou,
                "mode": mode,
            },
            data={
                "eventId": eventId,
                "firstCourseEnrolledEventId": firstCourseEnrolledEventId,
                "dropinCourseEnrolledEventId": dropinCourseEnrolledEventId,
                "startTime": startTime,
                "endTime": endTime,
                "customerId": customerId,
                "customer": customer,
                "externalRef": externalRef,
                "participants": participants,
                "resources": resources,
                "sourceIp": sourceIp,
                "productId": productId,
                "options": options,
                "privateEvent": privateEvent,
                "priceAdjustments": priceAdjustments,
                "promotionCodeInput": promotionCodeInput,
                "giftVoucherCodeInput": giftVoucherCodeInput,
                "initialPayments": initialPayments,
                "source": source,
            },
            method="POST",
        )
        if resp.status_code != 201:
            return None
        location = resp.headers.get("Location")
        data = resp.json()
        return (location, BookeoBooking(**data))

    def _retrieve_bookings(
        self,
        startTime: Optional[datetime],
        endTime: Optional[datetime],
        lastUpdatedStartTime: Optional[datetime],
        lastUpdatedEndTime: Optional[datetime],
        productId: Optional[str],
        pageNavigationToken: Optional[str],
        includeCanceled: bool = False,
        expandCustomer: bool = False,
        expandParticipants: bool = False,
        itemsPerPage: int = 50,
        pageNumber: int = 1,
    ) -> list[BookeoBooking]:
        pass

    def retrieve_bookings(self) -> list[BookeoBooking] | None:
        pass

    def retrieve_booking(
        self,
        bookingNumber: str,
        expandCustomer: bool = False,
        expandParticipants: bool = False,
    ) -> BookeoBooking | None:
        if bookingNumber is None:
            raise Exception()  # TODO: Make error more specific

        res = requests.get(
            url=f"https://api.bookeo.com/v2/bookings/{bookingNumber}",
            params={
                "expandCustomer": expandCustomer,
                "expandParticipants": expandParticipants,
            },
            headers=self.__HEADERS,
        )

    def update_booking(
        self,
        bookingNumber: str,
        productId: str,
        participants: list[BookeoParticipant],
        notifyUsers: Optional[bool],
        notifyCustomer: Optional[bool],
        mode: Optional[str],
        eventId: Optional[str],
        firstCourseEnrolledEventId: Optional[str],
        dropinCourseEnrolledEventId: Optional[str],
        startTime: Optional[datetime],
        endTime: Optional[datetime],
        customerId: Optional[str],
        customer: Optional[BookeoCustomer],
        externalRef: Optional[str],
        resources: Optional[list[BookeoResource]],
        sourceIp: Optional[str],
        options: Optional[list[BookeoBookingOption]],
        privateEvent: Optional[bool],
        priceAdjustments: Optional[list[BookeoPriceAdjustment]],
        promotionCodeInput: Optional[str],
        giftVoucherCodeInput: Optional[str],
        initialPayments: Optional[list[BookeoPayment]],
        source: Optional[str],
    ) -> BookeoBooking:
        resp = self._request(
            f"/bookings/{bookingNumber}",
            params={},
            method="PUT",
        )

    def cancel_booking(
        self,
        bookingNumber: str,
        reason: Optional[str],
        notifyUsers: Optional[bool],
        notifyCustomer: Optional[bool],
        applyCancellationPolicy: Optional[bool],
        trackInCustomerHistory: Optional[bool],
        cancelRemainingSeries: Optional[bool],
    ) -> bool:
        resp = self._request(
            f"/bookings/{bookingNumber}",
            params={
                "reason": reason,
                "notifyUsers": notifyUsers,
                "notifyCustomer": notifyCustomer,
                "applyCancellationPolicy": applyCancellationPolicy,
                "trackInCustomerHistory": trackInCustomerHistory,
                "cancelRemainingSeries": cancelRemainingSeries,
            },
            method="DELETE",
        )
        return resp.status_code == 204

    def add_booking_payment(
        self,
        booking_number: str,
        received_time: datetime,
        reason: str,
        amount: BookeoMoney,
        payment_method: BookeoPaymentMethod,
        payment_method_other: Optional[str],
    ) -> Optional[BookeoPayment]:
        resp = self._request(f"/bookings/{booking_number}", data={}, method="POST")
        if resp.status_code != 201:
            return None

    def get_received_payments(
        self, booking_number: str
    ) -> Optional[tuple[list[BookeoPayment], BookeoPagination]]:
        resp = self._request(f"/bookings/{booking_number}/payments")
        if resp.status_code != 200:
            return None
        data = resp.json()
        payments = [BookeoPayment(**s) for s in data["data"]]
        info = data["info"]
        pager = BookeoPagination(**info)
        return (payments, pager)

    def get_customer(self, booking_number: str) -> Optional[BookeoCustomer]:
        resp = self._request(f"/bookings/{booking_number}/customer")
        if resp.status_code != 200:
            return None
        data = resp.json()
        return BookeoCustomer(**data)

from typing import Optional

import requests

from .client import BookeoClient
from .core import BookeoAPI
from .schemas import (
    BookeoBooking,
    BookeoDateTime,
    BookeoParticipant,
    BookingOption,
    Customer,
    Money,
    Payment,
    PaymentMethod,
    PriceAdjustment,
    Resource,
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
        startTime: Optional[BookeoDateTime],
        endTime: Optional[BookeoDateTime],
        customerId: Optional[str],
        customer: Optional[Customer],
        externalRef: Optional[str],
        resources: Optional[list[Resource]],
        options: Optional[list[BookingOption]],
        privateEvent: Optional[bool],
        priceAdjustments: Optional[list[PriceAdjustment]],
        giftVoucherCodeInput: Optional[str],
        initialPayments: Optional[list[Payment]],
        source: Optional[str],
    ) -> BookeoBooking | None:
        if None in (productId, participants) or len(participants) == 0:
            raise Exception()  # TODO: Specify this exception
        pass

    def _retrieve_bookings(
        self,
        startTime: Optional[BookeoDateTime],
        endTime: Optional[BookeoDateTime],
        lastUpdatedStartTime: Optional[BookeoDateTime],
        lastUpdatedEndTime: Optional[BookeoDateTime],
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
        participants: list[Participant],
        notifyUsers: Optional[bool],
        notifyCustomer: Optional[bool],
        mode: Optional[str],
        eventId: Optional[str],
        firstCourseEnrolledEventId: Optional[str],
        dropinCourseEnrolledEventId: Optional[str],
        startTime: Optional[BookeoDateTime],
        endTime: Optional[BookeoDateTime],
        customerId: Optional[str],
        customer: Optional[Customer],
        externalRef: Optional[str],
        resources: Optional[list[Resource]],
        sourceIp: Optional[str],
        options: Optional[list[BookingOption]],
        privateEvent: Optional[bool],
        priceAdjustments: Optional[list[PriceAdjustment]],
        promotionCodeInput: Optional[str],
        giftVoucherCodeInput: Optional[str],
        initialPayments: Optional[list[Payment]],
        source: Optional[str],
    ) -> BookeoBooking:
        if None in (bookingNumber, productId, participants) or len(participants) == 0:
            raise Exception()  # TODO: Specify exception

        res = requests.put(
            url=f"https://api.bookeo.com/v2/bookings/{bookingNumber}",
            params={},
            headers=self.__HEADERS,
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
        if bookingNumber is None:
            raise Exception()  # TODO: Yeah

        res = requests.delete(
            url=f"https://api.bookeo.com/v2/bookings/{bookingNumber}",
            params={
                "reason": reason,
                "notifyUsers": notifyUsers,
                "notifyCustomer": notifyCustomer,
                "applyCancellationPolicy": applyCancellationPolicy,
                "trackInCustomerHistory": trackInCustomerHistory,
                "cancelRemainingSeries": cancelRemainingSeries,
            },
            headers=self.__HEADERS,
        )

    def add_booking_payment(
        self,
        bookingNumber: str,
        receivedTime: BookeoDateTime,
        reason: str,
        amount: Money,
        paymentMethod: PaymentMethod,
        paymentMethodOther: str,
        comment: Optional[str],
    ) -> Payment | None:
        pass

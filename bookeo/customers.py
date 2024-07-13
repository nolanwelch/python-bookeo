import urllib.parse
from datetime import datetime

from .client import BookeoClient, BookeoRequestException, dt_to_bookeo_timestamp
from .schemas import (
    BookeoBooking,
    BookeoCustomer,
    BookeoCustomerSearchField,
    BookeoCustomField,
    BookeoGender,
    BookeoLinkedPerson,
    BookeoPagination,
    BookeoPhoneNumber,
    BookeoStreetAddress,
)


class BookeoCustomers(BookeoClient):

    def get_customers(
        self,
        current_members: bool = True,
        current_non_members: bool = True,
        created_since: datetime = None,
        search_field: BookeoCustomerSearchField = "name",
        search_text: str = None,
        items_per_page: int = None,
        nav_token=None,
        page_number=1,
    ) -> tuple[list[BookeoCustomer], BookeoPagination]:
        resp = self._request(
            "/customers",
            params={
                "currentMembers": current_members,
                "currentNonMembers": current_non_members,
                "createdSince": dt_to_bookeo_timestamp(created_since),
                "searchField": search_field.value,
                "searchText": search_text,
                "items_per_page": items_per_page,
                "pageNavigationToken": nav_token,
                "pageNumber": page_number,
            },
        )
        if resp.status_code != 200:
            raise BookeoRequestException("Could not get customers.", resp.request.url)
        data = resp.json()
        customers = [BookeoCustomer(**c) for c in data["data"]]
        info = data["info"]
        pager = BookeoPagination(**info)
        return (customers, pager)

    def create_new_customer(
        self, customer: BookeoCustomer
    ) -> tuple[str, BookeoCustomer]:
        if customer is None:
            raise TypeError("customer cannot be None.")
        resp = self._request("/customers", data=customer.model_dump(), method="POST")
        if resp.status_code != 201:
            raise BookeoRequestException(
                "Could not create requested customer.", resp.request.url
            )
        location = resp.headers["Location"]
        data = resp.json()
        return (location, BookeoCustomer(**data))

    def get_linked_person(self, customer_id: str, id: str) -> BookeoLinkedPerson:
        if customer_id is None:
            raise TypeError("customer_id cannot be None.")
        if id is None:
            raise TypeError("id cannot be None.")
        resp = self._request(f"/customers/{customer_id}/linkedpeople/{id}")
        if resp.status_code != 200:
            raise BookeoRequestException(
                f"Could not get person with id {id} from customer with id {customer_id}.",
                resp.request.url,
            )
        data = resp.json()
        return BookeoLinkedPerson(**data)

    def update_linked_person(
        self,
        customer_id: str,
        id: str,
        first_name: str = None,
        middle_name: str = None,
        last_name: str = None,
        email: str = None,
        phone_numbers: list[BookeoPhoneNumber] = [],
        street_address: BookeoStreetAddress = None,
        date_of_birth: str = None,
        custom_fields: list[BookeoCustomField] = [],
        gender: BookeoGender = None,
    ) -> None:
        if customer_id is None:
            raise TypeError("customer_id cannot be None.")
        if id is None:
            raise TypeError("id cannot be None.")
        resp = self._request(
            f"/customers/{customer_id}/linkedpeople/{id}",
            data={
                "firstName": first_name,
                "middleName": middle_name,
                "lastName": last_name,
                "emailAddress": email,
                "phoneNumbers": [pn.model_dump() for pn in phone_numbers],
                "streetAddress": street_address.model_dump(),
                "dateOfBirth": date_of_birth,
                "customFields": [cf.model_dump() for cf in custom_fields],
                "gender": gender.value,
            },
            method="PUT",
        )
        if resp.status_code != 200:
            raise BookeoRequestException(
                f"Could not update information of person with id {id} from customer with id {customer_id}.",
                resp.request.url,
            )
        return

    def delete_linked_person(self, customer_id: str, id: str) -> None:
        if customer_id is None:
            raise TypeError("customer_id cannot be None.")
        if id is None:
            raise TypeError("id cannot be None.")
        resp = self._request(
            f"/customers/{customer_id}/linkedpeople/{id}", method="DELETE"
        )
        if resp.status_code != 204:
            raise BookeoRequestException(
                f"Could not delete person with id {id} from customer with id {customer_id}.",
                resp.request.url,
            )
        return

    def get_customer(self, id: str) -> BookeoCustomer:
        if id is None:
            raise TypeError("id cannot be None.")
        resp = self._request(f"/customers/{id}")
        if resp.status_code != 200:
            raise BookeoRequestException(
                f"Could not get customer with id {id}.", resp.request.url
            )
        data = resp.json()
        return BookeoCustomer(**data)

    def update_customer(
        self,
        id: str,
        first_name: str = None,
        middle_name: str = None,
        last_name: str = None,
        email: str = None,
        phone_numbers: list[BookeoPhoneNumber] = [],
        street_address: BookeoStreetAddress = None,
        date_of_birth: str = None,
        custom_fields: list[BookeoCustomField] = [],
        gender: BookeoGender = None,
        facebook_id: str = None,
        language_code: str = None,
        accept_sms_reminders: bool = None,
    ) -> tuple[str, BookeoCustomer]:
        if id is None:
            raise TypeError("id cannot be None.")
        resp = self._request(
            f"/customers/{id}",
            data={
                "firstName": first_name,
                "middleName": middle_name,
                "lastName": last_name,
                "emailAddress": email,
                "phoneNumbers": [pn.model_dump() for pn in phone_numbers],
                "streetAddress": street_address.model_dump(),
                "dateOfBirth": date_of_birth,
                "customFields": [cf.model_dump() for cf in custom_fields],
                "gender": gender.value,
                "facebookId": facebook_id,
                "languageCode": language_code,
                "acceptSmsReminders": accept_sms_reminders,
            },
            method="PUT",
        )
        if resp.status_code != 200:
            raise BookeoRequestException(
                f"Could not update customer with id {id}.", resp.request.url
            )
        location = resp.headers["Location"]
        data = resp.json()
        return (location, BookeoCustomer(**data))

    def delete_customer(self, id: str) -> None:
        if id is None:
            raise TypeError("id cannot be None.")
        resp = self._request(f"/customers/{id}", method="DELETE")
        if resp.status_code != 204:
            raise BookeoRequestException(
                f"Could not delete customer with id {id}.", resp.request.url
            )
        return

    def check_customer_password(self, id: str, password: str) -> bool:
        if id is None:
            raise TypeError("id cannot be None.")
        if password is None:
            raise TypeError("password cannot be None.")
        resp = self._request(
            f"/customers/{id}/authenticate",
            params={"password": urllib.parse.quote(password)},
        )
        match resp.status_code:
            case 200:
                return True
            case 403:
                return False
            case _:
                raise BookeoRequestException(
                    f"Could not validate password for customer with id {id}.",
                    resp.request.url,
                )

    def get_customer_bookings(
        self,
        id: str,
        begin_date: datetime = None,
        end_date: datetime = None,
        expand_participants: bool = False,
        items_per_page: int = 50,
        nav_token: str = None,
        page_number: int = 1,
    ) -> tuple[list[BookeoBooking], BookeoPagination]:
        if id is None:
            raise TypeError("id cannot be None.")
        resp = self._request(
            f"/customers/{id}/bookings",
            params={
                "beginDate": dt_to_bookeo_timestamp(begin_date),
                "endDate": dt_to_bookeo_timestamp(end_date),
                "expandParticipants": expand_participants,
                "itemsPerPage": items_per_page,
                "pageNavigationToken": nav_token,
                "pageNumber": page_number,
            },
        )
        if resp.status_code != 200:
            raise BookeoRequestException(
                f"Could not get bookings for customer with id {id}.", resp.request.url
            )
        data = resp.json()
        bookings = [BookeoBooking(**b) for b in data["data"]]
        info = data["info"]
        pager = BookeoPagination(**info)
        return (bookings, pager)

    def get_linked_people(
        self,
        id: str,
        items_per_page: int = 50,
        nav_token: str = None,
        page_number: int = 1,
    ) -> tuple[list[BookeoLinkedPerson], BookeoPagination]:
        if id is None:
            raise TypeError("id cannot be None.")
        resp = self._request(
            f"/customers/{id}/linkedpeople",
            params={
                "itemsPerPage": items_per_page,
                "pageNavigationToken": nav_token,
                "pageNumber": page_number,
            },
        )
        if resp.status_code != 200:
            raise BookeoRequestException(
                f"Could not get linked people for customer with id {id}.",
                resp.request.url,
            )
        data = resp.json()
        people = [BookeoLinkedPerson(**p) for p in data["data"]]
        info = data["info"]
        pager = BookeoPagination(**info)
        return (people, pager)

from dataclasses import dataclass
from datetime import date, datetime
from enum import Enum
from typing import Optional

from .core import bookeo_timestamp_to_dt, dt_to_bookeo_timestamp

# Bookeo enumerable types


class BookeoEnum(Enum):
    @classmethod
    def from_str(cls, label: str):
        for sub in cls:
            if sub.value == label:
                return sub
        return None


class BookeoPhoneType(BookeoEnum):
    Mobile = "mobile"
    Work = "work"
    Home = "home"
    Fax = "fax"


class BookeoGender(BookeoEnum):
    Male = "male"
    Female = "female"
    Unknown = "unknown"


class BookeoPaymentMethod(BookeoEnum):
    CreditCard = "creditCard"
    Paypal = "paypal"
    BankTransfer = "bankTransfer"
    Cash = "cash"
    Check = "checque"
    DebitCard = "debitCard"
    ExistingCredit = "existingCredit"
    AccountCredit = "accountCredit"
    MoneyVoucher = "moneyVoucher"
    Other = "other"


class BookeoProductType(BookeoEnum):
    Fixed = "fixed"
    FixedCourse = "fixedCourse"
    FlexibleTime = "flexibleTime"


class BookeoWebhookDomain(BookeoEnum):
    Bookings = "bookings"
    SeatBlocks = "seatblocks"
    ResourceBlocks = "resourceblocks"
    Customers = "customers"
    Payments = "payments"


class BookeoWebhookType(BookeoEnum):
    Created = "created"
    Updated = "updated"
    Deleted = "deleted"


# Object schemas


class BookeoSchema:
    # TODO: Implement this https://stackoverflow.com/a/49003922
    def to_dict(self):
        raise NotImplementedError

    @classmethod
    def from_dict(cls, data: dict):
        raise NotImplementedError


@dataclass
class BookeoAPIKeyInfo:
    """Provides detailed information about the API Key being used."""

    account_id: str
    permissions: list[str]
    creation_time: datetime

    @staticmethod
    # TODO: Implement BookeoAPIKeyInfo.from_dict()
    def from_dict(data: dict):
        raise NotImplementedError
        if data is None:
            return None
        pass


@dataclass
class BookeoPhoneNumber:
    number: str
    phone_type: BookeoPhoneType

    def __repr__(self) -> str:
        return f"BookeoPhoneNumber({self.number} : {self.phone_type})"

    def to_dict(self):
        return {"number": self.number, "type": self.phone_type.value}

    @staticmethod
    def from_dict(data: dict):
        if not isinstance(data, dict):
            return None
        return BookeoPhoneNumber(
            data.get("number"), BookeoPhoneType.from_str(data.get("type"))
        )


@dataclass
class BookeoStreetAddress:
    address_1: Optional[str]
    address_2: Optional[str]
    city: Optional[str]
    country_code: Optional[str]
    state: Optional[str]
    post_code: Optional[str]

    @staticmethod
    def from_dict(data: dict):
        if not isinstance(data, dict):
            return None
        return BookeoStreetAddress(
            data.get("address1"),
            data.get("address2"),
            data.get("city"),
            data.get("countryCode"),
            data.get("state"),
            data.get("postcode"),
        )


@dataclass
class BookeoBusinessInfo:
    id: str
    name: str
    legal_identifiers: Optional[str]
    phone_numbers: list[BookeoPhoneNumber]
    website_url: Optional[str]
    email: Optional[str]
    street_address: BookeoStreetAddress
    logo_url: Optional[str]
    description: Optional[str]

    def __repr__(self) -> str:
        return f"BookeoBusinessInfo({self.id}, {self.name})"


@dataclass
class BookeoBooking:
    """Represents a booking"""

    title: str
    creation_time: datetime
    creation_agent: str
    product_id: str


@dataclass
class BookeoBookingOption:
    value: str
    id: Optional[str]
    name: Optional[str]

    def to_dict(self):
        return {"value": self.value, "id": self.id, "name": self.name}

    @staticmethod
    def from_dict(data: dict):
        return BookeoBookingOption(data["value"], data.get("id"), data.get("name"))


@dataclass
class BookingLimit:
    pass


@dataclass
class Duration:
    pass


@dataclass
class BookeoMoney:
    amount: str
    currency: str

    def to_dict(self):
        return {"amount": self.amount, "currency": self.currency}

    @staticmethod
    def from_dict(data: dict):
        return BookeoMoney(data["amount"], data["currency"])


@dataclass
class BookeoPayment:
    id: str
    creation_time: datetime
    received_time: datetime
    reason: str
    description: Optional[str]
    comment: Optional[str]
    amount: BookeoMoney
    payment_method: BookeoPaymentMethod
    payment_method_other: Optional[str]
    agent: Optional[str]
    customer_id: Optional[str]
    gateway_name: Optional[str]
    transaction_id: Optional[str]

    def to_dict(self):
        return {
            "receivedTime": dt_to_bookeo_timestamp(self.received_time),
            "reason": self.reason,
            "comment": self.comment,
            "amount": self.amount.to_dict(),
            "paymentMethod": self.payment_method.value,
            "paymentMethodOther": self.payment_method_other,
        }

    @staticmethod
    def from_dict(data: dict):
        return BookeoPayment(
            data["id"],
            bookeo_timestamp_to_dt(data["creationTime"]),
            bookeo_timestamp_to_dt(data["receivedTime"]),
            data["reason"],
            data.get("description"),
            data.get("comment"),
            BookeoMoney.from_dict(data["money"]),
            BookeoPaymentMethod.from_str(data["paymentMethod"]),
            data.get("paymentMethodOther"),
            data.get("agent"),
            data.get("customerId"),
            data.get("gatewayName"),
            data.get("transactionId"),
        )


@dataclass
class BookeoPriceAdjustment:
    unit_price: BookeoMoney
    quantity: int
    description: str
    tax_ids: Optional[list[str]]

    def to_dict(self):
        return {
            "unitPrice": self.unit_price.to_dict(),
            "quantity": self.quantity,
            "description": self.description,
            "taxIds": [id for id in self.tax_ids],
        }

    @staticmethod
    def from_dict(data: dict):
        return BookeoPriceAdjustment(
            BookeoMoney.from_dict(data["unitPrice"]),
            data["quantity"],
            data["description"],
            data["taxIds"],
        )


@dataclass
class BookeoProduct:
    name: str
    product_id: str
    product_code: str
    booking_limits: list[BookingLimit]
    duration: Duration
    product_type: BookeoProductType
    members_only: bool
    prepaid_only: bool
    accept_deny: bool
    api_bookings_allowed: bool
    dropin_only: bool


@dataclass
class BookeoTax:
    id: str
    name: str
    enabled: bool


@dataclass
class BookeoPriceTax:
    tax_id: str
    amount: BookeoMoney

    @staticmethod
    def from_dict(data: dict):
        if data is None:
            return None
        return BookeoPriceTax(data["taxId"], data["amount"])


@dataclass
class TelephoneNumber:
    """Describes a phone/fax number"""

    number: str


@dataclass
class BookeoWebhook:
    pass


@dataclass
class BookeoLanguage:
    tag: str
    name: str
    customers_default: bool


@dataclass
class BookeoCustomChoiceValue:
    id: str
    name: str
    description: str


@dataclass
class BookeoCustomField:
    id: str
    name: str
    description: Optional[str]
    shown_to_customers: bool
    for_customer: bool
    for_participants: bool
    index: int


class BookeoChoiceField(BookeoCustomField):
    def __init__(
        self,
        id: str,
        name: str,
        description: Optional[str],
        shownToCustomers: bool,
        forCustomer: bool,
        forParticipants: bool,
        index: int,
        values: list[BookeoCustomChoiceValue],
        defaultValueId: Optional[str],
    ):
        self.values = values
        self.defaultValueId = defaultValueId
        super.__init__(
            id, name, description, shownToCustomers, forCustomer, forParticipants, index
        )


class BookeoNumberField(BookeoCustomField):
    # TODO: Write __init__ to handle input
    def __init__(
        self,
        id: str,
        name: str,
        description: Optional[str],
        shownToCustomers: bool,
        forCustomer: bool,
        forParticipants: bool,
        index: int,
        minValue: int,
        maxValue: int,
        defaultValue: int,
    ):
        self.minValue = minValue
        self.maxValue = maxValue
        self.defaultValue = defaultValue
        super.__init__(
            id, name, description, shownToCustomers, forCustomer, forParticipants, index
        )


@dataclass
class BookeoOnOffField(BookeoCustomField):
    def __init__(
        self,
        id: str,
        name: str,
        description: Optional[str],
        shown_to_customers: bool,
        for_customer: bool,
        for_participants: bool,
        index: int,
        default_state: bool,
    ):
        self.default_state = default_state
        super.__init__(
            id,
            name,
            description,
            shown_to_customers,
            for_customer,
            for_participants,
            index,
        )


@dataclass
class BookeoPeopleCategory:
    name: str
    id: str
    numSeats: int


@dataclass
class BookeoPagination:
    total_items: int
    total_pages: int
    current_page: int
    nav_token: Optional[str]

    @staticmethod
    def from_dict(info: dict):
        page_nav = info.get("pageNavigationToken")
        if page_nav is None:
            return None
        return BookeoPagination(
            info["totalItems"],
            info["totalPages"],
            info["currentPage"],
            page_nav,
        )


@dataclass
class BookeoSubaccount:
    pass


@dataclass
class BookeoPrice:
    total_gross: BookeoMoney
    total_net: BookeoMoney
    total_taxes: BookeoMoney
    total_paid: BookeoMoney
    taxes: list[BookeoPriceTax]

    @staticmethod
    def from_dict(data: dict):
        if data is None:
            return None
        taxes = [BookeoPriceTax.from_dict(t) for t in data["taxes"]]
        return BookeoPrice(
            data["totalGross"],
            data["totalNet"],
            data["totalTaxes"],
            data["totalPaid"],
            taxes,
        )


@dataclass
class BookeoResource:
    id: str

    def to_dict(self):
        return {"id": self.id}

    @staticmethod
    def from_dict(data: dict):
        return BookeoResource(data["id"])


@dataclass
class BookeoHold:
    id: str
    price: BookeoPrice
    total_payable: BookeoMoney
    expiration: datetime
    applicable_money_credit: Optional[BookeoMoney]
    applicable_giftvoucher_credit: Optional[BookeoMoney]
    applicable_prepaid_credits: Optional[int]
    promotion_applicable: Optional[bool]
    applied_promotion_discount: Optional[BookeoMoney]

    # TODO: Write BookeoHold.__str__()
    def __str__(self):
        raise NotImplementedError

    @staticmethod
    def from_dict(data: dict):
        if data is None:
            return None
        return BookeoHold(
            data["id"],
            BookeoPrice.from_dict(data["price"]),
            BookeoMoney.from_dict(data["totalPayable"]),
            bookeo_timestamp_to_dt(data["expiration"]),
            BookeoMoney.from_dict(data.get("applicableMoneyCredit")),
            BookeoMoney.from_dict(data.get("applicableGiftVoucherCredit")),
            data.get("applicablePrepaid"),
            data.get("promotionApplicable"),
            BookeoMoney.from_dict(data.get("appliedPromotionDiscount")),
        )


# TODO: Okay idk what is going on with LinkedPerson, but it seems to have multiple conflicting definitions in the Bookeo API.
@dataclass
class BookeoLinkedPerson:
    id: str
    customer_id: str
    creation_time: datetime
    first_name: Optional[str]
    middle_name: Optional[str]
    last_name: Optional[str]
    email: Optional[str]
    phone_numbers: Optional[list[BookeoPhoneNumber]]
    street_address: Optional[BookeoStreetAddress]
    next_booking_start_time: Optional[datetime]
    prev_booking_start_time: Optional[datetime]
    date_of_birth: Optional[date]
    custom_fields: Optional[list[BookeoCustomField]]
    gender: Optional[BookeoGender]

    def to_dict(self):
        return {
            "firstName": self.first_name,
            "middleName": self.middle_name,
            "lastName": self.last_name,
            "emailAddress": self.email,
            "phoneNumbers": [num.to_dict() for num in self.phone_numbers],
            "streetAddress": (self.street_address.to_dict()),
            "dateOfBirth": self.date_of_birth.strftime(r"%Y-%m-%d"),
            "customFields": [cf.to_dict() for cf in self.custom_fields],
            "gender": self.gender.value,
        }

    @staticmethod
    def from_dict(data: dict):
        return BookeoLinkedPerson(
            data["id"],
        )


@dataclass
class BookeoPeopleNumber:
    people_category_id: str
    number: int

    def to_dict(self):
        return {
            "peopleCategoryId": self.people_category_id,
            "number": self.number,
        }


@dataclass
class BookeoCustomer:
    first_name: Optional[str]
    last_name: Optional[str]
    middle_name: Optional[str]
    email: Optional[str]
    phone_numbers: Optional[list[BookeoPhoneNumber]]
    street_address: Optional[BookeoStreetAddress]
    date_of_birth: Optional[date]
    custom_fields: Optional[list[BookeoCustomField]]
    gender: Optional[BookeoGender]
    facebook_id: Optional[str]
    lang_code: Optional[str]
    accept_sms_reminders: Optional[bool]

    # TODO: Finish implementing this
    def to_dict(self):
        raise NotImplementedError
        return {
            "firstName": self.first_name,
            "middleName": self.middle_name,
            "lastName": self.last_name,
            "emailAddress": self.email,
            "phoneNumbers": [num.to_dict() for num in self.phone_numbers],
            "streetAddress": self.street_address.to_dict(),
            "dateOfBirth": self.date_of_birth.strftime(r"%Y-%m-%d"),
            "customFields": [cf.to_dict() for cf in self.custom_fields],
            "gender": self.gender.value,
            "facebookId": self.facebook_id,
            "languageCode": self.lang_code,
            "acceptSmsReminders": self.accept_sms_reminders,
        }

    @staticmethod
    def from_dict(data: dict):
        return BookeoCustomer(
            data.get("firstName"),
            data.get("lastName"),
            data.get("middleName"),
            data.get("emailAddress"),
            [BookeoPhoneNumber.from_dict(num) for num in data.get("phoneNumbers")],
            BookeoStreetAddress.from_dict(data.get("streetAddress")),
            datetime.strptime(data.get("dateOfBirth"), r"%Y-%m-%d"),
            [BookeoCustomField.from_dict(cf) for cf in data.get("customFields")],
            BookeoGender.from_str(data.get("gender")),
            data.get("facebookId"),
            data.get("languageCode"),
            data.get("acceptSmsReminders"),
        )


@dataclass
class BookeoParticipant:
    person_id: str
    people_category_id: str
    category_idx: int
    person_details: Optional[BookeoLinkedPerson]

    def to_dict(self):
        return {
            "personId": self.person_id,
            "peopleCategoryId": self.people_category_id,
            "categoryIndex": self.category_idx,
            "personDetails": self.person_details.to_dict(),
        }


@dataclass
class BookeoParticipants:
    numbers: list[BookeoPeopleNumber]
    participants: Optional[list[BookeoParticipant]]

    def to_dict(self):
        return {
            "numbers": [pn.to_dict() for pn in self.numbers],
            "details": [p.to_dict() for p in self.participants],
        }

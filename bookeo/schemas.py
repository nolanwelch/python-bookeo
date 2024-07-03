from datetime import datetime
from enum import Enum
from typing import Optional

from .core import dt_from_bookeo_str


class BookeoAPIKeyInfo:
    """Provides detailed information about the API Key being used."""

    def __init__(self, accountId: str, permissions: list[str], creationTime: str):
        self.accountId = accountId
        self.permissions = permissions
        self.creationTime = dt_from_bookeo_str(creationTime)


class BookeoPhoneType(Enum):
    Mobile = "mobile"
    Work = "work"
    Home = "home"
    Fax = "fax"

    @staticmethod
    def from_str(label: str):
        for type in BookeoPhoneType:
            if type.value == label:
                return type
        return None


class BookeoPhoneNumber:
    def __init__(self, number: str, type: BookeoPhoneType):
        self.number = number
        self.type = type

    def __repr__(self) -> str:
        return f"BookeoPhoneNumber({self.number} : {self.type})"

    @staticmethod
    def from_dict(data: dict):
        if not isinstance(data, dict):
            return None
        return BookeoPhoneNumber(
            data.get("number"), BookeoPhoneType.from_str(data.get("type"))
        )


class BookeoStreetAddress:
    def __init__(
        self,
        address_1: Optional[str],
        address_2: Optional[str],
        city: Optional[str],
        country_code: Optional[str],
        state: Optional[str],
        post_code: Optional[str],
    ):
        self.address_1 = address_1
        self.address_2 = address_2
        self.city = city
        self.country_code = country_code
        self.state = state
        self.post_code = post_code

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


class BookeoBusinessInfo:
    def __init__(
        self,
        id: str,
        name: str,
        legal_identifiers: Optional[str],
        phone_numbers: list[BookeoPhoneNumber],
        website_url: Optional[str],
        email: Optional[str],
        street_address: BookeoStreetAddress,
        logo_url: Optional[str],
        description: Optional[str],
    ):
        self.id = id
        self.name = name
        self.legal_identifiers = legal_identifiers
        self.phone_numbers = phone_numbers
        self.website_url = website_url
        self.email = email
        self.street_address = street_address
        self.logo_url = logo_url
        self.description = description

    def __repr__(self) -> str:
        return f"BookeoBusinessInfo({self.id}, {self.name})"


class BookeoBooking:
    """Represents a booking"""

    def __init__(
        self,
        title: str,
        creationTime: datetime.datetime,
        creationAgent: str,
        productId: str,
    ):
        self.title = title
        self.creationTime = creationTime
        self.creationAgent = creationAgent
        self.productId = productId


class BookingLimit:
    pass


class Duration:
    pass


class BookeoMoney:
    def __init__(self, amount: str, currency: str):
        self.amount = amount
        self.currency = currency

    @staticmethod
    def from_dict(data: dict):
        return BookeoMoney(data["amount"], data["currency"])


class BookeoPaymentMethod(Enum):
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

    @staticmethod
    def from_str(label: str):
        for method in BookeoPaymentMethod:
            if method.value == label:
                return method
        return None


class BookeoPayment:
    def __init__(
        self,
        id: str,
        creation_time: datetime,
        received_time: datetime,
        reason: str,
        description: Optional[str],
        comment: Optional[str],
        amount: BookeoMoney,
        payment_method: BookeoPaymentMethod,
        payment_method_other: Optional[str],
        agent: Optional[str],
        customer_id: Optional[str],
        gateway_name: Optional[str],
        transaction_id: Optional[str],
    ):
        self.id = id
        self.creation_time = creation_time
        self.received_time = received_time
        self.reason = reason
        self.description = description
        self.comment = comment
        self.amount = amount
        self.payment_method = payment_method
        self.payment_method_other = payment_method_other
        self.agent = agent
        self.customer_id = customer_id
        self.gateway_name = gateway_name
        self.transaction_id = transaction_id

    @staticmethod
    def from_dict(data: dict):
        return BookeoPayment(
            data["id"],
            dt_from_bookeo_str(data["creationTime"]),
            dt_from_bookeo_str(data["receivedTime"]),
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


class PriceAdjustment:
    pass


class BookeoProductType(Enum):
    Fixed = "fixed"
    FixedCourse = "fixedCourse"
    FlexibleTime = "flexibleTime"

    @staticmethod
    def from_str(label: str):
        for domain in BookeoProductType:
            if domain.value == label:
                return domain
        return None


class BookeoProduct:
    def __init__(
        self,
        name: str,
        productId: str,
        productCode: str,
        bookingLimits: list[BookingLimit],
        duration: Duration,
        type: BookeoProductType,
        membersOnly: bool,
        prepaidOnly: bool,
        acceptDeny: bool,
        apiBookingsAllowed: bool,
        dropInOnly: bool,
    ):
        pass


class Tax:
    def __init__(self, id: str, name: str, enabled: bool):
        self.id = id
        self.name = name
        self.enabled = enabled


class TelephoneNumber:
    """Describes a phone/fax number"""

    def __init__(self, number: str):
        self.number = number


class BookeoWebhook:
    pass


class BookeoWebhookDomain(Enum):
    Bookings = "bookings"
    SeatBlocks = "seatblocks"
    ResourceBlocks = "resourceblocks"
    Customers = "customers"
    Payments = "payments"

    @staticmethod
    def from_str(label: str):
        for domain in BookeoWebhookDomain:
            if domain.value == label:
                return domain
        return None


class BookeoWebhookType(Enum):
    Created = "created"
    Updated = "updated"
    Deleted = "deleted"

    @staticmethod
    def from_str(label: str):
        for domain in BookeoWebhookType:
            if domain.value == label:
                return domain
        return None


class BookeoLanguage:
    def __init__(self, tag: str, name: str, customersDefault: bool):
        self.tag = tag
        self.name = name
        self.customersDefault = customersDefault


class BookeoCustomChoiceValue:
    def __init__(self, id: str, name: str, description: str):
        self.id = id
        self.name = name
        self.description = description


class BookeoCustomField:
    def __init__(
        self,
        id: str,
        name: str,
        description: Optional[str],
        shownToCustomers: bool,
        forCustomer: bool,
        forParticipants: bool,
        index: int,
    ):
        self.id = id
        self.name = name
        self.description = description
        self.shownToCustomers = shownToCustomers
        self.forCustomer = forCustomer
        self.forParticipants = forParticipants
        self.index = index


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


class BookeoOnOffField(BookeoCustomField):
    def __init__(
        self,
        id: str,
        name: str,
        description: Optional[str],
        shownToCustomers: bool,
        forCustomer: bool,
        forParticipants: bool,
        index: int,
        defaultState: bool,
    ):
        self.defaultState = defaultState
        super.__init__(
            id, name, description, shownToCustomers, forCustomer, forParticipants, index
        )


class BookeoTextField(BookeoCustomField):
    def __init__(
        self,
        id: str,
        name: str,
        description: Optional[str],
        shownToCustomers: bool,
        forCustomer: bool,
        forParticipants: bool,
        index: int,
    ):
        super.__init__(
            id, name, description, shownToCustomers, forCustomer, forParticipants, index
        )


class BookeoPeopleCategory:
    def __init__(self, name: str, id: str, numSeats: int):
        self.name = name
        self.id = id
        self.numSeats = numSeats


class BookeoPagination:
    def __init__(
        self,
        total_items: int,
        total_pages: int,
        current_page: int,
        nav_token: Optional[str],
    ):
        self.total_items = total_items
        self.total_pages = total_pages
        self.current_page = current_page
        self.nav_token = nav_token

    @staticmethod
    def from_dict(info: dict):
        return BookeoPagination(
            info["totalItems"],
            info["totalPages"],
            info["currentPage"],
            info.get("pageNavigationToken"),
        )


class BookeoSubaccount:
    pass

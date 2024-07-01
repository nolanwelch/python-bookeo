from enum import Enum
import datetime


class ApiKeyInfo:
    """
    Provides detailed information about the API Key being used.
    """

    def __init__(
        self, accountId: str, permissions: list[str], creationTime: datetime.datetime
    ):
        self.accountId = accountId
        self.permissions = permissions
        self.creationTime = creationTime


class Booking:
    """
    Represents a booking
    """

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


class DateTime:
    def __init__(self):
        pass

    def __str__(self):
        pass


class Duration:
    pass


class Money:
    pass


class PriceAdjustment:
    pass


class ProductType(Enum):
    Fixed = "fixed"
    FixedCourse = "fixedCourse"
    FlexibleTime = "flexibleTime"


class Product:
    def __init__(
        self,
        name: str,
        productId: str,
        productCode: str,
        bookingLimits: list[BookingLimit],
        duration: Duration,
        type: ProductType,
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

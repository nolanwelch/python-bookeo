from datetime import datetime
from enum import Enum

from pydantic import BaseModel, ConfigDict, PlainSerializer, alias_generators
from typing_extensions import Annotated

from .core import dt_to_bookeo_timestamp

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

BookeoDatetime = Annotated[
    datetime, PlainSerializer(dt_to_bookeo_timestamp, return_type=str)
]


class BookeoSchema(BaseModel):
    model_config = ConfigDict(alias_generator=alias_generators.to_camel)

    class Config:
        validate_schema: True


class BookeoAPIKeyInfo(BookeoSchema):
    """Provides detailed information about the API Key being used."""

    account_id: str
    permissions: list[str]
    creation_time: BookeoDatetime


class BookeoImage(BookeoSchema):
    url: str


class BookeoPhoneNumber(BookeoSchema):
    number: str
    type: BookeoPhoneType


class BookeoStreetAddress(BookeoSchema):
    address_1: str = None
    address_2: str = None
    city: str = None
    country_code: str = None
    state: str = None
    postcode: str = None


class BookeoBusinessInfo(BookeoSchema):
    id: str
    name: str
    legal_identifiers: str = None
    phone_numbers: list[BookeoPhoneNumber]
    website_URL: str = None
    email_address: str = None
    street_address: BookeoStreetAddress
    logo: BookeoImage = None
    description: str = None


class BookeoFieldOption(BookeoSchema):
    id: str
    name: str
    description: str


class BookeoBookingOption(BookeoSchema):
    value: str
    id: str = None
    name: str = None


class BookeoCustomChoiceValue(BookeoFieldOption):
    pass


# TODO:
class BookeoCustomField(BookeoSchema):
    id: str
    name: str
    description: str = None
    shown_to_customers: bool
    for_customer: bool
    for_participants: bool
    index: int


class BookeoChoiceField(BookeoCustomField):
    values: list[BookeoCustomChoiceValue]
    default_value_id: str = None


class BookeoChoiceOptionValue(BookeoFieldOption):
    pass


class BookeoChoiceOption(BookeoFieldOption):
    index: int
    shown_to_customers: bool
    enabled: bool
    values: list[BookeoChoiceOptionValue]
    default_value_id: str = None


class BookeoNumberField(BookeoCustomField):
    min_value: int
    max_value: int
    default_value: int


class BookeoNumberOption(BookeoFieldOption):
    index: int
    shown_to_customers: bool
    enabled: bool
    min_value: int
    max_value: int
    default_value: int


class BookeoOnOffField(BookeoCustomField):
    default_state: bool


class BookeoOnOffOption(BookeoFieldOption):
    index: int
    shown_to_customers: bool
    enabled: bool
    default: bool


class BookeoTextField(BookeoCustomField):
    pass


class BookeoTextOption(BookeoCustomField):
    index: int
    shown_to_customers: bool
    enabled: bool
    required: bool


class BookeoBookingLimit(BookeoSchema):
    people_category_id: str = None
    min: int
    max: int


# TODO: Should there be a conversion from this class to timedelta?
class BookeoDuration(BookeoSchema):
    days: int
    hours: int
    minutes: int


class BookeoMoney(BookeoSchema):
    amount: str
    currency: str


class BookeoPayment(BookeoSchema):
    id: str
    creation_time: BookeoDatetime
    received_time: BookeoDatetime
    reason: str
    description: str = None
    comment: str = None
    amount: BookeoMoney
    payment_method: BookeoPaymentMethod
    payment_method_other: str = None
    agent: str = None
    customer_id: str = None
    gateway_name: str = None
    transaction_id: str = None


class BookeoPriceAdjustment(BookeoSchema):
    unit_price: BookeoMoney
    quantity: int
    description: str
    tax_ids: list[str] = None


class BookeoTax(BookeoSchema):
    id: str
    name: str
    enabled: bool


class BookeoPriceTax(BookeoSchema):
    tax_id: str
    amount: BookeoMoney


class BookeoPriceRate(BookeoSchema):
    people_category_id: str = None
    price: BookeoMoney = None


class BookeoProduct(BookeoSchema):
    name: str
    description: str = None
    images: list[BookeoImage] = None
    product_id: str
    product_code: str
    booking_limits: list[BookeoBookingLimit]
    default_rates: list[BookeoPriceRate] = None
    duration: BookeoDuration
    type: BookeoProductType
    members_only: bool
    prepaid_only: bool
    accept_deny: bool
    api_bookings_allowed: bool
    drop_in_only: bool
    allow_private_events: bool = None
    choice_options: list[BookeoChoiceOption] = None
    number_options: list[BookeoNumberOption] = None
    on_off_options: list[BookeoOnOffOption] = None
    text_options: list[BookeoTextOption] = None


class BookeoWebhook(BookeoSchema):
    id: str
    url: str
    domain: BookeoWebhookDomain
    type: BookeoWebhookType
    blocked_time: BookeoDatetime = None
    blocked_reason: str = None


class BookeoLanguage(BookeoSchema):
    tag: str
    name: str
    customers_default: bool


class BookeoPeopleCategory(BookeoSchema):
    name: str
    id: str
    num_seats: int


class BookeoPagination(BookeoSchema):
    total_items: int
    total_pages: int
    current_page: int
    page_navigation_token: str = None


class BookeoSubaccount(BookeoSchema):
    id: str
    name: str


class BookeoPrice(BookeoSchema):
    total_gross: BookeoMoney
    total_net: BookeoMoney
    total_taxes: BookeoMoney
    total_paid: BookeoMoney
    taxes: list[BookeoPriceTax]


class BookeoResource(BookeoSchema):
    name: str
    id: str


class BookeoResourceType(BookeoSchema):
    name: str = None
    id: str = None
    is_public: bool = None
    resources: list[BookeoResource] = None


class BookeoCourseEvent(BookeoSchema):
    event_number: int
    event_id: str
    start_time: BookeoDatetime
    end_time: BookeoDatetime


class BookeoCourseSchedule(BookeoSchema):
    events: list[BookeoCourseEvent]
    title: str


class BookeoMatchingSlot(BookeoSchema):
    start_time: BookeoDatetime
    end_time: BookeoDatetime
    price: BookeoMoney = None
    course_schedule: BookeoCourseSchedule = None
    event_id: str
    resources: list[BookeoResource] = None


class BookeoHold(BookeoSchema):
    id: str
    price: BookeoPrice
    total_payable: BookeoMoney
    expiration: BookeoDatetime
    applicable_money_credit: BookeoMoney = None
    applicable_gift_voucher_credit: BookeoMoney = None
    applicable_prepaid_credits: int = None
    promotion_applicable: bool = None
    applied_promotion_discount: BookeoMoney = None


# TODO: Okay idk what is going on with LinkedPerson, but it seems to have multiple conflicting definitions in the Bookeo API.
class BookeoLinkedPerson(BookeoSchema):
    id: str
    first_name: str = None
    middle_name: str = None
    last_name: str = None
    email_address: str = None
    phone_numbers: list[BookeoPhoneNumber] = None
    street_address: BookeoStreetAddress = None
    creation_time: BookeoDatetime
    start_time_of_next_booking: BookeoDatetime = None
    start_time_of_previous_booking: BookeoDatetime = None
    date_of_birth: BookeoDatetime = None
    custom_fields: list[BookeoCustomField] = None
    gender: BookeoGender = None
    customer_id: str


class BookeoPeopleNumber(BookeoSchema):
    people_category_id: str
    number: int


class BookeoCustomer(BookeoSchema):
    id: str
    first_name: str = None
    middle_name: str = None
    last_name: str = None
    email_address: str = None
    phone_numbers: list[BookeoPhoneNumber] = None
    street_address: BookeoStreetAddress = None
    start_time_of_next_booking: BookeoDatetime = None
    start_time_of_previous_booking: BookeoDatetime = None
    date_of_birth: BookeoDatetime = None
    custom_fields: list[BookeoCustomField] = None
    gender: BookeoGender = None
    facebook_id: str = None
    language_code: str = None
    accept_sms_reminders: bool = None
    num_bookings: int = None
    num_cancelations: int = None
    num_no_shows: int = None
    member: bool = None
    membership_end: BookeoDatetime = None


class BookeoParticipant(BookeoSchema):
    person_id: str
    people_category_id: str
    category_index: int
    person_details: BookeoLinkedPerson = None


class BookeoParticipants(BookeoSchema):
    numbers: list[BookeoPeopleNumber]
    details: list[BookeoParticipant] = None


class BookeoResourceBlock(BookeoSchema):
    id: str
    start_time: BookeoDatetime
    end_time: BookeoDatetime
    reason: str = None
    resources: list[BookeoResource]
    creation_time: datetime
    creation_agent: str
    last_change_time: BookeoDatetime = None
    last_change_agent: str = None


class BookeoSeatBlock(BookeoSchema):
    id: str
    event_id: str
    product_id: str
    reason: str = None
    num_seats: int
    start_time: BookeoDatetime = None
    creation_time: datetime
    creation_agent: str
    last_change_time: BookeoDatetime = None
    last_change_agent: str = None


class BookeoBooking(BookeoSchema):
    """Represents a booking"""

    booking_number: str = None
    event_id: str = None
    first_course_enrolled_event_id: str = None
    dropin_course_enrolled_event_id: str = None
    start_time: BookeoDatetime = None
    end_time: BookeoDatetime = None
    customer_id: str = None
    customer: BookeoCustomer = None
    title: str
    external_ref: str = None
    participants: BookeoParticipants
    resources: list[BookeoResource] = None
    canceled: bool = None
    cancelation_time: BookeoDatetime = None
    cancelation_agent: str = None
    accepted: bool = None
    source_ip: str = None
    creation_time: BookeoDatetime
    creation_agent: str
    last_change_time: BookeoDatetime = None
    last_change_agent: str = None
    product_name: str = None
    product_id: str
    options: list[BookeoBookingOption] = None
    private_event: bool = None
    price_adjustments: list[BookeoPriceAdjustment] = None
    promotion_code_input: str = None
    promotion_name: str = None
    coupon_codes: list[str] = None
    gift_voucher_code_input: str = None
    specific_voucher_code: str = None
    initial_payments: list[BookeoPayment] = None
    no_show: bool = None
    price: BookeoPrice = None
    source: str = None

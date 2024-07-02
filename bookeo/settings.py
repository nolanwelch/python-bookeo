from typing import Optional

from .client import BookeoClient
from .core import BookeoAPI
from .schemas import (
    BookeoAPIKeyInfo,
    BookeoBusinessInfo,
    BookeoChoiceField,
    BookeoCustomChoiceValue,
    BookeoLanguage,
    BookeoNumberField,
    BookeoOnOffField,
    BookeoPagination,
    BookeoPeopleCategory,
    BookeoPhoneNumber,
    BookeoPhoneType,
    BookeoProduct,
    BookeoProductType,
    BookeoStreetAddress,
    BookeoTextField,
)

# TODO: Add descriptions for all class methods


class BookeoSettings(BookeoAPI):
    def __init__(self, client: BookeoClient):
        super().__init__(client)

    def api_key_info(self, use_cached=True) -> BookeoAPIKeyInfo:
        if not use_cached or self._api_key_info is None:
            resp = self.client.request(self.client, "/settings/apikeyinfo")

            data = resp.json()
            self._api_key_info = BookeoAPIKeyInfo(
                data["accountId"], data["permissions"], data["creationTime"]
            )
        return self._api_key_info

    def business_info(self, use_cached=True) -> BookeoBusinessInfo:
        if not use_cached or self._business_info is None:
            resp = self.client.request("/settings/business")
            data = resp.json()
            if not isinstance(data, dict):
                return None
            phone_numbers = []
            for number in data["phoneNumbers"]:
                phone_numbers.append(
                    BookeoPhoneNumber(
                        number["number"], BookeoPhoneType.from_str(number["type"])
                    )
                )
            logo = data.get("logo")
            logo_url = logo["url"] if logo is not None else None
            self._business_info = BookeoBusinessInfo(
                data["id"],
                data["name"],
                data.get("legalIdentifiers"),
                phone_numbers,
                data.get("websiteURL"),
                data.get("emailAddress"),
                BookeoStreetAddress.from_dict(data["streetAddress"]),
                logo_url,
                data.get("description"),
            )
        return self._business_info

    def _fetch_customer_participant_info(self):
        resp = self.client.request(self.client, "/settings/customercustomfields")
        fields = resp.json()
        if not isinstance(fields, dict):
            return
        self._custom_fields = fields

    def get_choice_fields(self, use_cached=True) -> list[BookeoChoiceField]:
        if not use_cached or self._custom_fields is None:
            self._fetch_customer_participant_info()
        choice_fields = self._custom_fields.get("choiceFields")
        try:
            if not isinstance(choice_fields, list) and isinstance(
                choice_fields[0], dict
            ):
                return []
        except IndexError:
            return []

        custom_fields = []
        for field in choice_fields:
            # TODO: Handle field["values"]
            values = [
                BookeoCustomChoiceValue(v["id"], v["name"], v["description"])
                for v in field["values"]
            ]
            custom_fields.append(
                BookeoChoiceField(
                    field["id"],
                    field["name"],
                    field.get("description"),
                    field["shownToCustomers"],
                    field["forCustomer"],
                    field["forParticipants"],
                    field["index"],
                    values,
                    field.get("defaultValueId"),
                )
            )
        return custom_fields

    def get_number_fields(self, use_cached=True) -> list[BookeoNumberField]:
        if not use_cached or self._custom_fields is None:
            self._fetch_customer_participant_info()
        number_fields = self._custom_fields.get("numberFields")
        try:
            if not isinstance(number_fields, list) and isinstance(
                number_fields[0], dict
            ):
                return []
        except IndexError:
            return []

        custom_fields = []
        for field in number_fields:
            custom_fields.append(
                BookeoNumberField(
                    field["id"],
                    field["name"],
                    field.get("description"),
                    field["shownToCustomers"],
                    field["forCustomer"],
                    field["forParticipants"],
                    field["index"],
                    field["minValue"],
                    field["maxValue"],
                    field["defaultValue"],
                )
            )
        return custom_fields

    def get_onoff_fields(self, use_cached=True) -> list[BookeoOnOffField]:
        if not use_cached or self._custom_fields is None:
            self._fetch_customer_participant_info()
        onoff_fields = self._custom_fields.get("onOffFields")
        try:
            if not isinstance(onoff_fields, list) and isinstance(onoff_fields[0], dict):
                return []
        except IndexError:
            return []

        custom_fields = []
        for field in onoff_fields:
            custom_fields.append(
                BookeoOnOffField(
                    field["id"],
                    field["name"],
                    field.get("description"),
                    field["shownToCustomers"],
                    field["forCustomer"],
                    field["forParticipants"],
                    field["index"],
                    field["defaultState"],
                )
            )
        return custom_fields

    def get_text_fields(self, use_cached=True) -> list[BookeoTextField]:
        if not use_cached or self._custom_fields is None:
            self._fetch_customer_participant_info()
        text_fields = self._custom_fields.get("textFields")
        try:
            if not isinstance(text_fields, list) and isinstance(text_fields[0], dict):
                return []
        except IndexError:
            return []

        custom_fields = []
        for field in text_fields:
            custom_fields.append(
                BookeoTextField(
                    field["id"],
                    field["name"],
                    field.get("description"),
                    field["shownToCustomers"],
                    field["forCustomer"],
                    field["forParticipants"],
                    field["index"],
                )
            )
        return custom_fields

    def get_langs(self, use_cached=True) -> list[BookeoLanguage]:
        if not use_cached or self._languages is None:
            resp = self.client.request(self.client, "/settings/languages")
            data = resp.json()
            try:
                if not isinstance(data, list) and isinstance(data[0], dict):
                    return []
            except IndexError:
                return []

            self._languages = []
            for lang in data:
                self._languages.append(
                    BookeoLanguage(lang["tag"], lang["name"], lang["customersDefault"])
                )
        return self._languages

    def get_people_categories(self, use_cached=True) -> list[BookeoPeopleCategory]:
        if not use_cached or self._people_categories is None:
            resp = self.client.request(self.client, "/settings/peoplecategories")
            data = resp.json()
            try:
                if not isinstance(data, list) and isinstance(data[0], dict):
                    return []
            except IndexError:
                return []

            self._people_categories = []
            for cat in data:
                self._people_categories.append(
                    BookeoPeopleCategory(cat["name"], cat["id"], cat["numSeats"])
                )
        return self._people_categories

    # TODO: How to give users a choice between paginated responses and all? Iterable?
    def get_products(
        self,
        type: Optional[str | BookeoProductType],
        itemsPerPage: Optional[int],
        pageNavigationToken: str,
        pageNumber: Optional[int],
        lang: Optional[str],
        use_cached=True,
    ) -> tuple[BookeoPagination, list[BookeoProduct]]:
        # TODO: Complete this method
        if not use_cached or self._products is None:
            if isinstance(type, str):
                type = BookeoProductType.from_str(type)
            resp = self.client.request(self.client, "/settings/products", params={})
            if resp.status_code != 200 or False:
                pass
        return self._products

    def get_resources(self, use_cached=True):
        resp = self.client.request(self.client, "/settings/resources")

    def get_taxes(self, use_cached=True):
        resp = self.client.request(self.client, "/settings/taxes")

from .client import BookeoClient, BookeoRequestException
from .schemas import (
    BookeoAPIKeyInfo,
    BookeoBusinessInfo,
    BookeoChoiceField,
    BookeoLanguage,
    BookeoNumberField,
    BookeoOnOffField,
    BookeoPagination,
    BookeoPeopleCategory,
    BookeoProduct,
    BookeoProductType,
    BookeoResource,
    BookeoTax,
    BookeoTextField,
)


class BookeoSettings(BookeoClient):

    def api_key_info(self, use_cached=True) -> BookeoAPIKeyInfo:
        if not use_cached or self._api_key_info is None:
            resp = self._request("/settings/apikeyinfo")
            if resp.status_code != 200:
                raise BookeoRequestException(
                    "Could not get API key information.", resp.request.url
                )
            data = resp.json()
            self._api_key_info = BookeoAPIKeyInfo(**data)
        return self._api_key_info

    def business_info(self, use_cached=True) -> BookeoBusinessInfo:
        if not use_cached or self._business_info is None:
            resp = self._request("/settings/business")
            if resp.status_code != 200:
                raise BookeoRequestException(
                    "Could not get business information.", resp.request.url
                )
            data = resp.json()
            self._business_info = BookeoBusinessInfo(**data)
        return self._business_info

    def _fetch_customer_participant_info(self):
        resp = self._request("/settings/customercustomfields")
        if resp.status_code != 200:
            raise BookeoRequestException(
                "Unable to fetch custom field information.", resp.request.url
            )
        self._custom_fields = resp.json()

    def get_choice_fields(self, use_cached=True) -> list[BookeoChoiceField]:
        if not use_cached or self._choice_fields is None:
            self._fetch_customer_participant_info()
            fields = self._custom_fields.get("choiceFields")
            self._choice_fields = [BookeoChoiceField(**f) for f in fields]
        return self._choice_fields

    def get_number_fields(self, use_cached=True) -> list[BookeoNumberField]:
        if not use_cached or self._number_fields is None:
            self._fetch_customer_participant_info()
            fields = self._custom_fields.get("numberFields")
            self._number_fields = [BookeoNumberField(**f) for f in fields]
        return self._number_fields

    def get_onoff_fields(self, use_cached=True) -> list[BookeoOnOffField]:
        if not use_cached or self._onoff_fields is None:
            self._fetch_customer_participant_info()
            fields = self._custom_fields.get("onOffFields")
            self._onoff_fields = [BookeoOnOffField(**f) for f in fields]
        return self._onoff_fields

    def get_text_fields(self, use_cached=True) -> list[BookeoTextField]:
        if not use_cached or self._text_fields is None:
            self._fetch_customer_participant_info()
            fields = self._custom_fields.get("textFields")
            self._text_fields = [BookeoTextField(**f) for f in fields]
        return self._text_fields

    def get_langs(self, use_cached=True) -> list[BookeoLanguage]:
        if not use_cached or self._languages is None:
            resp = self._request("/settings/languages")
            if resp.status_code != 200:
                raise BookeoRequestException(
                    "Could not get supported languages.", resp.request.url
                )
            self._languages = [BookeoLanguage(**lang) for lang in resp.json()]
        return self._languages

    def get_people_categories(self, use_cached=True) -> list[BookeoPeopleCategory]:
        if not use_cached or self._people_categories is None:
            resp = self._request("/settings/peoplecategories")
            if resp.status_code != 200:
                raise BookeoRequestException(
                    "Could not get people categories.", resp.request.url
                )
            self._people_categories = [BookeoPeopleCategory(**c) for c in resp.json()]
        return self._people_categories

    def get_products(
        self,
        product_type: BookeoProductType = None,
        items_per_page: int = None,
        nav_token: str = None,
        page_number: int = None,
        lang: str = None,
    ) -> tuple[list[BookeoProduct], BookeoPagination]:
        resp = self._request(
            "/settings/products",
            params={
                "type": product_type.value,
                "itemsPerPage": items_per_page,
                "pageNavigationToken": nav_token,
                "pageNumber": page_number,
                "lang": lang,
            },
        )
        if resp.status_code != 200:
            raise BookeoRequestException(
                "Could not get available products.", resp.request.url
            )
        data = resp.json()
        products = [BookeoProduct(**p) for p in data["data"]]
        info = data["info"]
        pager = BookeoPagination(**info)
        return (products, pager)

    def get_resources(self) -> tuple[list[BookeoProduct], BookeoPagination]:
        resp = self._request("/settings/resources")
        if resp.status_code != 200:
            raise BookeoRequestException("Could not get resources.", resp.request.url)
        data = resp.json()
        resources = [BookeoResource(**p) for p in data["data"]]
        info = data["info"]
        pager = BookeoPagination(**info)
        return (resources, pager)

    def get_taxes(self) -> tuple[list[BookeoTax], BookeoPagination]:
        resp = self._request("/settings/taxes")
        if resp.status_code != 200:
            raise BookeoRequestException(
                "Could not get applicable taxes.", resp.request.url
            )
        data = resp.json()
        taxes = [BookeoTax(**t) for t in data["data"]]
        info = data["info"]
        pager = BookeoPagination(**info)
        return (taxes, pager)

from .request import BookeoRequest


class BookeoSettings:
    def __init__(self, client):
        self.client = client

    def api_key_info(self):
        r = BookeoRequest(self.client, "/settings/apikeyinfo")
        return r.request()

    def business_info(self):
        r = BookeoRequest(self.client, "/settings/business")
        return r.request()

    def customer_participant_info(self):
        r = BookeoRequest(self.client, "/settings/customercustomfields")
        return r.request()

    def get_langs(self):
        r = BookeoRequest(self.client, "/settings/languages")
        return r.request()

    def get_people_categories(self):
        r = BookeoRequest(self.client, "/settings/peoplecategories")
        return r.request()

    def get_products(self):
        r = BookeoRequest(self.client, "/settings/products")
        return r.request()

    def get_resources(self):
        r = BookeoRequest(self.client, "/settings/resources")
        return r.request()

    def get_taxes(self):
        r = BookeoRequest(self.client, "/settings/taxes")
        return r.request()

from .client import BookeoClient
from .core import BookeoAPI

class BookeoCustomers(BookeoAPI):
    def __init__(self, client: BookeoClient):
        super().__init__(client)
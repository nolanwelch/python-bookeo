from .core import BookeoAPI
from .client import BookeoClient

class BookeoPayments(BookeoAPI):
    def __init__(self, client: BookeoClient):
        super().__init__(client)
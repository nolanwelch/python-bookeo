from .core import BookeoAPI
from .client import BookeoClient

class BookeoHolds(BookeoAPI):
    def __init__(self, client: BookeoClient):
        super().__init__(client)
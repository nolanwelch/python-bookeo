from .core import BookeoAPI
from .client import BookeoClient

class BookeoResourceBlocks(BookeoAPI):
    def __init__(self, client: BookeoClient):
        super().__init__(client)
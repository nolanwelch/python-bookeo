from datetime import datetime
from typing import Optional

from .client import BookeoClient


class BookeoAPI:
    def __init__(self, client: BookeoClient):
        self.client = client


# TODO: Implement this method
def dt_from_bookeo_str(timestamp: str) -> Optional[datetime]:
    pass


# TODO: Implement this method
def bookeo_timestamp_from_dt(dt: datetime) -> Optional[str]:
    pass

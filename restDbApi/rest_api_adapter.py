import urllib
from dataclasses import Field
from typing import Optional, Any, Tuple, Union, Dict, List, Iterator

from shillelagh.adapters.base import Adapter
from shillelagh.fields import (
    Boolean,
    Field,
    Filter,
    Float,
    Integer,
    ISODate,
    ISODateTime,
    ISOTime,
    String,
)
from shillelagh.filters import Range, Equal
from shillelagh.typing import RequestedOrder, Row
from datetime import datetime, date, timedelta
import requests
import dateutil.parser
from shillelagh.lib import SimpleCostModel, analyze, flatten
import requests_cache
from jsonpath import JSONPath
import logging

SUPPORTED_PROTOCOLS = {"http", "https"}
AVERAGE_NUMBER_OF_ROWS = 100000
_logger = logging.getLogger(__name__)

def get_session() -> requests_cache.CachedSession:
    """
    Return a cached session.
    """
    return requests_cache.CachedSession(
        cache_name="rest_api_cache",
        backend="sqlite",
        expire_after=180,
    )

class RestAdapter(Adapter):
    safe = True
    supports_limit = True
    supports_offset = True

    """
    An adapter to use REST APIs as db-api
    """

    @staticmethod
    def supports(uri: str, fast: bool = True, **kwargs: Any) -> Optional[bool]:
        # return False
        parsed = urllib.parse.urlparse(uri)

        if parsed.scheme not in SUPPORTED_PROTOCOLS:
            return False
        if fast:
            return None

        # query_string = urllib.parse.parse_qs(parsed.query)
        session = get_session()
        response = session.head(uri)
        return "application/json" in response.headers["content-type"]

    @staticmethod
    def parse_uri(uri: str) -> Tuple[str, str]:
        parsed = urllib.parse.urlparse(uri)

        path = urllib.parse.unquote(parsed.fragment) or "$[*]"
        uri = urllib.parse.urlunparse(parsed._replace(fragment=""))

        return uri, path
    
    def __init__(self, uri: str, path: str = "$[*]"):
        super().__init__()

        self.uri = uri
        self.path = path

        self._session = get_session()

        self._set_columns()

    def _set_columns(self) -> None:
        print("yessss boiiii")
        rows = list(self.get_data({}, []))
        column_names = list(rows[0].keys()) if rows else []

        _, order, types = analyze(iter(rows))

        self.columns = {
            column_name: types[column_name](
                filters=[Equal],
                order=order[column_name],
                exact=False,
            )
            for column_name in column_names
        }

    def get_columns(self) -> Dict[str, Field]:
        return self.columns

    get_cost = SimpleCostModel(AVERAGE_NUMBER_OF_ROWS)

    def get_data(  # pylint: disable=unused-argument
            self,
            bounds: Dict[str, Filter],
            order: List[Tuple[str, RequestedOrder]],
            limit: Optional[int] = None,
            offset: Optional[int] = None,
            **kwargs: Any,
    ) -> Iterator[Row]:
        response = self._session.get(self.uri)
        payload = response.json()
        parser = JSONPath(self.path)
        data = parser.parse(payload)
        for i, row in enumerate(data):
            row["rowid"] = i
            _logger.debug(row)
            yield flatten(row)
        

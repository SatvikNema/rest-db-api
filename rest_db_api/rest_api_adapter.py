import urllib
from typing import Optional, Any, Tuple, Dict, List, Iterator

from shillelagh.adapters.base import Adapter
from shillelagh.fields import (
    Boolean,
    Field,
    Filter,
)
from shillelagh.filters import Equal
from shillelagh.typing import RequestedOrder, Row
from shillelagh.lib import SimpleCostModel, analyze, flatten
import requests_cache
from jsonpath import JSONPath
import logging
import json

SUPPORTED_PROTOCOLS = {"http", "https"}
AVERAGE_NUMBER_OF_ROWS = 100000
_logger = logging.getLogger(__name__)
CHARSET = 'utf8'


def get_session() -> requests_cache.CachedSession:
    """
    Return a cached session.
    """
    return requests_cache.CachedSession(
        cache_name="rest_api_cache",
        backend="sqlite",
        expire_after=180,
    )


def get_decoded_json_body(encoded_json_body: str) -> Dict[Any, Any]:
    decoded = urllib.parse.unquote(encoded_json_body, CHARSET)
    return json.loads(decoded)


def get_encoded_json_body(plain_json_body: str) -> str:
    return urllib.parse.quote(plain_json_body, CHARSET)


def decompose_virtual_table(uri: str) -> Tuple[str, Dict[str, List[str]], Dict[str, str], str, Dict[str, Any]]:
    parsed = urllib.parse.urlparse(uri)

    path = parsed.path
    params_and_headers: Dict[str, List[str]] = urllib.parse.parse_qs(parsed.query)
    fragment = urllib.parse.unquote(parsed.fragment) or "$[*]"

    headers: List[HttpHeader] = []
    query_params: Dict = {}
    body: Dict = {}
    for key, val in params_and_headers.items():
        if key.startswith("header"):
            header: HttpHeader = HttpHeader.parse_header_params(val[0])
            headers.append(header)
        elif key == "body":
            body = get_decoded_json_body(val[0])
        else:
            query_params[key] = ",".join(val)

    headers_dict = HttpHeader.load_headers(headers)
    return path, query_params, headers_dict, fragment, body


class HttpHeader:
    def __init__(self, key, value):
        self.key = key
        self.value = value

    def get_value(self) -> str:
        return self.value

    def get_key(self) -> str:
        return self.key

    @staticmethod
    def load_headers(headers: List['HttpHeader']) -> Dict[str, str]:
        header_dict = {}
        for header in headers:
            header_dict[header.get_key()] = header.get_value()
        return header_dict

    @staticmethod
    def parse_header_params(header_param: str) -> 'HttpHeader':
        first_colon_index = header_param.index(":", 0)
        key = header_param[:first_colon_index]
        value = header_param[first_colon_index + 1:]
        return HttpHeader(key, value)


class RestAdapter(Adapter):
    safe = True
    supports_limit = True
    supports_offset = True

    """
    An adapter to use REST APIs as db-api
    """

    @staticmethod
    def supports(uri: str, fast: bool = True, **kwargs: Any) -> Optional[bool]:
        return True  # as this is only called from rest_api_dialect

    @staticmethod
    def parse_uri(uri: str) -> Tuple[str, Dict[str, List[str]], Dict[str, str], str, Dict[str, Any]]:
        parsed = urllib.parse.urlparse(uri)

        path = parsed.path
        params_and_headers: Dict[str, List[str]] = urllib.parse.parse_qs(parsed.query)
        fragment = urllib.parse.unquote(parsed.fragment) or "$[*]"

        headers: List[HttpHeader] = []
        query_params: Dict = {}
        body: Dict = {}
        for key, val in params_and_headers.items():
            if key.startswith("header"):
                header: HttpHeader = HttpHeader.parse_header_params(val[0])
                headers.append(header)
            if key == "body":
                body = get_decoded_json_body(val[0])

            else:
                query_params[key] = val

        headers_dict = HttpHeader.load_headers(headers)
        return path, query_params, headers_dict, fragment, body

    def __init__(self,
                 path: str,
                 query_params: Dict[str, List[str]],
                 headers_dict: Dict[str, str],
                 fragment: str,
                 body: Dict[Any, Any],
                 base_url: str = None,
                 is_https: Boolean = True, **kwargs: Any):
        super().__init__()
        self.query_params = query_params
        self.fragment = fragment
        self.is_https = is_https
        self.headers = headers_dict
        self.body = body
        self._session = get_session()
        if self.is_https is None or self.is_https:
            prefix = "https://"
        else:
            prefix = "http://"

        self.url = prefix + base_url + path
        self._set_columns()

    def _set_columns(self) -> None:
        print("custom rest adapter is being used :)")
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

    def get_data(
            self,
            bounds: Dict[str, Filter],
            order: List[Tuple[str, RequestedOrder]],
            limit: Optional[int] = None,
            offset: Optional[int] = None,
            **kwargs: Any,
    ) -> Iterator[Row]:
        if self.body:
            response = self._session.post(self.url, params=self.query_params, headers=self.headers, json=self.body)
        else:
            response = self._session.get(self.url, params=self.query_params, headers=self.headers)
        payload = response.json()
        parser = JSONPath(self.fragment)
        data = parser.parse(payload)
        for i, row in enumerate(data):
            row["rowid"] = i
            _logger.debug(row)
            yield flatten(row)

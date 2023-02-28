import urllib.parse

from shillelagh.backends.apsw.dialects.base import APSWDialect
from sqlalchemy.engine.url import URL
from typing import Any, Dict, Tuple, List

from sqlalchemy.pool import _ConnectionFairy


class RestApiDialect(APSWDialect):
    name = "rest"
    supports_statement_cache = True

    def create_connect_args(self, url: URL) -> Tuple[Tuple[()], Dict[str, Any]]:
        str_url = url.__to_string__()
        parsed = urllib.parse.urlparse(str_url)
        base_url = parsed.netloc
        query_params = urllib.parse.parse_qs(parsed.query)
        is_https = False
        if "ishttps" in query_params:
            is_https = query_params["ishttps"][0] == '1'

        return (), {
            "path": ":memory:",
            "adapters": ["myrestadapter"],
            "adapter_kwargs": {
                "myrestadapter": {
                    "base_url": base_url,
                    "is_https": is_https,
                },
            },
            "safe": True,
            "isolation_level": self.isolation_level,
        }

    def get_table_names(self, connection, schema=None, **kw) -> List[str]:
        return ["'Tables' dont exists in rest APIs. Use SQL lab directly"]

    def do_ping(self, dbapi_connection: _ConnectionFairy) -> bool:
        # required to check 'active' connections by superset. As this is a REST call, this is not applicable.
        return True

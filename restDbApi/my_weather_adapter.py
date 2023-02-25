import urllib
from dataclasses import Field
from typing import Optional, Any, Tuple, Union, Dict, List, Iterator

from shillelagh.adapters.base import Adapter
from shillelagh.fields import (
    Field,
    Filter,
    Float,
    Integer,
)
from shillelagh.filters import Equal
from shillelagh.typing import RequestedOrder, Row
import requests

class MyWeatherAdapter(Adapter):

    safe = True
    supports_limit = True
    supports_offset = True

    """
    An adapter to forecast data from https://www.weatherapi.com/.
    """

    @staticmethod
    def supports(uri: str, fast: bool = True, **kwargs: Any) -> Optional[bool]:
        parsed = urllib.parse.urlparse(uri)
        query_string = urllib.parse.parse_qs(parsed.query)
        return (
                parsed.netloc == "api.weatherapi.com"
                and parsed.path == "/v1/forecast.json"
                and "q" in query_string
                and ("key" in query_string or "api_key" in kwargs)
        )

    @staticmethod
    def parse_uri(uri: str) -> Union[Tuple[str], Tuple[str, str]]:
        parsed = urllib.parse.urlparse(uri)
        query_string = urllib.parse.parse_qs(parsed.query)
        location = query_string["q"][0]

        # key can be passed in the URI or via connection arguments
        if "key" in query_string:
            return (location, query_string["key"][0])
        return (location,)

    def __init__(self, location: str, api_key: str):
        super().__init__()
        self.location = location
        self.api_key = api_key

    def get_columns(self) -> Dict[str, Field]:
        return {
            "maxtemp_c": Float(),
            "maxwind_kph": Float(),
            "days": Integer(filters=[Equal])
        }

    def get_rows(
            self,
            bounds: Dict[str, Filter],
            order: List[Tuple[str, RequestedOrder]],
            **kwargs: Any,
    ) -> Iterator[Row]:
        # get the time predicate
        days_param = bounds.get("days", Equal(1))
        aqi_param = bounds.get("aqi",  Equal("no"))
        alerts_param = bounds.get("alerts",  Equal("no"))

        url = "http://api.weatherapi.com/v1/forecast.json"
        params = {"key": self.api_key, "q": self.location, "days": days_param.value, "aqi": aqi_param.value, "alerts": alerts_param.value}
        response = requests.get(url, params=params, )
        payload = response.json()
        flat_data = []
        for record in payload["forecast"]["forecastday"]:
            data = record["day"]
            data['date'] = record['date']
            i = 0
            for hour in record["hour"]:
                data["hour_" + str(i) + "_gust_kph"] = hour["gust_kph"]
                i += 1
            data["astro"] = record["astro"]
            flat_data.append(data)

        for i, record in enumerate(flat_data):
            yield {
                "rowid": i,
                "maxtemp_c": record["maxtemp_c"],
                "maxwind_kph": record["maxwind_kph"],
                "days": days_param.value
            }



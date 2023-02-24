from typing import Dict, Any, List

import requests


def get_flat_weather_data(params: Dict[str, Any], url: str) -> List[Dict[str, Any]]:
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
    return flat_data

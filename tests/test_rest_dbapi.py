from pytest_mock import MockerFixture
from requests import Session
from requests_mock.mocker import Mocker
import urllib
from sqlalchemy import inspect

from rest_db_api.rest_api_adapter import decompose_virtual_table
from rest_db_api.utils import get_virtual_table

SIMPLE_URL = 'https://api.covidtracking.com/v1/us/daily.json'
POST_URL = 'http://some.api.com/some/api/path?a=60&b=-50&c=someQuery'

MOCK_PARAMS = {
    'key': 'this is my key',
    'q': 'Bangalore',
    'days': 5
}
MOCK_BODY = {
    "this": [
        {
            "id": "1",
            "name": "test body",
            "key": 123
        },
        {
            "id": "2",
            "name": "test body 2",
            "key": 567
        }
    ],
    "id": -10
}

MOCK_HEADERS = {
    "content-type": "application/json"
}

MOCK_HEADERS2 = {
    "content-type": "application/json",
    "ENV": "dev"
}

MOCK_RESPONSE = [
    {
        "date": 20210307,
        "states": 56,
        "positive": 28756489,
        "negative": 74582825,
        "pending": 11808,
        "hospitalizedCurrently": 40199,
        "hospitalizedCumulative": 776361,
        "inIcuCurrently": 8134,
        "inIcuCumulative": 45475,
        "onVentilatorCurrently": 2802,
        "onVentilatorCumulative": 4281,
        "dateChecked": "2021-03-07T24:00:00Z",
        "death": 515151,
        "hospitalized": 776361,
        "totalTestResults": 363825123,
        "lastModified": "2021-03-07T24:00:00Z",
        "recovered": None,
        "total": 0,
        "posNeg": 0,
        "deathIncrease": 842,
        "hospitalizedIncrease": 726,
        "negativeIncrease": 131835,
        "positiveIncrease": 41835,
        "totalTestResultsIncrease": 1170059,
        "hash": "a80d0063822e251249fd9a44730c49cb23defd83"
    },
    {
        "date": 20210306,
        "states": 56,
        "positive": 28714654,
        "negative": 74450990,
        "pending": 11783,
        "hospitalizedCurrently": 41401,
        "hospitalizedCumulative": 775635,
        "inIcuCurrently": 8409,
        "inIcuCumulative": 45453,
        "onVentilatorCurrently": 2811,
        "onVentilatorCumulative": 4280,
        "dateChecked": "2021-03-06T24:00:00Z",
        "death": 514309,
        "hospitalized": 775635,
        "totalTestResults": 362655064,
        "lastModified": "2021-03-06T24:00:00Z",
        "recovered": None,
        "total": 0,
        "posNeg": 0,
        "deathIncrease": 1680,
        "hospitalizedIncrease": 503,
        "negativeIncrease": 143835,
        "positiveIncrease": 60015,
        "totalTestResultsIncrease": 1430992,
        "hash": "dae5e558c24adb86686bbd58c08cce5f610b8bb0"
    }]


def test_rest_adapter(mocker: MockerFixture, requests_mock: Mocker, covid_data_connection):
    mocker.patch(
        "rest_db_api.rest_api_adapter.requests_cache.CachedSession",
        return_value=Session(),
    )

    requests_mock.get(SIMPLE_URL, json=MOCK_RESPONSE)

    sql = "select * from '/v1/us/daily.json'"
    data = covid_data_connection.execute(sql)
    assert len(list(data)) == 2


def test_rest_adapter_post(mocker: MockerFixture, requests_mock: Mocker, post_data_connection):
    mocker.patch(
        "rest_db_api.rest_api_adapter.requests_cache.CachedSession",
        return_value=Session(),
    )

    endpoint = '/some/api/path?a=60&b=-50&c=someQuery'
    headers = '&header1=Content-Type:application/json'
    headers += '&header2=IAM_ID:satvik'
    headers += '&header3=ENVIRONMENT:staging:1.5.3'
    headers += '&header4=NAME:MY-REST-SERVICE'
    body = '{ "name": "satvik", "interests": [ { "name": "badminton", "category": "sports", "stats": { "racket": "intermediate", "shuttle": "yonex mavis 500" } }, { "name": "programming", "category": "computers", "stats": { "laptop": "mac book pro", "mouse": "5D ergonomic", "keyboard": "broken" } } ] }'
    jsonpath = "#$[*]"

    encoded_body = "&body=" + urllib.parse.quote(body, 'utf8')
    url = endpoint + headers + encoded_body + jsonpath
    sql = f"select * from '{url}'"

    requests_mock.post(POST_URL, json=MOCK_RESPONSE)
    data = post_data_connection.execute(sql)
    assert len(list(data)) == 2


def test_dialect_get_table_name(covid_data_connection):
    metadata = inspect(covid_data_connection)
    tables = metadata.get_table_names()
    assert len(tables) == 1
    assert tables[0] == "'Tables' dont exists in rest APIs. Use SQL lab directly"


def test_get_virtual_table():
    endpoint = '/v1/forecast.json'
    default = get_virtual_table(endpoint=endpoint)
    assert default == '/v1/forecast.json#$[*]'

    with_params = get_virtual_table(endpoint=endpoint, params=MOCK_PARAMS)
    assert with_params == '/v1/forecast.json?key=this+is+my+key&q=Bangalore&days=5#$[*]'

    with_headers = get_virtual_table(endpoint=endpoint, params=MOCK_PARAMS, headers=MOCK_HEADERS)
    assert with_headers == '/v1/forecast.json?key=this+is+my+key&q=Bangalore&days=5&header1=content-type:application/json#$[*]'

    only_headers = get_virtual_table(endpoint=endpoint, headers=MOCK_HEADERS)
    assert only_headers == '/v1/forecast.json?header1=content-type:application/json#$[*]'

    with_body = get_virtual_table(endpoint=endpoint, params=MOCK_PARAMS, headers=MOCK_HEADERS2, body=MOCK_BODY)
    assert with_body == '/v1/forecast.json?key=this+is+my+key&q=Bangalore&days=5&header1=content-type:application/json&header2=ENV:dev&body=%7B%22this%22%3A%20%5B%7B%22id%22%3A%20%221%22%2C%20%22name%22%3A%20%22test%20body%22%2C%20%22key%22%3A%20123%7D%2C%20%7B%22id%22%3A%20%222%22%2C%20%22name%22%3A%20%22test%20body%202%22%2C%20%22key%22%3A%20567%7D%5D%2C%20%22id%22%3A%20-10%7D#$[*]'

    only_body = get_virtual_table(endpoint=endpoint, body=MOCK_BODY)
    assert only_body == '/v1/forecast.json?body=%7B%22this%22%3A%20%5B%7B%22id%22%3A%20%221%22%2C%20%22name%22%3A%20%22test%20body%22%2C%20%22key%22%3A%20123%7D%2C%20%7B%22id%22%3A%20%222%22%2C%20%22name%22%3A%20%22test%20body%202%22%2C%20%22key%22%3A%20567%7D%5D%2C%20%22id%22%3A%20-10%7D#$[*]'


def test_decompose_virtual_table():
    virtual_table = "/api/v1/test?param1=p1value1%2Cp2value2%2Cp3value3&n1=34.51&n2=-98.35&n3=30.66&n4=-117.87&header1=Content-Type:application/json&header2=h1:some_header_1&header3=h2:someHeader2&header4=h3:some_header_3&body=%7B%22name%22%3A%20%22Satvik%22%2C%20%22interests%22%3A%20%5B%22runningreading%22%2C%20%22tech%22%5D%2C%20%22location%22%3A%20%7B%22init%22%3A%20%7B%22name%22%3A%20%22mumbai%22%2C%20%22time%22%3A%2020%7D%2C%20%22adult%22%3A%20%7B%22name%22%3A%20%22blr%22%2C%20%22time%22%3A%201%7D%7D%7D#$[*]"
    path, query_params, headers_dict, fragment, body = decompose_virtual_table(virtual_table)

    expected_body = {
        "name": "Satvik",
        "interests": [
            "running"
            "reading",
            "tech"
        ],
        "location": {
            "init": {
                "name": "mumbai",
                "time": 20
            },
            "adult": {
                "name": "blr",
                "time": 1
            }
        }
    }

    expected_headers = {'Content-Type': 'application/json',
                        'h1': 'some_header_1',
                        'h2': 'someHeader2',
                        'h3': 'some_header_3'}

    expected_params = {'param1': 'p1value1,p2value2,p3value3',
                       'n1': '34.51',
                       'n2': '-98.35',
                       'n3': '30.66',
                       'n4': '-117.87'}

    assert query_params == expected_params
    assert headers_dict == expected_headers
    assert fragment == "$[*]"
    assert body == expected_body
    assert path == "/api/v1/test"

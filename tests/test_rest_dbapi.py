from pytest_mock import MockerFixture
from requests import Session
from requests_mock.mocker import Mocker
import urllib
import restDbApi.rest_api_dialect
from sqlalchemy import inspect

SIMPLE_URL = 'https://api.covidtracking.com/v1/us/daily.json'
POST_URL = 'http://some.api.com/some/api/path?a=60=-50&c=someQuery'

def test_rest_adapter(mocker: MockerFixture, requests_mock: Mocker, covid_data_connection):
    mocker.patch(
        "restDbApi.rest_api_adapter.requests_cache.CachedSession",
        return_value=Session(),
    )

    requests_mock.get(SIMPLE_URL, json= [
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
  }])

    sql = "select * from '/v1/us/daily.json'"
    data = covid_data_connection.execute(sql)
    assert len(list(data)) == 2

def test_rest_adapter_post(mocker: MockerFixture, requests_mock: Mocker, post_data_connection):
    mocker.patch(
        "restDbApi.rest_api_adapter.requests_cache.CachedSession",
        return_value=Session(),
    )

    endpoint = '/some/api/path?a=60=-50&c=someQuery'
    headers = '&header1=Content-Type:application/json'
    headers += '&header2=IAM_ID:satvik'
    headers += '&header3=ENVIRONMENT:staging:1.5.3'
    headers += '&header4=NAME:MY-REST-SERVICE'
    body = '{ "name": "satvik", "interests": [ { "name": "badminton", "category": "sports", "stats": { "racket": "intermediate", "shuttle": "yonex mavis 500" } }, { "name": "programming", "category": "computers", "stats": { "laptop": "mac book pro", "mouse": "5D ergonomic", "keyboard": "broken" } } ] }'
    jsonpath = "#$[*]"


    encoded_body = "&body=" + urllib.parse.quote(body, 'utf8')
    url = endpoint + headers + encoded_body + jsonpath
    sql = f"select * from '{url}'"

    requests_mock.post(POST_URL, json= [
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
  }])
    data = post_data_connection.execute(sql)
    assert len(list(data)) == 2

def test_dialect_get_table_name(covid_data_connection):
    metadata = inspect(covid_data_connection)
    tables = metadata.get_table_names()
    assert len(tables) == 1
    assert tables[0] == "'Tables' dont exists in rest APIs. Use SQL lab directly"
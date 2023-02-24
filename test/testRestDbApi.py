from shillelagh.backends.apsw.db import connect


def get_custom():
    api_key = 'f1f6d01fe66c4cd48de113426232402'
    connection = connect(":memory:", adapter_kwargs={"myweatherapi": {"api_key": api_key}})
    cursor = connection.cursor()

    query = 'SELECT maxtemp_c FROM "http://api.weatherapi.com/v1/forecast.json?q=London" where days=10'

    show_results(query, cursor)

def get_generic_json():
    connection = connect(":memory:")
    cursor = connection.cursor()
    # query = 'SELECT * FROM "http://api.weatherapi.com/v1/forecast.json?q=London&key=f1f6d01fe66c4cd48de113426232402&days=5#$.forecast.forecastday[*]" where date_epoch in (1677283200,1677456000)'
    query = 'SELECT json_extract(astro, "$.moonrise") FROM "http://api.weatherapi.com/v1/forecast.json?q=London&key=f1f6d01fe66c4cd48de113426232402&days=5#$.forecast.forecastday[*]" where date_epoch in (1677283200,1677456000)'
    show_results(query, cursor)

def show_results(query, cursor):
    res = cursor.execute(query)
    print("final result: ")
    for row in res:
        print(row)

user_my_adapter = 0
if user_my_adapter:
    get_custom()
else:
    get_generic_json()
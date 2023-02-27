from sqlalchemy import create_engine
from restDbApi.utils import get_virtual_table

# engine = create_engine("rest://api.weatherapi.com?ishttps=1")
#
# endpoint = '/v1/forecast.json'
# params = {
#     'key': 'f1f6d01fe66c4cd48de113426232402',
#     'q': 'Bangalore',
#     'days': 5
# }
# jsonpath = "$.forecast.forecastday[*]"
# virtual_table = get_virtual_table(endpoint=endpoint,
#                                   params=params,
#                                   jsonpath=jsonpath)
# connection = engine.connect()
# query = f"""
# SELECT
#   date,
#   json_extract(day, "$.maxtemp_c") as max_temp_celsius,
#   json_extract(hour, "$[6].temp_c") as six_am_celsius,
#   json_extract(hour, "$[6].will_it_rain") as will_it_rain
# FROM
#   "{virtual_table}"
# """
# for i in connection.execute(query):
#     print(i)


# engine = create_engine("rest://stg.wsp-store-info.walmart.com?ishttps=0")
# connection = engine.connect()
#
# endpoint = '/wsp-store-info/v1/layers/pipelinestores'
#
# params = {
#     'hlong': '-98.04269584580887',
#     'llat': '30.660521215372583',
#     'hlat': '34.51010643175928',
#     'llong': '-117.87603469278673',
#     'pipelinestores': 'APPROVED_LX,IDEA_LX,PROJECTS_LX'
# }
#
# headers = {
#     'Content-Type': 'application/json',
#     'WM_CONSUMER.ID': '7aa13f7b-5e29-451b-bcfa-ba1b62471b89',
#     'WM_SVC.ENV': 'stg',
#     'WM_SVC.NAME': 'WSP-STORE-INFO',
#     'sessionId': 'czBuMDJxbQ==',
# }
#
# jsonpath = "$[*]"
#
# virtual_table = get_virtual_table(endpoint=endpoint,
#                                   params=params,
#                                   headers=headers,
#                                   jsonpath=jsonpath)
# print(virtual_table)
# for i in connection.execute(f'SELECT * FROM "{virtual_table}"'):
#     print(i)



engine = create_engine("rest://stg.wsp-store-info.walmart.com?ishttps=0")
connection = engine.connect()
endpoint = '/wsp-store-info/v1/layers/remodel'

params = {
    "hlong": '-98.04269584580887',
    'llat': '33.006947387589554',
    'hlat': '34.22131924306147',
    'llong': '-112.11325248643387'
}

headers = {
    'Content-Type': 'application/json',
    'WM_CONSUMER.ID': '7aa13f7b-5e29-451b-bcfa-ba1b62471b89',
    'WM_SVC.ENV': 'stg',
    'WM_SVC.NAME': 'WSP-STORE-INFO',
    'sessionId': 'czBuMDJxbQ==',
}

body = {
    "remodelInitiative": ["EOTF", "RSDWH", "D8 PET COOLER"],
    "remodelProjectStatus": [
        "RECENTLY_COMPLETED"
    ]
}

jsonpath = "$.remodelData[*]"

virtual_table = get_virtual_table(endpoint=endpoint,
                                  params=params,
                                  headers=headers,
                                  body=body,
                                  jsonpath=jsonpath)

print(virtual_table)
for i in connection.execute(f'SELECT * FROM "{virtual_table}"'):
    print(i)
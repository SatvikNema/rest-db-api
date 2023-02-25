import urllib.parse

from sqlalchemy import create_engine

engine = create_engine("rest://api.weatherapi.com?ishttps=1")
connection = engine.connect()
for i in connection.execute('SELECT * FROM "/v1/forecast.json?key=f1f6d01fe66c4cd48de113426232402&q=London&days=5#$.forecast.forecastday[*]"'):
    print(i)


engine = create_engine("rest://stg.wsp-store-info.walmart.com?ishttps=0")
connection = engine.connect()

endpoint = '/wsp-store-info/v1/layers/pipelinestores?pipelinestores=APPROVED_LX,IDEA_LX,PROJECTS_LX&hlat=34.51010643175928&hlong=-98.35332961466173&llat=30.660521215372583&llong=-117.87603469278673';
headers = '&header1=Content-Type:application/json'
headers += '&header2=WM_CONSUMER.ID:7aa13f7b-5e29-451b-bcfa-ba1b62471b89'
headers += '&header3=WM_SVC.ENV:stg'
headers += '&header4=WM_SVC.NAME:WSP-STORE-INFO'
headers += '&header5=sessionId:czBuMDJxbQ=='
jsonpath = "#$[*]"

virtual_table = endpoint+headers+jsonpath
print(virtual_table)
for i in connection.execute(f'SELECT * FROM "{virtual_table}"'):
    print(i)

engine = create_engine("rest://stg.wsp-store-info.walmart.com?ishttps=0")
connection = engine.connect()

endpoint = '/wsp-store-info/v1/layers/remodel?hlat=60.22131924306147&hlong=-50.04269584580887&llat=1.006947387589554&llong=-160.11325248643387&openstores=SUP';
headers = '&header1=Content-Type:application/json'
headers += '&header2=WM_CONSUMER.ID:7aa13f7b-5e29-451b-bcfa-ba1b62471b89'
headers += '&header3=WM_SVC.ENV:stg'
headers += '&header4=WM_SVC.NAME:WSP-STORE-INFO'
headers += '&header5=sessionId:czBuMDJxbQ=='
body = '{ "remodelInitiative": ["EOTF", "RSDWH", "D8 PET COOLER"], "remodelProjectStatus": ["RECENTLY_COMPLETED"] }'
jsonpath = "#$.remodelData[*]"

encoded_body = "&body="+urllib.parse.quote(body, 'utf8')
virtual_table = endpoint+headers+encoded_body+jsonpath
print(virtual_table)
for i in connection.execute(f'SELECT * FROM "{virtual_table}"'):
    print(i)
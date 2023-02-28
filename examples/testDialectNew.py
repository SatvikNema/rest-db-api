from sqlalchemy import create_engine

engine = create_engine("rest://api.weatherapi.com?ishttps=1")
connection = engine.connect()
key = 'f1f6d01fe66c4cd48de113426232402'
query = f'SELECT * FROM "/v1/forecast.json?key={key}&q=Bangalore&days=3#$.forecast.forecastday[*]"'
for i in connection.execute(query):
    print(i)
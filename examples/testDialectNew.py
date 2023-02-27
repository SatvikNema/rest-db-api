from sqlalchemy import create_engine

engine = create_engine("rest://api.weatherapi.com?ishttps=1")
connection = engine.connect()
key = 'your_key'
query = f'SELECT * FROM "/v1/forecast.json?key={key}&q=Bangalore&days=3#$.forecast.forecastday[*]"'
for i in connection.execute(query):
    print(i)
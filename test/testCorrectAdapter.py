from datetime import datetime, timedelta
from shillelagh.backends.apsw.db import connect

three_days_ago = datetime.now() - timedelta(days=3)

# sign up for an API key at https://www.weatherapi.com/my/
api_key = "349be02b64f54bbd9bb70758232302"

connection = connect(":memory:", adapter_kwargs={"weatherapi": {"api_key": api_key}})
cursor = connection.cursor()

sql = """
SELECT *
FROM "https://api.weatherapi.com/v1/history.json?q=London"
WHERE time >= ?
"""
for row in cursor.execute(sql, (three_days_ago,)):
    print(row)
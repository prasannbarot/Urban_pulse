# check_weather.py
import sqlite3
import pandas as pd

DB_PATH = "urbanpulse.db"

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='weather';")
if not cursor.fetchone():
    print("Weather table does not exist!")
else:
    df = pd.read_sql_query("SELECT * FROM weather", conn)
    if df.empty:
        print("Weather table is empty!")
    else:
        print("Weather data:")
        print(df)
        for city in ["Toronto", "Vancouver", "Montreal"]:
            city_data = df[df["city"] == city]
            print(f"\n{city} data:")
            print(city_data)

conn.close()
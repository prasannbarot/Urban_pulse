# load/db_loader.py

import sqlite3
import json

def create_connection(db_file="urbanpulse.db"):
    """
    Create a SQLite database connection.
    """
    conn = sqlite3.connect(db_file)
    return conn

def create_tables(conn):
    """
    Create tables for weather, sensor, and social data.
    """
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS weather (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            city TEXT,
            temperature REAL,
            humidity REAL,
            description TEXT,
            data TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sensor (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            air_quality_index INTEGER,
            noise_level REAL,
            timestamp DATETIME
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS social (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            text TEXT,
            label TEXT,
            score REAL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()

def load_weather_data(conn, weather_data, city="Toronto"):
    """
    Insert weather data into the weather table.
    """
    cursor = conn.cursor()
    temperature = weather_data['main']['temp']
    humidity = weather_data['main']['humidity']
    description = weather_data['weather'][0]['description']
    data_str = json.dumps(weather_data)  # Save raw JSON
    cursor.execute("""
        INSERT INTO weather (city, temperature, humidity, description, data)
        VALUES (?, ?, ?, ?, ?)
    """, (city, temperature, humidity, description, data_str))
    conn.commit()

def load_sensor_data(conn, sensor_data):
    """
    Insert sensor data into the sensor table.
    """
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO sensor (air_quality_index, noise_level, timestamp)
        VALUES (?, ?, ?)
    """, (sensor_data["air_quality_index"], sensor_data["noise_level"], sensor_data["timestamp"]))
    conn.commit()

def load_social_data(conn, text, sentiment):
    """
    Insert a social media record into the social table.
    `sentiment` is a dict with keys 'label' and 'score'.
    """
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO social (text, label, score)
        VALUES (?, ?, ?)
    """, (text, sentiment["label"], sentiment["score"]))
    conn.commit()

if __name__ == "__main__":
    conn = create_connection()
    create_tables(conn)
    print("Database and tables are ready!")

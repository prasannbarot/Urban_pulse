# transform/data_transform.py

import sqlite3
import pandas as pd

def fetch_data(conn):
    """
    Fetch data from the raw tables.
    Returns dataframes: weather_df, sensor_df, and social_df.
    """
    weather_df = pd.read_sql_query("SELECT * FROM weather", conn)
    sensor_df = pd.read_sql_query("SELECT * FROM sensor", conn)
    social_df = pd.read_sql_query("SELECT * FROM social", conn)
    return weather_df, sensor_df, social_df

def transform_data(weather_df, sensor_df, social_df):
    """
    Merge data from various sources and compute an urban stress index.
    For demonstration, we simulate a computation using sensor values and sentiment scores.
    Returns a combined DataFrame.
    """
    # For simplicity, assume we have similar lengths and align by index.
    sensor_df['air_quality_factor'] = sensor_df['air_quality_index'] / 100.0
    social_df['sentiment_factor'] = social_df['score']
    
    # Create a combined DataFrame (simulation)
    df_combined = pd.DataFrame({
        "temperature": weather_df["temperature"][:len(sensor_df)].values,
        "humidity": weather_df["humidity"][:len(sensor_df)].values,
        "air_quality_index": sensor_df["air_quality_index"],
        "noise_level": sensor_df["noise_level"],
        "sentiment_factor": social_df["sentiment_factor"][:len(sensor_df)].values
    })
    
    # A simulated urban stress index (weighted combination)
    df_combined["urban_stress_index"] = (
        0.4 * df_combined["air_quality_index"] +
        0.3 * df_combined["noise_level"] +
        0.3 * (1 - df_combined["sentiment_factor"])
    )
    return df_combined

if __name__ == "__main__":
    conn = sqlite3.connect("urbanpulse.db")
    weather_df, sensor_df, social_df = fetch_data(conn)
    transformed_df = transform_data(weather_df, sensor_df, social_df)
    print("Transformed Data Preview:")
    print(transformed_df.head())

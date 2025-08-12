# transform/data_transform.py

import sqlite3
import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest

def fetch_data(conn):
    """Fetch data from the raw tables."""
    weather_df = pd.read_sql_query("SELECT * FROM weather", conn)
    sensor_df = pd.read_sql_query("SELECT * FROM sensor", conn)
    social_df = pd.read_sql_query("SELECT * FROM social", conn)
    return weather_df, sensor_df, social_df

def transform_data(weather_df, sensor_df, social_df):
    """Merge data, compute urban stress index, and detect anomalies."""
    if any(df.empty for df in [weather_df, sensor_df, social_df]):
        raise ValueError("One or more input DataFrames are empty")

    # Normalize features
    n = min(len(weather_df), len(sensor_df), len(social_df))
    weather_df = weather_df.iloc[:n]
    sensor_df = sensor_df.iloc[:n]
    social_df = social_df.iloc[:n]

    aqi_normalized = sensor_df['air_quality_index'] / 200.0
    noise_normalized = sensor_df['noise_level'] / 100.0
    sentiment_normalized = social_df['score']

    # Create combined DataFrame
    df_combined = pd.DataFrame({
        "timestamp": sensor_df["timestamp"],
        "temperature": weather_df["temperature"],
        "humidity": weather_df["humidity"],
        "air_quality_index": sensor_df["air_quality_index"],
        "noise_level": sensor_df["noise_level"],
        "sentiment_factor": sentiment_normalized
    })
    
    # Compute urban stress index
    df_combined["urban_stress_index"] = (
        0.4 * aqi_normalized +
        0.3 * noise_normalized +
        0.3 * (1 - sentiment_normalized)
    )
    
    # Anomaly detection
    iso_forest = IsolationForest(contamination=0.1, random_state=42)
    features = df_combined[["air_quality_index", "noise_level", "sentiment_factor"]]
    df_combined["anomaly"] = iso_forest.fit_predict(features)
    df_combined["anomaly"] = df_combined["anomaly"].map({1: "Normal", -1: "Anomaly"})
    
    return df_combined

if __name__ == "__main__":
    conn = sqlite3.connect("urbanpulse.db")
    weather_df, sensor_df, social_df = fetch_data(conn)
    transformed_df = transform_data(weather_df, sensor_df, social_df)
    print("Transformed Data Preview:")
    print(transformed_df.head())
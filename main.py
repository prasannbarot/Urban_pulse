# main.py

import sqlite3

def main():
    # --- Extraction Phase ---
    from extract.weather_extractor import fetch_weather
    from extract.sensor_extractor import fetch_sensor_data
    from extract.social_extractor import fetch_social_sentiment

    api_key = "API KEY"  # Replace with your API key
    weather_data = fetch_weather(city="Toronto", api_key=api_key)
    sensor_data = fetch_sensor_data()
    social_texts = [
        "Traffic is horrible!",
        "The air quality is amazing!",
        "Public transport is inefficient today."
    ]
    social_sentiments = fetch_social_sentiment(social_texts)

    # --- Loading Phase ---
    from load.db_loader import create_connection, create_tables, load_weather_data, load_sensor_data, load_social_data
    conn = create_connection()
    create_tables(conn)
    load_weather_data(conn, weather_data, city="Toronto")
    load_sensor_data(conn, sensor_data)
    for text, sentiment in zip(social_texts, social_sentiments):
        load_social_data(conn, text, sentiment)
    print("Data loaded successfully.")

    # --- Transformation Phase ---
    from transform.data_transform import fetch_data, transform_data
    weather_df, sensor_df, social_df = fetch_data(conn)
    transformed_df = transform_data(weather_df, sensor_df, social_df)
    print("Transformed Data Preview:")
    print(transformed_df.head())
    conn.close()

if __name__ == "__main__":
    main()

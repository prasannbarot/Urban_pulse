# main.py

import sqlite3
import yaml
import logging
from extract.weather_extractor import fetch_weather
from extract.sensor_extractor import fetch_sensor_data
from extract.social_extractor import fetch_social_sentiment
from load.db_loader import create_connection, create_tables, load_weather_data, load_sensor_data, load_social_data
from transform.data_transform import fetch_data, transform_data

# Configure logging
with open("config.yaml", "r") as f:
    config = yaml.safe_load(f)

logging.basicConfig(
    filename=config["logging"]["file"],
    level=config["logging"]["level"],
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def main():
    try:
        # --- Extraction Phase ---
        logging.info("Starting extraction phase")
        api_key = config["api"]["openweathermap_key"]
        city = config["cities"][0]  # Use first city for now
        weather_data = fetch_weather(city=city, api_key=api_key)
        sensor_data = fetch_sensor_data()
        social_texts = [
            "Traffic is horrible!",
            "The air quality is amazing!",
            "Public transport is inefficient today."
        ]
        social_sentiments = fetch_social_sentiment(social_texts)
        logging.info("Extraction completed successfully")

        # --- Loading Phase ---
        logging.info("Starting loading phase")
        conn = create_connection(db_file=config["database"]["path"])
        create_tables(conn)
        load_weather_data(conn, weather_data, city=city)
        load_sensor_data(conn, sensor_data)
        for text, sentiment in zip(social_texts, social_sentiments):
            load_social_data(conn, text, sentiment)
        logging.info("Data loaded successfully")

        # --- Transformation Phase ---
        logging.info("Starting transformation phase")
        weather_df, sensor_df, social_df = fetch_data(conn)
        transformed_df = transform_data(weather_df, sensor_df, social_df)
        logging.info("Transformed Data Preview:\n%s", transformed_df.head())
        conn.close()
        logging.info("Pipeline completed successfully")

    except Exception as e:
        logging.error(f"Pipeline failed: {str(e)}")
        raise

if __name__ == "__main__":
    main()
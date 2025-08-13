# main.py

import logging
import sqlite3
import yaml
import pandas as pd
from extract.weather_extractor import fetch_weather
from extract.sensor_extractor import fetch_sensor_data
from extract.social_extractor import fetch_social_sentiment
from load.db_loader import create_connection, create_tables, load_weather_data, load_sensor_data, load_social_data
from transform.data_transform import transform_data

# Configure logging
with open("config.yaml", "r") as f:
    config = yaml.safe_load(f)

logging.basicConfig(
    filename=config["logging"]["file"],
    level=getattr(logging, config["logging"]["level"]),
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

def main():
    logger.info("Starting Urban Pulse pipeline")
    
    try:
        # Initialize database
        conn = create_connection(config["database"]["path"])
        create_tables(conn)
        
        # Fetch and load weather data for all cities
        api_key = config["api"]["openweathermap_key"]
        for city in config["cities"]:
            logger.info(f"Fetching weather data for {city}")
            weather_data = fetch_weather(city=city, api_key=api_key)
            if weather_data:
                load_weather_data(conn, weather_data, city=city)
                logger.info(f"Weather data loaded for {city}")
            else:
                logger.warning(f"No weather data fetched for {city}")
        
        # Fetch and load sensor data
        sensor_data = fetch_sensor_data()
        load_sensor_data(conn, sensor_data)
        logger.info("Sensor data loaded successfully")
        
        # Fetch and load social sentiment data
        sample_texts = [
            "Traffic is horrible!",
            "The city environment is amazing today.",
            "Public transport is really unreliable."
        ]
        social_sentiments = fetch_social_sentiment(sample_texts)
        for text, sentiment in zip(sample_texts, social_sentiments):
            load_social_data(conn, text, sentiment)
        logger.info("Social sentiment data loaded successfully")
        
        # Transform data
        logger.info("Starting transformation phase")
        weather_df = pd.read_sql_query("SELECT * FROM weather", conn)
        sensor_df = pd.read_sql_query("SELECT * FROM sensor", conn)
        social_df = pd.read_sql_query("SELECT * FROM social", conn)
        transformed_df = transform_data(weather_df, sensor_df, social_df)
        transformed_df.to_sql("urban_stress", conn, if_exists="replace", index=False)
        logger.info("Data transformation and loading completed")
        
        conn.close()
        
    except Exception as e:
        logger.error(f"Pipeline failed: {str(e)}")
        raise

if __name__ == "__main__":
    main()
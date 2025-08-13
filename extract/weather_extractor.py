# extract/weather_extractor.py

import requests
import json
import yaml
import logging

logger = logging.getLogger(__name__)

def fetch_weather(city="Toronto", api_key=None):
    """Fetch weather data for a given city."""
    if not api_key:
        with open("config.yaml", "r") as f:
            config = yaml.safe_load(f)
        api_key = config["api"]["openweathermap_key"]
    
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        logger.info(f"Successfully fetched weather data for {city}")
        return data
    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to fetch weather data for {city}: {str(e)}")
        return None

def save_weather_data(data, city, filename=None):
    """Save weather data to a JSON file."""
    if not filename:
        filename = f"data/sample/weather_{city}.json"
    try:
        with open(filename, "w") as f:
            json.dump(data, f, indent=4)
        logger.info(f"Saved weather data for {city} to {filename}")
    except Exception as e:
        logger.error(f"Failed to save weather data for {city}: {str(e)}")

if __name__ == "__main__":
    with open("config.yaml", "r") as f:
        config = yaml.safe_load(f)
    cities = config["cities"]
    for city in cities:
        weather_data = fetch_weather(city=city)
        if weather_data:
            save_weather_data(weather_data, city)
            print(f"Weather Data for {city}:", weather_data)
        else:
            print(f"Failed to fetch weather data for {city}")
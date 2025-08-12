# extract/weather_extractor.py

import requests
import json
import yaml

def fetch_weather(city="Toronto", api_key=None):
    """Fetch weather data for a given city."""
    if not api_key:
        with open("config.yaml", "r") as f:
            config = yaml.safe_load(f)
        api_key = config["api"]["openweathermap_key"]
    
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Error fetching weather data for {city}: {response.status_code}")

def save_weather_data(data, city, filename=None):
    """Save weather data to a JSON file."""
    if not filename:
        filename = f"data/sample/weather_{city}.json"
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)

if __name__ == "__main__":
    with open("config.yaml", "r") as f:
        config = yaml.safe_load(f)
    cities = config["cities"]
    for city in cities:
        weather_data = fetch_weather(city=city)
        print(f"Weather Data for {city}:", weather_data)
        save_weather_data(weather_data, city)
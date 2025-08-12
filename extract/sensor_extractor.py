# extract/sensor_extractor.py

import random
import datetime
import math

def fetch_sensor_data():
    """
    Simulate sensor data with diurnal patterns.
    Returns a dictionary.
    """
    now = datetime.datetime.now()
    hour = now.hour
    # Simulate diurnal air quality (worse during rush hours)
    aqi_base = 50 + 50 * math.sin(math.pi * hour / 12)
    aqi = min(max(int(aqi_base + random.gauss(0, 10)), 0), 200)
    # Simulate noise level (higher during day)
    noise_base = 30 + 40 * math.cos(math.pi * hour / 12)
    noise = round(min(max(noise_base + random.gauss(0, 5), 20), 100), 2)
    
    data = {
        "timestamp": now.isoformat(),
        "air_quality_index": aqi,
        "noise_level": noise
    }
    return data

if __name__ == "__main__":
    sensor_data = fetch_sensor_data()
    print("Sensor Data:", sensor_data)
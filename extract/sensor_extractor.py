# extract/sensor_extractor.py

import random
import datetime

def fetch_sensor_data():
    """
    Simulate sensor data extraction (e.g., air quality, noise level).
    Returns a dictionary.
    """
    data = {
        "timestamp": datetime.datetime.now().isoformat(),
        "air_quality_index": random.randint(50, 150),
        "noise_level": round(random.uniform(20, 100), 2)
    }
    return data

if __name__ == "__main__":
    sensor_data = fetch_sensor_data()
    print("Sensor Data:", sensor_data)

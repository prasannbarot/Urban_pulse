# orchestration/urban_pulse_dag.py

from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import logging
import yaml

default_args = {
    'owner': 'urban_pulse',
    'depends_on_past': False,
    'start_date': datetime(2025, 6, 14),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 3,
    'retry_delay': timedelta(minutes=5),
}

def setup_logging():
    logging.basicConfig(
        filename='urban_pulse.log',
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )

def run_extraction(**kwargs):
    from extract.weather_extractor import fetch_weather, save_weather_data
    from extract.sensor_extractor import fetch_sensor_data
    from extract.social_extractor import fetch_social_sentiment
    setup_logging()
    with open("config.yaml", "r") as f:
        config = yaml.safe_load(f)
    
    logging.info("Starting extraction")
    api_key = config["api"]["openweathermap_key"]
    cities = config["cities"]
    for city in cities:
        data = fetch_weather(city=city, api_key=api_key)
        save_weather_data(data, city)
    sensor_data = fetch_sensor_data()
    social_texts = [
        "Traffic is horrible!",
        "The air quality is amazing!",
        "Public transport is inefficient today."
    ]
    social_sentiments = fetch_social_sentiment(social_texts)
    logging.info("Extraction completed")
    return {"weather": {city: f"data/sample/weather_{city}.json" for city in cities},
            "sensor": sensor_data, "social": list(zip(social_texts, social_sentiments))}

def run_loading(**kwargs):
    from load.db_loader import create_connection, create_tables, load_weather_data, load_sensor_data, load_social_data
    import json
    setup_logging()
    logging.info("Starting loading")
    conn = create_connection()
    create_tables(conn)
    with open("config.yaml", "r") as f:
        config = yaml.safe_load(f)
    
    # Load weather data
    for city in config["cities"]:
        with open(f"data/sample/weather_{city}.json", "r") as f:
            weather_data = json.load(f)
        load_weather_data(conn, weather_data, city=city)
    
    # Load sensor and social data
    ti = kwargs['ti']
    extracted_data = ti.xcom_pull(task_ids='extract_task')
    load_sensor_data(conn, extracted_data["sensor"])
    for text, sentiment in extracted_data["social"]:
        load_social_data(conn, text, sentiment)
    logging.info("Loading completed")
    conn.close()

def run_transformation(**kwargs):
    from transform.data_transform import fetch_data, transform_data
    import sqlite3
    setup_logging()
    logging.info("Starting transformation")
    conn = sqlite3.connect("urbanpulse.db")
    weather_df, sensor_df, social_df = fetch_data(conn)
    transformed = transform_data(weather_df, sensor_df, social_df)
    logging.info("Transformed Data:\n%s", transformed.head())
    conn.close()

dag = DAG('urban_pulse_etl', default_args=default_args, schedule_interval=timedelta(hours=1))

t1 = PythonOperator(task_id='extract_task', python_callable=run_extraction, dag=dag)
t2 = PythonOperator(task_id='load_task', python_callable=run_loading, provide_context=True, dag=dag)
t3 = PythonOperator(task_id='transform_task', python_callable=run_transformation, dag=dag)

t1 >> t2 >> t3
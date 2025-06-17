# orchestration/urban_pulse_dag.py

"""
Sample Airflow DAG for Urban Pulse ELT pipeline.
Note: Adjust paths and configuration when deploying in an Airflow environment.
"""

from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'urban_pulse',
    'depends_on_past': False,
    'start_date': datetime(2025, 6, 14),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

def run_extraction(**kwargs):
    from extract.weather_extractor import fetch_weather, save_weather_data
    api_key = "YOUR_OPENWEATHER_API_KEY"
    data = fetch_weather(city="Toronto", api_key=api_key)
    save_weather_data(data, filename="data/sample/weather_Toronto.json")

def run_loading(**kwargs):
    from load.db_loader import create_connection, create_tables, load_weather_data
    import json
    conn = create_connection()
    create_tables(conn)
    with open("data/sample/weather_Toronto.json", "r") as f:
        weather_data = json.load(f)
    load_weather_data(conn, weather_data, city="Toronto")

def run_transformation(**kwargs):
    from transform.data_transform import fetch_data, transform_data
    import sqlite3
    conn = sqlite3.connect("urbanpulse.db")
    weather_df, sensor_df, social_df = fetch_data(conn)
    transformed = transform_data(weather_df, sensor_df, social_df)
    print("Transformed Data:")
    print(transformed.head())

dag = DAG('urban_pulse_etl', default_args=default_args, schedule_interval=timedelta(hours=1))

t1 = PythonOperator(task_id='extract_task', python_callable=run_extraction, dag=dag)
t2 = PythonOperator(task_id='load_task', python_callable=run_loading, dag=dag)
t3 = PythonOperator(task_id='transform_task', python_callable=run_transformation, dag=dag)

t1 >> t2 >> t3

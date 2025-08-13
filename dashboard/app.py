# dashboard/app.py

import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px
import yaml
import sys
import os

# Add project root to Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

DB_PATH = "urbanpulse.db"

def load_table(table_name):
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query(f"SELECT * FROM {table_name}", conn)
    conn.close()
    return df

# Load config
try:
    with open("config.yaml", "r") as f:
        config = yaml.safe_load(f)
except FileNotFoundError:
    st.error("Configuration file (config.yaml) not found. Please ensure it exists in the project root.")
    config = {"cities": ["Toronto", "Vancouver", "Montreal"]}

st.title("🌆 Urban Pulse Dashboard")
st.markdown("Real-time insights into urban well-being based on environment and sentiment.")

# City filter
city = st.selectbox("Select City", config["cities"])

# Weather Data
st.header("🌤️ Weather Data")
weather_df = load_table("weather")
if not weather_df.empty:
    weather_df = weather_df[weather_df["city"] == city]
    if not weather_df.empty:
        st.dataframe(weather_df)
        fig1 = px.histogram(weather_df, x="temperature", nbins=10, title=f"Temperature Distribution in {city}")
        st.plotly_chart(fig1)
    else:
        st.warning(f"No weather data available for {city}. Run `python main.py` to fetch data.")
else:
    st.warning("No weather data available. Run `python main.py` to fetch data.")

# Sensor Data
st.header("🌫️ Sensor Data")
sensor_df = load_table("sensor")
if not sensor_df.empty:
    st.dataframe(sensor_df)
    fig2 = px.histogram(sensor_df, x="air_quality_index", nbins=10, title="Air Quality Index Distribution", color_discrete_sequence=['orange'])
    st.plotly_chart(fig2)
else:
    st.warning("No sensor data available. Run `python main.py` to fetch data.")

# Social Sentiment Data
st.header("💬 Social Sentiment")
social_df = load_table("social")
if not social_df.empty:
    st.dataframe(social_df)
    fig3 = px.bar(social_df["label"].value_counts(), title="Sentiment Distribution")
    st.plotly_chart(fig3)
else:
    st.warning("No social sentiment data available. Run `python main.py` to fetch data.")

# Urban Stress Index
st.header("📈 Urban Stress Index")
conn = sqlite3.connect(DB_PATH)
weather_df, sensor_df, social_df = pd.read_sql_query("SELECT * FROM weather", conn), \
                                  pd.read_sql_query("SELECT * FROM sensor", conn), \
                                  pd.read_sql_query("SELECT * FROM social", conn)
from transform.data_transform import transform_data
transformed_df = transform_data(weather_df, sensor_df, social_df)
if not transformed_df.empty:
    fig4 = px.line(transformed_df, x="timestamp", y="urban_stress_index", title="Urban Stress Index Over Time")
    st.plotly_chart(fig4)
else:
    st.warning("No urban stress index data available. Ensure data is loaded in the database.")
conn.close()
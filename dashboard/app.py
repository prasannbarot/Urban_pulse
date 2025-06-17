# dashboard/app.py

import streamlit as st
import pandas as pd
import sqlite3
import matplotlib.pyplot as plt

def get_weather_data(db_path="urbanpulse.db"):
    conn = sqlite3.connect(db_path)
    df = pd.read_sql_query("SELECT * FROM weather", conn)
    conn.close()
    return df

st.title("🌆 Urban Pulse Dashboard")
st.write("Real-Time Insights on Urban Wellbeing")

# Display Weather Data
df_weather = get_weather_data()
st.write("### Weather Data")
st.dataframe(df_weather)

# Plot temperature distribution if available
if "temperature" in df_weather.columns:
    st.write("### Temperature Distribution")
    fig, ax = plt.subplots()
    df_weather['temperature'].hist(ax=ax)
    st.pyplot(fig)

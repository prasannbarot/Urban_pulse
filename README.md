# 🌆 Urban Pulse

**A real-time modular ELT pipeline & machine learning system for analyzing urban well-being.**  
This project extracts live data from APIs (e.g., weather, simulated sensors, and social sentiment), loads and stores it in a structured database, performs transformations and ML processing, and visualizes actionable insights via an interactive Streamlit dashboard.

---

## 🚀 Features

- 🛰️ **Modular ELT Pipeline**: Decoupled modules for Extract, Load, and Transform steps using real-time and simulated data
- 🔍 **Sentiment Analysis**: Uses state-of-the-art NLP to assess public sentiment from city-related texts
- ☁️ **Weather & Sensor Streams**: Integrates real-time weather APIs and simulated air quality/noise data
- 📈 **Urban Stress Index**: Derived metric combining environmental and social indicators
- 📊 **Interactive Dashboard**: Built with Streamlit to visualize temperature, humidity, sentiment, and stress levels
- 📦 **SQLite Database**: Lightweight persistent storage with minimal setup
- ⚙️ **Main Execution Script**: Orchestrates the full ELT process in one command
- 🧠 **Expandable ML Architecture**: Easily extendable to supervised learning, anomaly detection, or time-series forecasting
- ⏱️ **Airflow-Compatible Orchestration**: Sample DAG included for advanced scheduling
- ☁️ **Docker Ready**: Optional Dockerfile for containerized deployment

---

## 📂 Directory Structure

urban-pulse/ <br>
├── data/ <br>
│   ├── sample/     <br>                  
│   │   └── weather_Toronto.json      # Sample weather JSON (created during testing) <br>
│   └── schemas/                      # (Optional) JSON schemas for raw data validation <br>
│
├── extract/
│   ├── __init__.py                   # (Empty file to mark package)
│   ├── weather_extractor.py          # Fetches weather data from OpenWeatherMap
│   ├── sensor_extractor.py           # Simulates sensor data extraction (e.g. air quality)
│   └── social_extractor.py           # Uses transformers to perform sentiment analysis on social texts
│
├── load/
│   ├── __init__.py
│   └── db_loader.py                  # Loads extracted data into a SQLite database
│
├── transform/
│   ├── __init__.py
│   └── data_transform.py             # Transforms and merges raw data, calculates an urban stress index
│
├── dashboard/
│   ├── __init__.py
│   └── app.py                        # A Streamlit dashboard to visualize the data
│
├── orchestration/
│   ├── __init__.py
│   └── urban_pulse_dag.py            # A sample Airflow DAG for scheduling the pipeline (optional)
│
├── main.py                           # The main script to run the complete ELT pipeline
├── requirements.txt                  # A list of required Python packages
├── Dockerfile                        # (Optional) To containerize the project
├── .gitignore                        # Files and folders to ignore in Git
└── README.md                         # Project overview and setup instructions




---

## 🛠️ Technologies

| Layer             | Stack                                                                 |
|------------------|------------------------------------------------------------------------|
| Language          | Python 3.x                                                             |
| Libraries         | `pandas`, `requests`, `transformers`, `scikit-learn`, `streamlit`     |
| Storage           | SQLite                                                                 |
| Dashboard         | Streamlit                                                              |
| ML/NLP            | HuggingFace Transformers (`distilBERT`, `VADER`)                      |
| Orchestration     | Apache Airflow (optional DAG provided)                                |
| Deployment        | Streamlit Cloud or Docker                                              |

---

## 🔁 ELT Workflow Overview

1. **Extract**  
   - Weather data from OpenWeatherMap API  
   - Sensor data (simulated air quality and noise)  
   - Social text sentiment using HuggingFace or NLTK  

2. **Load**  
   - Persisted to local SQLite database  

3. **Transform**  
   - Merges multimodal data  
   - Calculates Urban Stress Index  

4. **Visualize**  
   - Interactive visual analytics via Streamlit  

---

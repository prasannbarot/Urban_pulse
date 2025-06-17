# Urban Pulse - A Comprehensive ELT Data Science Project

## Overview
Urban Pulse demonstrates a complete ELT (Extract, Load, Transform) pipeline where data from Multiple sources—weather APIs, simulated sensors, and social media sentiment—are processed, loaded into a SQLite database, transformed into actionable insights (like an urban stress index), and finally visualized via a Streamlit dashboard.

## Repository Structure

urban-pulse/
├── data/
│   ├── sample/                       
│   │   └── weather_Toronto.json      # Sample weather JSON (created during testing)
│   └── schemas/                      # (Optional) JSON schemas for raw data validation
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

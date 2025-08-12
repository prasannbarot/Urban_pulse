# 🌆 Urban Pulse

**A real-time modular ELT pipeline & machine learning system for analyzing urban well-being.**

This project extracts live data from APIs (e.g., weather, simulated sensors, and social sentiment), loads it into a SQLite database, performs transformations and ML processing (including anomaly detection), and visualizes actionable insights via an interactive Streamlit dashboard.

## 🚀 Features

- 🛰️ **Modular ELT Pipeline**: Decoupled extract, load, and transform steps with configuration management.
- 🔍 **Sentiment Analysis**: Uses DistilBERT for advanced NLP on city-related texts.
- ☁️ **Weather & Sensor Streams**: Integrates OpenWeatherMap API and realistic simulated sensor data.
- 📈 **Urban Stress Index**: Normalized metric combining environmental and social factors.
- 📊 **Interactive Dashboard**: Streamlit with Plotly for dynamic visualizations.
- 📦 **SQLite Database**: Lightweight storage with indexing for performance.
- ⚙️ **Main Execution Script**: Orchestrates the pipeline with logging and error handling.
- 🧠 **Expandable ML Architecture**: Includes anomaly detection with Isolation Forest.
- ⏱️ **Airflow-Compatible Orchestration**: Sample DAG for scheduling.
- ☁️ **Docker Ready**: Containerized deployment with Dockerfile.

## 📂 Directory Structure

```
urban-pulse/
├── data/
│   ├── sample/
│   │   └── weather_Toronto.json
│   └── schemas/
├── extract/
│   ├── weather_extractor.py
│   ├── sensor_extractor.py
│   ├── social_extractor.py
│   └── __init__.py
├── load/
│   ├── db_loader.py
│   └── __init__.py
├── transform/
│   ├── data_transform.py
│   └── __init__.py
├── dashboard/
│   ├── app.py
│   └── __init__.py
├── orchestration/
│   ├── urban_pulse_dag.py
│   └── __init__.py
├── main.py
├── config.yaml
├── requirements.txt
├── Dockerfile
├── .gitignore
└── README.md
```

## 🛠️ Technologies

| Layer             | Stack                                                                |
|-------------------|----------------------------------------------------------------------|
| Language          | Python 3.x                                                           |
| Libraries         | `pandas`, `requests`, `transformers`, `scikit-learn`, `streamlit`, `plotly`, `pyyaml` |
| Storage           | SQLite                                                               |
| Dashboard         | Streamlit with Plotly                                                |
| ML/NLP            | HuggingFace Transformers (`distilbert-base-uncased-finetuned-sst-2-english`) |
| Anomaly Detection | Scikit-learn Isolation Forest                                         |
| Orchestration     | Apache Airflow (optional DAG)                                        |
| Deployment        | Docker or Streamlit Cloud                                            |

## 🔁 ELT Workflow Overview

1. **Extract**  
   - Weather data from OpenWeatherMap API (multi-city support).  
   - Simulated sensor data (air quality, noise) with diurnal patterns.  
   - Social sentiment using DistilBERT.  

2. **Load**  
   - Data persisted to SQLite with indexing for performance.  

3. **Transform**  
   - Merges multimodal data and computes a normalized Urban Stress Index.  
   - Detects anomalies using Isolation Forest.  

4. **Visualize**  
   - Interactive Streamlit dashboard with Plotly charts and city filters.

## 🛠️ Setup Instructions

### Prerequisites
- Python 3.9+
- VS Code (for development)
- Docker (optional, for containerized deployment)

### Local Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/prasannbarot/Urban_pulse.git
   cd Urban_pulse
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Update `config.yaml` with your OpenWeatherMap API key.
4. Run the pipeline:
   ```bash
   python main.py
   ```
5. Launch the dashboard:
   ```bash
   streamlit run dashboard/app.py
   ```

### Docker Setup
1. Build the Docker image:
   ```bash
   docker build -t urban_pulse .
   ```
2. Run the container:
   ```bash
   docker run -p 8501:8501 urban_pulse
   ```
3. Access the dashboard at `http://localhost:8501`.

### Airflow Setup
1. Install Apache Airflow:
   ```bash
   pip install apache-airflow
   ```
2. Move `orchestration/urban_pulse_dag.py` to your Airflow DAGs folder.
3. Start Airflow and trigger the `urban_pulse_etl` DAG.

## 📸 Screenshots
*Add screenshots of the Streamlit dashboard here for GitHub/LinkedIn.*

## 🚀 Future Enhancements
- Add time-series forecasting for Urban Stress Index.
- Integrate real social media APIs (e.g., Twitter/X).
- Expand anomaly detection with clustering algorithms.
- Deploy dashboard to Streamlit Cloud.

## 📜 License
MIT License. See [LICENSE](LICENSE.txt) for details.

## 👤 Author
*Built with 💻 by [Prasann Barot](https://linkedin.com/in/prasannbarot).*

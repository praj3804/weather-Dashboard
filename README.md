
#  Interactive Weather Dashboard

An **interactive weather forecasting dashboard** built with [Streamlit](https://streamlit.io/) and the [OpenWeather API](https://openweathermap.org/api).  
This app allows users to view forecasts, compare two cities side by side, check alerts, and download forecast data.  

---

##  Features

- 📍 **Current Weather Conditions**
  - Temperature, humidity, wind speed, rainfall, and cloudiness.
  - Comfort index (temperature + humidity factor).

- 📊 **Forecast Trends**
  - Interactive charts for temperature, humidity, wind speed, cloudiness, and rainfall.

- 📝 **AI-like Summaries**
  - Simple text-based forecast summaries.

- ⚠️ **Weather Alerts**
  - Heatwave, cold wave, and heavy rainfall warnings.

- 🔄 **Comparison Mode**
  - Compare two cities side by side with charts for **temperature** and **rainfall**.

- 🕘 **Search History**
  - Quick access to your 5 most recent searches.

- 📥 **Download Data**
  - Export forecast as CSV.

---

## 🚀 Installation

Clone the repository:

```bash
git clone https://github.com/your-username/weather-dashboard.git
cd weather-dashboard
````

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## 🔑 API Key Setup

1. Sign up at [OpenWeather](https://home.openweathermap.org/users/sign_up) to get a **free API key**.
2. In the code, replace:

```python
API_KEY = "your_api_key_here"
```

with your actual key.

⚠️ **Tip**: When deploying publicly (e.g., on Streamlit Cloud), don’t hardcode your API key.
Instead, store it as a **secret** in `.streamlit/secrets.toml`:

```toml
API_KEY = "your_api_key_here"
```

And access it in your code with:

```python
import streamlit as st
API_KEY = st.secrets["API_KEY"]
```

---

## ▶️ Run the App

```bash
streamlit run app.py
```

Open your browser at **[http://localhost:8501](http://localhost:8501)**.

---

## 📦 Deployment

You can deploy this app for free on **[Streamlit Community Cloud](https://streamlit.io/cloud)**:

1. Push your code to GitHub.
2. Go to Streamlit Cloud → New app.
3. Connect your repo and branch.
4. Add your **API key** in *Secrets Manager*.
5. Deploy 🚀.

---

## 📸 Screenshots

### Single City Dashboard

* Current conditions, alerts, trends, and downloadable data.

### City Comparison

* Side-by-side comparison of two cities with trend charts.

---

## 🛠️ Tech Stack

* [Streamlit](https://streamlit.io/) – interactive web UI
* [Pandas](https://pandas.pydata.org/) – data manipulation
* [Requests](https://docs.python-requests.org/) – API calls
* [Geocoder](https://geocoder.readthedocs.io/) – location-based defaults
* [OpenWeather API](https://openweathermap.org/api) – weather data source

---

## 📄 License

This project is open-source and free to use under the **MIT License**.

---



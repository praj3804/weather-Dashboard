import requests
import streamlit as st
import pandas as pd
from datetime import datetime
import pycountry
import geocoder

API_KEY = st.secrets["API_KEY"] # you go to the openWeather api signin for free and use it for your dashboard


# ---------- Helper Functions ----------
def get_weather_data(city, units="metric"):
    """Fetch forecast data from OpenWeather API"""
    url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}&units={units}"
    response = requests.get(url).json()
    return response

def process_data(response):
    """Extract relevant fields into a DataFrame"""
    data = []
    for entry in response["list"]:
        time = datetime.strptime(entry["dt_txt"], "%Y-%m-%d %H:%M:%S")
        temp = entry["main"]["temp"]
        feels_like = entry["main"]["feels_like"]
        humidity = entry["main"]["humidity"]
        wind = entry["wind"]["speed"]
        weather = entry["weather"][0]["description"].title()
        clouds = entry["clouds"]["all"]
        rain = entry.get("rain", {}).get("3h", 0)  # rainfall in last 3h (mm)
        data.append({
            "time": time, 
            "temperature": temp, 
            "feels_like": feels_like,
            "humidity": humidity, 
            "wind_speed": wind,
            "weather": weather,
            "cloudiness": clouds,
            "rainfall": rain
        })
    return pd.DataFrame(data)

def calculate_comfort_index(temp, humidity):
    """Simple comfort index: combines temperature and humidity"""
    return round(temp + (0.1 * humidity), 1)

def generate_summary(df):
    """Generate a simple AI-like summary"""
    avg_temp = df['temperature'].mean()
    avg_hum = df['humidity'].mean()
    rain_days = df[df['rainfall'] > 0]['time'].dt.day_name().unique()
    
    summary = f"Expect an average temperature of {avg_temp:.1f}°C with humidity around {avg_hum:.0f}%. "
    if len(rain_days) > 0:
        summary += f"Rain is likely on {', '.join(rain_days)}."
    else:
        summary += "Mostly dry conditions expected."
    return summary

# ---------- Dashboard ----------
st.set_page_config(page_title="Weather Dashboard", page_icon="🌍", layout="wide")

st.title("Interactive Weather Dashboard")
st.caption("Powered by OpenWeather API | Built with Streamlit")

# Sidebar controls
st.sidebar.header("Customize Your Screen..")

# --- Auto unit detection ---
g = geocoder.ip("me")
region = g.country
unit_auto = "metric" if region not in ["US", "BS", "BZ", "KY", "PW"] else "imperial"
unit = st.sidebar.radio("Select Unit", ["Auto", "Celsius", "Fahrenheit"])
if unit == "Auto":
    unit_api = unit_auto
    unit_label = "C" if unit_auto == "metric" else "F"
else:
    unit_api = "metric" if unit == "Celsius" else "imperial"
    unit_label = "C" if unit == "Celsius" else "F"

# --- Search history ---
if "history" not in st.session_state:
    st.session_state.history = []

# Toggle compare mode
compare_mode = st.sidebar.checkbox("Compare Two Cities?")

if compare_mode:
    city1 = st.sidebar.text_input("Enter first city (City,CountryCode)", "Delhi,IN")
    city2 = st.sidebar.text_input("Enter second city (City,CountryCode)", "Mumbai,IN")
    cities = [city1, city2]
else:
    city = st.sidebar.text_input("Enter city (City,CountryCode)", "Delhi,IN")
    cities = [city]

# --- Main Section ---
weather_data = {}
for c in cities:
    if c:
        response = get_weather_data(c, units=unit_api)
        if "list" in response:
            df = process_data(response)
            weather_data[c] = df
            # Keep search history
            if c not in st.session_state.history:
                st.session_state.history.insert(0, c)
                st.session_state.history = st.session_state.history[:5]
        else:
            st.error(f"⚠️ Could not fetch forecast for {c}")

if weather_data:
    if compare_mode and len(weather_data) == 2:
        st.subheader("📊 Comparison Between Two Cities")
        col1, col2 = st.columns(2)
        for idx, (city, df) in enumerate(weather_data.items()):
            current = df.iloc[0]
            with (col1 if idx == 0 else col2):
                st.metric(f"{city} Temp", f"{current['temperature']}°{unit_label}")
                st.metric("Humidity", f"{current['humidity']} %")
                st.metric("Wind", f"{current['wind_speed']} m/s")
                st.metric("Comfort Index", f"{calculate_comfort_index(current['temperature'], current['humidity'])}")
                st.write(generate_summary(df))

        # Trend comparison
        st.subheader("🌡️ Temperature Comparison")
        temp_df = pd.DataFrame()
        for city, df in weather_data.items():
            df_city = df[["time", "temperature"]].copy()
            df_city.rename(columns={"temperature": city}, inplace=True)
            if temp_df.empty:
                temp_df = df_city
            else:
                temp_df = temp_df.merge(df_city, on="time")
        st.line_chart(temp_df.set_index("time"))

        st.subheader("🌧️ Rainfall Comparison")
        rain_df = pd.DataFrame()
        for city, df in weather_data.items():
            df_city = df[["time", "rainfall"]].copy()
            df_city.rename(columns={"rainfall": city}, inplace=True)
            if rain_df.empty:
                rain_df = df_city
            else:
                rain_df = rain_df.merge(df_city, on="time")
        st.bar_chart(rain_df.set_index("time"))

    else:
        # Single city dashboard
        for city, df in weather_data.items():
            st.subheader(f"📍 Current Weather in {city}")
            current = df.iloc[0]

            col1, col2, col3, col4 = st.columns(4)
            col1.metric("🌡️ Temp", f"{current['temperature']}°{unit_label}")
            col2.metric("💧 Humidity", f"{current['humidity']} %")
            col3.metric("💨 Wind", f"{current['wind_speed']} m/s")
            col4.metric("🌡️ Comfort Index", f"{calculate_comfort_index(current['temperature'], current['humidity'])}")

            st.write(f"**Condition:** {current['weather']} | ☁️ Cloudiness: {current['cloudiness']}% | 🌧️ Rainfall (last 3h): {current['rainfall']} mm")

            # Alerts
            if current["rainfall"] > 20:
                st.error("⚠️ Flooding risk due to heavy rainfall!")
            elif current["temperature"] > 35 and unit_api == "metric":
                st.warning("🥵 Heatwave risk! Stay hydrated.")
            elif current["temperature"] < 10 and unit_api == "metric":
                st.info("🥶 Cold wave risk. Dress warmly!")
            else:
                st.success("😊 Normal weather conditions.")

            # AI-like summary
            st.subheader("📝 Weather Summary")
            st.write(generate_summary(df))

            # Visualizations
            tab1, tab2, tab3, tab4, tab5 = st.tabs([
                "🌡️ Temperature", "💧 Humidity", "💨 Wind Speed", "☁️ Cloudiness", "🌧️ Rainfall"
            ])
            with tab1:
                st.line_chart(df.set_index("time")["temperature"])
            with tab2:
                st.area_chart(df.set_index("time")["humidity"])
            with tab3:
                st.bar_chart(df.set_index("time")["wind_speed"])
            with tab4:
                st.area_chart(df.set_index("time")["cloudiness"])
            with tab5:
                st.bar_chart(df.set_index("time")["rainfall"])

            # Download option
            st.subheader("📥 Download Forecast Data")
            csv = df.to_csv(index=False).encode("utf-8")
            st.download_button(
                label="Download as CSV",
                data=csv,
                file_name=f"{city}_forecast.csv",
                mime="text/csv",
            )

# --- Sidebar history ---
if st.session_state.history:
    st.sidebar.markdown("🕘 Recent Searches:")
    for c in st.session_state.history:
        if st.sidebar.button(c):
            city = c

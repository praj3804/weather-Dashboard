
import requests
import streamlit as st



import pandas as pd

API_KEY = "ac5e7fdd599e092153162a8e2a459500" # you go to the openWeather api signin for free and use it for your dashboard
st.title("Temperature Trend Dashboard") 

# User input would have to be in a certain format or else the api wouldnt work therefore specify a certain format as default
CITY = st.text_input("Enter a city name:", "Delhi,IN")

if CITY:
    url = f"http://api.openweathermap.org/data/2.5/forecast?q={CITY}&appid={API_KEY}&units=metric"# url to make sure it knows where to take data from  
    response = requests.get(url).json()

    if "list" in response:  # valid response
        # Extract forecast data
        data = []
        for entry in response["list"]:
            time = entry["dt_txt"]
            temp = entry["main"]["temp"]
            data.append({"time": time, "temperature": temp})

        df = pd.DataFrame(data)

        # Show latest temp
        latest_temp = df["temperature"].iloc[0]
        st.metric(label=f"Current Temp in {CITY}", value=f"{latest_temp} °C")
        if latest_temp>35:
            'Too hot 🥵 suspecting hot wave... '# a very vague description to classify if its hot cold or normal
        elif latest_temp<10:
            'Too cold 🥶 suspecting cold wave... '
        else:
            'Normal ☺️'

        # Line chart of forecast trend
        st.subheader("📈 Temperature Trend (Next 5 Days, every 3 hours)")
        st.line_chart(df.set_index("time"))

    else:
        st.error("⚠️ Could not fetch forecast. Try again with City,CountryCode (e.g., Delhi,IN)")
        #this is required to make sure we understand why it isnt working if we put a wrong location

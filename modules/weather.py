import streamlit as st
import requests
from utils.gemini_client import ask_gemini
import os
from dotenv import load_dotenv

load_dotenv()

DISTRICT_COORDS = {
    "Lucknow": (26.85, 80.95),
    "Agra": (27.18, 78.01),
    "Varanasi": (25.32, 83.01),
    "Amritsar": (31.63, 74.87),
    "Ludhiana": (30.90, 75.85),
    "Patiala": (30.34, 76.39),
    "Chennai": (13.08, 80.27),
    "Coimbatore": (11.01, 76.96),
    "Madurai": (9.93, 78.12),
    "Jaipur": (26.91, 75.79),
    "Bhopal": (23.25, 77.41),
    "Nagpur": (21.15, 79.09),
    "Pune": (18.52, 73.86),
    "Hyderabad": (17.38, 78.48),
    "Bengaluru": (12.97, 77.59),
}

CROP_RULES = {
    "Wheat":     {"frost": 8,  "flood": 40, "heat": 35},
    "Rice":      {"frost": 15, "flood": 60, "heat": 38},
    "Tomato":    {"frost": 10, "flood": 30, "heat": 35},
    "Mustard":   {"frost": 5,  "flood": 35, "heat": 32},
    "Sugarcane": {"frost": 12, "flood": 70, "heat": 40},
    "Cotton":    {"frost": 15, "flood": 45, "heat": 42},
}

def check_risks(forecast, crop):
    alerts = []
    rules = CROP_RULES.get(crop, CROP_RULES["Wheat"])
    for day in forecast:
        temp_min = day.get("temp_min", 20)
        temp_max = day.get("temp_max", 30)
        rain = day.get("rain", 0)
        if temp_min < rules["frost"]:
            alerts.append(f"🔴 Frost risk — temp dropping to {temp_min}°C. Cover seedlings.")
        if rain > rules["flood"]:
            alerts.append(f"🔴 Waterlogging risk — {rain}mm rain expected. Check drainage.")
        if temp_max > rules["heat"]:
            alerts.append(f"🟡 Heat stress — {temp_max}°C expected. Irrigate early morning.")
    return list(set(alerts))

def render():
    st.header("🌦 Weather Risk Forecasting")

    district = st.session_state.get("district", "Lucknow")
    crop = st.session_state.get("crop", "Wheat")

    if district not in DISTRICT_COORDS:
        st.warning(f"{district} not in database. Showing Lucknow data.")
        district = "Lucknow"

    lat, lon = DISTRICT_COORDS[district]
    api_key = os.getenv("OPENWEATHER_API_KEY")

    if not api_key:
        st.error("OpenWeather API key missing in .env file.")
        return

    url = f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={api_key}&units=metric"

    with st.spinner("Fetching weather data..."):
        try:
            res = requests.get(url, timeout=10)
            data = res.json()

            forecast = []
            seen_dates = []
            for item in data.get("list", []):
                date = item["dt_txt"].split(" ")[0]
                if date not in seen_dates:
                    seen_dates.append(date)
                    forecast.append({
                        "date": date,
                        "temp_min": item["main"]["temp_min"],
                        "temp_max": item["main"]["temp_max"],
                        "rain": item.get("rain", {}).get("3h", 0),
                        "humidity": item["main"]["humidity"],
                        "description": item["weather"][0]["description"]
                    })

            st.subheader(f"7-Day Forecast — {district}")
            cols = st.columns(max(1, len(forecast[:5])))
            for i, day in enumerate(forecast[:5]):
                with cols[i]:
                    st.metric(day["date"], f"{day['temp_max']}°C", f"Min {day['temp_min']}°C")
                    st.caption(day["description"])

            alerts = check_risks(forecast, crop)
            st.subheader("Risk Alerts")
            if alerts:
                for alert in alerts:
                    st.warning(alert)
            else:
                st.success("✅ No major risks detected for your crop this week.")

            summary = f"District: {district}, Crop: {crop}, Forecast: {forecast[:3]}"
            advice = ask_gemini(
                f"Give a 2-line farming advisory based on this weather: {summary}",
                "You are an agricultural weather advisor for Indian farmers. Be specific and practical."
            )
            st.info(f"💡 Advisory: {advice}")

        except Exception as e:
            st.error(f"Weather fetch failed: {str(e)}")
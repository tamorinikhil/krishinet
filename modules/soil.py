import streamlit as st
import pandas as pd
from utils.gemini_client import ask_gemini
from utils.tts import speak

def render():
    st.header("🌱 Soil Health Lookup")

    district = st.session_state.get("district", "Lucknow")
    crop = st.session_state.get("crop", "Wheat")
    language = st.session_state.get("language", "Hindi")

    soil_data = pd.read_csv("data/soil_health.csv")

    row = soil_data[soil_data["District"].str.lower() == district.lower()]

    if row.empty:
        st.warning(f"No soil data for {district}. Showing Lucknow data.")
        row = soil_data.iloc[0]
    else:
        row = row.iloc[0]

    st.subheader(f"Soil Profile — {district}")

    def color_level(level):
        if level == "Low":
            return "🔴 Low"
        if level == "Medium":
            return "🟡 Medium"
        if level == "High":
            return "🟢 High"
        return level

    col1, col2 = st.columns(2)
    with col1:
        st.metric("Nitrogen (N)", color_level(row["Nitrogen"]))
        st.metric("Phosphorus (P)", color_level(row["Phosphorus"]))
        st.metric("Potassium (K)", color_level(row["Potassium"]))
    with col2:
        st.metric("pH Level", row["pH"])
        st.metric("Organic Carbon", color_level(row["Organic_Carbon"]))

    if st.button("Get Fertiliser Recommendation"):
        with st.spinner("Generating recommendation..."):
            prompt = f"""
            District: {district}
            Crop: {crop}
            Soil profile: N={row['Nitrogen']}, P={row['Phosphorus']},
            K={row['Potassium']}, pH={row['pH']},
            Organic Carbon={row['Organic_Carbon']}
            Give specific fertiliser recommendation in {language}:
            - Which fertilisers to use (kg per acre)
            - When to apply
            - One organic alternative
            Keep under 120 words.
            """
            rec = ask_gemini(prompt)
            st.success("Recommendation:")
            st.markdown(rec)
            audio = speak(rec, language)
            if audio:
                st.audio(audio, format="audio/mp3")
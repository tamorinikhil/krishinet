import streamlit as st
from modules import disease, chatbot, weather, soil, satellite

st.set_page_config(
    page_title="KrishiNet",
    page_icon="🌾",
    layout="wide"
)

STATES_DISTRICTS = {
    "Uttar Pradesh": ["Lucknow", "Agra", "Varanasi"],
    "Punjab":        ["Amritsar", "Ludhiana", "Patiala"],
    "Tamil Nadu":    ["Chennai", "Coimbatore", "Madurai"],
    "Rajasthan":     ["Jaipur"],
    "Madhya Pradesh":["Bhopal"],
    "Maharashtra":   ["Nagpur", "Pune"],
    "Telangana":     ["Hyderabad"],
    "Karnataka":     ["Bengaluru"],
}

CROPS = ["Wheat", "Rice", "Tomato", "Mustard", "Sugarcane", "Cotton"]
LANGUAGES = ["Hindi", "Punjabi", "Tamil"]

with st.sidebar:
    st.image("https://img.icons8.com/emoji/96/seedling.png", width=60)
    st.title("KrishiNet 🌾")
    st.caption("Federated Agro-Intelligence Platform")
    st.divider()

    state = st.selectbox("State", list(STATES_DISTRICTS.keys()))
    district = st.selectbox("District", STATES_DISTRICTS[state])
    crop = st.selectbox("Crop", CROPS)
    language = st.selectbox("Language", LANGUAGES)

    st.session_state["state"] = state
    st.session_state["district"] = district
    st.session_state["crop"] = crop
    st.session_state["language"] = language

    st.divider()
    page = st.radio("Navigate", [
        "🌿 Disease Detection",
        "🤖 Advisory Chatbot",
        "🌦 Weather Risk",
        "🌱 Soil Health",
        "🛰 Satellite NDVI"
    ])
    st.divider()
    st.caption("Build with AI: Code for Communities\nGoogle Cloud Hackathon 2026")

if page == "🌿 Disease Detection":
    disease.render()
elif page == "🤖 Advisory Chatbot":
    chatbot.render()
elif page == "🌦 Weather Risk":
    weather.render()
elif page == "🌱 Soil Health":
    soil.render()
elif page == "🛰 Satellite NDVI":
    satellite.render()
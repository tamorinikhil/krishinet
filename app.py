import streamlit as st
from modules import disease, chatbot, weather, soil, satellite

st.set_page_config(
    page_title="KrishiNet",
    page_icon="🌾",
    layout="wide"
)

st.markdown("""
<style>
section[data-testid="stSidebar"] {
    background-color: #1B4332 !important;
}
section[data-testid="stSidebar"] * {
    color: white !important;
}
.stButton > button {
    background-color: #2D6A4F !important;
    color: white !important;
    border-radius: 8px !important;
    border: none !important;
    font-weight: bold !important;
}
.stButton > button:hover {
    background-color: #1B4332 !important;
}
</style>
""", unsafe_allow_html=True)

STATES_DISTRICTS = {
    "Uttar Pradesh": ["Lucknow", "Agra", "Varanasi"],
    "Punjab": ["Amritsar", "Ludhiana", "Patiala"],
    "Tamil Nadu": ["Chennai", "Coimbatore", "Madurai"],
    "Rajasthan": ["Jaipur"],
    "Madhya Pradesh": ["Bhopal"],
    "Maharashtra": ["Nagpur", "Pune"],
    "Telangana": ["Hyderabad"],
    "Karnataka": ["Bengaluru"],
}

CROPS = ["Wheat", "Rice", "Tomato", "Mustard", "Sugarcane", "Cotton"]
LANGUAGES = ["Hindi", "Punjabi", "Tamil"]

with st.sidebar:
    st.markdown("## 🌾 KrishiNet")
    st.markdown("*Federated Agro-Intelligence Platform*")
    st.markdown("---")
    st.markdown("### 📍 Location")
    state = st.selectbox("State", list(STATES_DISTRICTS.keys()))
    district = st.selectbox("District", STATES_DISTRICTS[state])
    st.markdown("### 🌱 Crop")
    crop = st.selectbox("Crop", CROPS)
    st.markdown("### 🗣 Language")
    language = st.selectbox("Language", LANGUAGES)
    st.session_state["state"] = state
    st.session_state["district"] = district
    st.session_state["crop"] = crop
    st.session_state["language"] = language
    st.markdown("---")
    page = st.radio("Navigate", [
        "🏠 Home",
        "🌿 Disease Detection",
        "🤖 Advisory Chatbot",
        "🌦 Weather Risk",
        "🌱 Soil Health",
        "🛰 Satellite NDVI"
    ])
    st.markdown("---")
    st.markdown("*Google Cloud Hackathon 2026*")

if page == "🏠 Home":
    st.title("🌾 Welcome to KrishiNet")
    st.subheader("AI-powered agricultural intelligence for every Indian farmer")
    st.divider()

    st.markdown("### What KrishiNet offers you")
    col1, col2, col3 = st.columns(3)

    with col1:
        with st.container(border=True):
            st.markdown("#### 🌿 Disease Detection")
            st.markdown("Upload a crop photo. Gemini Vision diagnoses disease in your language with voice output.")

    with col2:
        with st.container(border=True):
            st.markdown("#### 🤖 Advisory Chatbot")
            st.markdown("Ask farming questions in Hindi, Punjabi, or Tamil and get expert answers instantly.")

    with col3:
        with st.container(border=True):
            st.markdown("#### 🌦 Weather Risk")
            st.markdown("7-day forecast with crop-specific alerts for frost, flood, and heat stress.")

    col4, col5 = st.columns(2)

    with col4:
        with st.container(border=True):
            st.markdown("#### 🌱 Soil Health")
            st.markdown("District NPK and pH data with AI fertiliser recommendations.")

    with col5:
        with st.container(border=True):
            st.markdown("#### 🛰 Satellite NDVI")
            st.markdown("Sentinel-2 vegetation health index — spot crop stress before it's visible.")

    st.divider()
    st.markdown("### Platform Stats")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("States", "8")
    c2.metric("Languages", "3")
    c3.metric("Crops", "6")
    c4.metric("AI Model", "Gemini")
    st.divider()
    st.caption("Data: data.gov.in · IMD · OpenWeather · Sentinel-2 · Google Cloud")
    st.caption("Build with AI: Code for Communities — Google Cloud Hackathon 2026")

elif page == "🌿 Disease Detection":
    disease.render()
elif page == "🤖 Advisory Chatbot":
    chatbot.render()
elif page == "🌦 Weather Risk":
    weather.render()
elif page == "🌱 Soil Health":
    soil.render()
elif page == "🛰 Satellite NDVI":
    satellite.render()
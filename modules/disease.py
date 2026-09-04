import streamlit as st
from utils.gemini_client import ask_gemini_vision
from utils.tts import speak

def render():
    st.header("🌿 Crop Disease Detection")
    st.caption("Upload a photo of your crop — KrishiNet will diagnose the disease.")

    crop = st.session_state.get("crop", "Wheat")
    language = st.session_state.get("language", "Hindi")

    uploaded = st.file_uploader("Upload crop photo", type=["jpg", "jpeg", "png"])

    if uploaded:
        st.image(uploaded, caption="Uploaded Image", use_container_width=True)
        image_bytes = uploaded.read()

        if st.button("Diagnose Disease"):
            with st.spinner("Analyzing with Gemini Vision..."):
                prompt = f"""
                You are an expert agricultural scientist.
                The farmer grows {crop}.
                Analyze this crop image and respond in {language}.
                Provide:
                1. Disease name (bold)
                2. Severity: Low / Medium / High
                3. Cause (1 sentence)
                4. Treatment steps (numbered, max 3)
                5. Prevention tip (1 sentence)
                Keep response under 150 words.
                """
                result = ask_gemini_vision(image_bytes, prompt)

            st.success("Diagnosis Complete")
            st.markdown(result)

            audio = speak(result, language)
            if audio:
                st.audio(audio, format="audio/mp3")
    else:
        st.info("Upload a photo of your crop leaf or plant to begin diagnosis.")
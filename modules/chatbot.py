import streamlit as st
from utils.gemini_client import ask_gemini
from utils.tts import speak

SYSTEM_PROMPT = """
You are a senior Krishi Vigyan Kendra (KVK) extension officer with 20 years 
of experience advising small and marginal farmers across India.
Rules:
- Always reply in the farmer's chosen language
- Maximum 150 words per response
- Use simple words, no jargon
- Always end with one specific actionable step
- Focus on regenerative, low-cost farming practices
- Consider Indian seasons, soil types, and crop varieties
"""

def render():
    st.header("🤖 Agro-Advisory Chatbot")
    st.caption("Ask any farming question in Hindi, Punjabi, or Tamil.")

    language = st.session_state.get("language", "Hindi")
    district = st.session_state.get("district", "")
    crop = st.session_state.get("crop", "Wheat")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if prompt := st.chat_input("Apna sawaal yahan likhein..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Soch raha hoon..."):
                context = f"Farmer is in {district}, growing {crop}. Reply in {language}."
                full_prompt = f"{context}\n\nFarmer's question: {prompt}"
                response = ask_gemini(full_prompt, SYSTEM_PROMPT)
                st.markdown(response)
                audio = speak(response, language)
                if audio:
                    st.audio(audio, format="audio/mp3")

        st.session_state.messages.append({"role": "assistant", "content": response})

    if st.button("Clear Chat"):
        st.session_state.messages = []
        st.rerun()
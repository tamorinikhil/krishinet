from gtts import gTTS
import io

LANG_CODES = {
    "Hindi": "hi",
    "Punjabi": "pa",
    "Tamil": "ta"
}

def speak(text, language="Hindi"):
    try:
        lang_code = LANG_CODES.get(language, "hi")
        tts = gTTS(text=text, lang=lang_code)
        audio_bytes = io.BytesIO()
        tts.write_to_fp(audio_bytes)
        audio_bytes.seek(0)
        return audio_bytes
    except Exception as e:
        return None
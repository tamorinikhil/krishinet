import os
import PIL.Image
import io
from dotenv import load_dotenv
import google.genai as genai
from google.genai import types

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
MODEL = "gemini-3.5-flash-lite"

def ask_gemini(prompt, system_prompt="You are a helpful agricultural assistant for Indian farmers."):
    try:
        response = client.models.generate_content(
            model=MODEL,
            contents=prompt,
            config=types.GenerateContentConfig(
                system_instruction=system_prompt,
                max_output_tokens=500,
            )
        )
        return response.text
    except Exception as e:
        return f"Error: {str(e)}"

def ask_gemini_vision(image_bytes, prompt):
    try:
        image = PIL.Image.open(io.BytesIO(image_bytes))
        response = client.models.generate_content(
            model=MODEL,
            contents=[prompt, image],
        )
        return response.text
    except Exception as e:
        return f"Error: {str(e)}"
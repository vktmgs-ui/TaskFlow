import os

from dotenv import load_dotenv
from google import genai

load_dotenv(override=True)

API_KEY = os.getenv("AI_API_KEY")

client = genai.Client(api_key=API_KEY)


def ask_ai(prompt: str):
    response = client.models.generate_content(
       model="gemini-3.5-flash",
        contents=prompt
    )

    return response.text


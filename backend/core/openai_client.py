import openai
import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY")

settings = Settings()

def ask_openai(prompt: str, model: str = "gpt-4o-mini", max_tokens: int = 250):
    """
    Send a prompt to OpenAI and get a response.
    Compatible with latest SDK (v2.x)
    """
    response = openai.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=max_tokens
    )
    return response.choices[0].message.content.strip()

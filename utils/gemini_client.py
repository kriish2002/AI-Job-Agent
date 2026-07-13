import os

from dotenv import load_dotenv
from google import genai


class GeminiClient:

    def __init__(self):

        load_dotenv()

        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            raise ValueError(
                "GEMINI_API_KEY not found in .env"
            )

        self.client = genai.Client(
            api_key=api_key
        )

        self.model = "gemini-3.1-flash-lite"

    def generate(self, prompt):

        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt
        )

        return response.text
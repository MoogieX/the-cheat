import google.generativeai as genai
from .base_provider import BaseProvider

class GeminiProvider(BaseProvider):
    """
    An AI provider that uses the Google Gemini API.
    """

    def __init__(self, api_key: str):
        if not api_key or api_key == "YOUR_API_KEY":
            raise ValueError("Gemini API key is missing. Please configure it in school_work_helper.py")
        self.api_key = api_key

    def get_ai_assistance(self, prompt: str) -> str:
        """
        Sends a prompt to the Gemini API and returns the response.
        """
        try:
            genai.configure(api_key=self.api_key)
            model = genai.GenerativeModel('gemini-pro')
            response = model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"An error occurred with the Gemini provider: {e}"

import requests
import json
from .base_provider import BaseProvider

class OllamaProvider(BaseProvider):
    """
    An AI provider that uses a local Ollama server.
    """

    def __init__(self, model_name: str = 'llama3', host: str = 'http://localhost:11434'):
        """
        Initializes the Ollama provider.

        Args:
            model_name: The name of the Ollama model to use (e.g., 'llama3').
            host: The URL of the Ollama server.
        """
        self.model_name = model_name
        self.host = host
        self.api_url = f"{self.host}/api/generate"

    def get_ai_assistance(self, prompt: str) -> str:
        """
        Sends a prompt to the local Ollama server and returns the full response.
        """
        try:
            payload = {
                "model": self.model_name,
                "prompt": prompt,
                "stream": False  # We want the full response at once
            }

            response = requests.post(self.api_url, json=payload)
            response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)

            # The response from Ollama (with stream=False) is a single JSON object
            response_data = response.json()
            return response_data.get('response', 'No response field found in Ollama output.')

        except requests.exceptions.ConnectionError:
            return f"Error: Could not connect to the Ollama server at {self.host}. Is Ollama running?"
        except requests.exceptions.RequestException as e:
            return f"An error occurred with the Ollama provider: {e}"

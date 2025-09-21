from abc import ABC, abstractmethod

class BaseProvider(ABC):
    """
    Abstract base class for all AI providers.
    """

    @abstractmethod
    def get_ai_assistance(self, prompt: str) -> str:
        """
        Sends a prompt to the AI and returns the text response.
        """
        pass

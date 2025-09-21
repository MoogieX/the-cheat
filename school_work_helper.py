import importlib

# --- Configuration ---
# Choose your AI provider: 'gemini' is the default.
# We can add more later, like 'ollama' for local models.
AI_PROVIDER = "gemini"

# API Keys for different cloud services
# IMPORTANT: Replace "YOUR_API_KEY" with your actual Gemini API key.
# You can get a key from Google AI Studio: https://aistudio.google.com/app/apikey
API_KEYS = {
    "gemini": "YOUR_API_KEY"
}

# --- Provider Loading ---

def get_provider(provider_name: str):
    """
    Dynamically imports and returns an instance of the chosen AI provider.
    """
    try:
        module = importlib.import_module(f"providers.{provider_name}_provider")
        # Assumes the class name is ProviderNameProvider (e.g., GeminiProvider)
        class_name = f"{provider_name.capitalize()}Provider"
        provider_class = getattr(module, class_name)

        # Pass the API key if the provider needs one
        api_key = API_KEYS.get(provider_name)
        if api_key:
            return provider_class(api_key=api_key)
        else:
            return provider_class()

    except (ImportError, AttributeError) as e:
        print(f"Error: Could not load provider '{provider_name}'. Please check the provider name and files.")
        print(f"Details: {e}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred while loading the provider: {e}")
        return None

# --- Main Application Logic ---

def main():
    """
    Main function to run the school work helper.
    """
    print("--- AI School Work Helper ---")
    print(f"Using AI provider: {AI_PROVIDER}")

    provider = get_provider(AI_PROVIDER)
    if not provider:
        return

    print("Enter your question or prompt below. Type 'exit' to quit.")

    while True:
        user_prompt = input("\n> ")
        if user_prompt.lower() == 'exit':
            break

        ai_response = provider.get_ai_assistance(user_prompt)
        print("\nAI Assistant:")
        print(ai_response)

if __name__ == "__main__":
    main()
import importlib
import configparser

# --- Configuration Loading ---

def load_config():
    """
    Loads settings from config.ini.
    Returns a configparser object or None if the file is not found.
    """
    config = configparser.ConfigParser()
    if not config.read('config.ini'):
        print("Error: config.ini not found. Please create it.")
        return None
    return config

# --- Provider Loading ---

def get_provider(config):
    """
    Dynamically imports and returns an instance of the chosen AI provider.
    """
    try:
        provider_name = config.get('General', 'ai_provider')
    except (configparser.NoSectionError, configparser.NoOptionError) as e:
        print(f"Error: Missing [General] section or 'ai_provider' option in config.ini: {e}")
        return None, None

    try:
        module = importlib.import_module(f"providers.{provider_name}_provider")
        class_name = f"{provider_name.capitalize()}Provider"
        provider_class = getattr(module, class_name)

        # Get the appropriate config section for the provider
        provider_config = {}
        if provider_name == 'gemini':
            # The Gemini provider expects the api_key directly
            provider_config['api_key'] = config.get('API_KEYS', 'gemini', fallback=None)
            # We need to pass a dictionary-like object to the constructor
            provider_instance = provider_class(type('Config', (), {'get': lambda k, d=None: provider_config.get(k, d)}))
        elif provider_name in config:
            provider_instance = provider_class(config[provider_name])
        else:
            # For providers that don't need special config (if any)
            provider_instance = provider_class()

        return provider_instance, provider_name

    except (ImportError, AttributeError) as e:
        print(f"Error: Could not load provider '{provider_name}'. Please check the provider name and files.")
        print(f"Details: {e}")
        return None, None
    except Exception as e:
        print(f"An unexpected error occurred while loading the provider: {e}")
        return None, None

# --- Main Application Logic ---

def main():
    """
    Main function to run the school work helper.
    """
    config = load_config()
    if not config:
        return

    provider, provider_name = get_provider(config)
    if not provider:
        return

    print("--- AI School Work Helper ---")
    print(f"Using AI provider: {provider_name}")
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

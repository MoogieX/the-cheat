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
        if provider_name == 'gemini':
            if 'API_KEYS' in config:
                provider_instance = provider_class(config['API_KEYS'])
            else:
                raise configparser.NoSectionError('API_KEYS')
        elif provider_name == 'ollama':
            if 'Ollama' in config:
                provider_instance = provider_class(config['Ollama'])
            else:
                raise configparser.NoSectionError('Ollama')
        else:
            provider_instance = provider_class()

        return provider_instance, provider_name

    except (ImportError, AttributeError) as e:
        print(f"Error: Could not load provider '{provider_name}'. Please check the provider name and files.")
        print(f"Details: {e}")
        return None, None
    except (configparser.NoSectionError, configparser.NoOptionError) as e:
        print(f"Error: Missing configuration section or option for '{provider_name}' in config.ini: {e}")
        return None, None
    except Exception as e:
        print(f"An unexpected error occurred while loading the provider: {e}")
        return None, None

# --- Helper Functions ---

def get_multiline_input(prompt):
    """
    Prompts the user for multi-line input until they type 'END_TEXT'.
    """
    print(prompt)
    lines = []
    while True:
        line = input()
        if line.strip().upper() == "END_TEXT":
            break
        lines.append(line)
    return "\n".join(lines)

# --- Application Modes ---

def run_qa_mode(provider):
    """
    Runs the interactive Question & Answer mode.
    """
    print("\n--- Q&A Mode ---")
    print("Enter your question or prompt below. Type 'exit' to return to the main menu.")
    while True:
        user_prompt = input("\n> ")
        if user_prompt.lower() == 'exit':
            break
        ai_response = provider.get_ai_assistance(user_prompt)
        print("\nAI Assistant:")
        print(ai_response)

def run_summarizer_mode(provider):
    """
    Runs the text summarization mode.
    """
    print("\n--- Summarizer Mode ---")
    text_to_summarize = get_multiline_input("Paste the text you want to summarize. Type 'END_TEXT' on a new line to finish.")
    
    if not text_to_summarize.strip():
        print("No text provided.")
        return

    print("\nSummarizing... Please wait.")
    prompt = f"Please provide a concise summary of the following text:\n\n---\n{text_to_summarize}\n---"
    
    ai_response = provider.get_ai_assistance(prompt)
    print("\n--- Summary ---")
    print(ai_response)

def run_paraphraser_mode(provider):
    """
    Runs the text paraphraser mode with an optional style example.
    """
    print("\n--- Paraphraser Mode ---")
    text_to_paraphrase = get_multiline_input("Paste the text you want to paraphrase. Type 'END_TEXT' on a new line to finish.")

    if not text_to_paraphrase.strip():
        print("No text provided.")
        return

    style_choice = input("Do you want to provide a style example? (y/n): ").lower()
    
    prompt = ""
    if style_choice == 'y':
        style_example = get_multiline_input("Paste your style example. Type 'END_TEXT' on a new line to finish.")
        if not style_example.strip():
            print("No style example provided. Proceeding with a simple paraphrase.")
            prompt = f"Please paraphrase the following text:\n\n---\n{text_to_paraphrase}\n---"
        else:
            prompt = f"Paraphrase the following text. Your response should mimic the writing style of the provided style example.\n\n--- STYLE EXAMPLE ---\n{style_example}\n\n--- TEXT TO PARAPHRASE ---\n{text_to_paraphrase}\n---"
    else:
        prompt = f"Please paraphrase the following text:\n\n---\n{text_to_paraphrase}\n---"

    print("\nParaphrasing... Please wait.")
    ai_response = provider.get_ai_assistance(prompt)
    print("\n--- Paraphrased Text ---")
    print(ai_response)

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

    while True:
        print("\n--- Main Menu ---")
        print("1. Q&A Mode")
        print("2. Summarizer Mode")
        print("3. Paraphraser Mode")
        print("4. Exit")
        
        choice = input("Choose a mode: ")

        if choice == '1':
            run_qa_mode(provider)
        elif choice == '2':
            run_summarizer_mode(provider)
        elif choice == '3':
            run_paraphraser_mode(provider)
        elif choice == '4':
            print("Exiting. Goodbye!")
            break
        else:
            print("Invalid choice, please try again.")

if __name__ == "__main__":
    main()

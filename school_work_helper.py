import importlib
import configparser
import traceback
from sympy import sympify, solve, symbols, Eq, pretty, diff, integrate, simplify

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
    # ... (omitted for brevity, no changes)

def run_summarizer_mode(provider):
    # ... (omitted for brevity, no changes)

def run_paraphraser_mode(provider):
    # ... (omitted for brevity, no changes)

def run_math_mode():
    """
    Runs the symbolic math solver mode using SymPy.
    """
    print("\n--- Math Mode ---")
    print("Enter a mathematical expression to solve. Type 'exit' to return to the main menu.")
    print("Available symbols: x, y, z")
    print("Available functions: solve, Eq, pretty, diff, integrate, simplify")
    print("\n--- Examples ---")
    print("Solve an equation: solve(Eq(x**2, 4), x)")
    print("Differentiate:      diff(x**3, x)")
    print("Integrate:          integrate(2*x, x)")
    print("Simplify:           simplify((x**2 - 1)/(x - 1))")

    # Define a safe namespace for evaluation
    x, y, z = symbols('x y z')
    safe_namespace = {
        'x': x, 'y': y, 'z': z,
        'solve': solve,
        'Eq': Eq,
        'pretty': pretty,
        'diff': diff,
        'integrate': integrate,
        'simplify': simplify
    }

    while True:
        user_input = input("\nMath> ")
        if user_input.lower() == 'exit':
            break
        
        try:
            # Use sympify to safely parse the string
            expr = sympify(user_input, locals=safe_namespace)
            result = expr
            
            # Use pretty printing for better output
            print("Result:")
            print(pretty(result))

        except Exception as e:
            print("\nAn error occurred. Please check your expression.")
            print(f"Details: {e}")
            # traceback.print_exc() # Uncomment for detailed debugging

# --- Main Application Logic ---

def main():
    # ... (omitted for brevity, no changes)

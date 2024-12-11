from deep_translator import GoogleTranslator
from languages import LANGUAGES
import Levenshtein

def translate_text(lang_code, text) -> str:
    """
    Translates the given text into the specified language using deep-translator.

    Parameters:
    lang_code: The target language code (e.g., 'es' for Spanish, 'fr' for French).
    text: The sentence or text to translate.

    Returns:
    A string with the translation or an error message if the language code is invalid.
    """
    
    # Check if the provided language code is valid
    if lang_code not in LANGUAGES:
        return "Invalid language code! Please use a valid one."

    try:
        # Translate the text using deep-translator
        translated_text = GoogleTranslator(source='auto', target=lang_code).translate(text)
        return f"Translated to {LANGUAGES[lang_code]}: {translated_text}"
    except Exception as e:
        return f"An error occurred during translation: {str(e)}"

def search_language_code(language_name: str) -> str:
    """
    Searches for the language code corresponding to the given language name,
    with support for close or similar input using Levenshtein distance.

    Parameters:
    language_name (str): The name of the language to search for.

    Returns:
    str: The language code if found, otherwise a message indicating the language was not found.
    """
    # Normalize the input to lowercase for case-insensitive comparison
    language_name = language_name.lower()

    # Create a reverse dictionary from LANGUAGES
    reverse_languages = {name.lower(): code for code, name in LANGUAGES.items()}

    # List of available languages
    available_languages = list(reverse_languages.keys())

    # Initialize the minimum distance and closest match
    min_distance = float('inf')
    closest_match = None

    # Find the closest match using Levenshtein distance
    for lang in available_languages:
        distance = Levenshtein.distance(language_name, lang)
        if distance < min_distance:
            min_distance = distance
            closest_match = lang

    # Define a threshold for considering a match
    threshold = 5  # This value can be adjusted based on requirements

    if min_distance <= threshold:
        lang_code = reverse_languages[closest_match]
        return lang_code
    else:
        return "Language not found. Please make sure the language name is correct."
    
def list_all_languages(page: int = 0, items_per_page: int = 10) -> str:
    """
    Returns a specific page of the formatted string containing available languages and their codes.
    
    Parameters:
    page (int): The page number to return.
    items_per_page (int): Number of languages to display per page.

    Returns:
    tuple: The string listing languages for the page and the total number of pages.
    """
    languages_list = [f"{name.title()} (`{code}`)" for code, name in LANGUAGES.items()]
    total_pages = len(languages_list) // items_per_page + (1 if len(languages_list) % items_per_page > 0 else 0)
    
    start = page * items_per_page
    end = start + items_per_page
    page_content = "\n".join(languages_list[start:end])
    
    return page_content, total_pages

def load_help_info(file_path):
    """Load help information from a Markdown file."""
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()
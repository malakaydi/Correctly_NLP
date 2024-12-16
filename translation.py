from transformers import pipeline

# Initialize translation models
try:
    translator_ar_to_en = pipeline("translation", model="Helsinki-NLP/opus-mt-ar-en")
    translator_en_to_ar = pipeline("translation", model="Helsinki-NLP/opus-mt-en-ar")
except Exception as e:
    print(f"Error initializing translation models: {str(e)}")

def translate_ar_to_en(text):
    """
    Translates Arabic text to English.
    Args:
        text (str): The Arabic text to translate.
    Returns:
        str: The translated English text.
    """
    if not text.strip():
        return "No text provided."
    try:
        translation = translator_ar_to_en(text)
        return translation[0]['translation_text']
    except Exception as e:
        return f"Error in translation: {str(e)}"

def translate_en_to_ar(text):
    """
    Translates English text to Arabic.
    Args:
        text (str): The English text to translate.
    Returns:
        str: The translated Arabic text.
    """
    if not text.strip():
        return "No text provided."
    try:
        translation = translator_en_to_ar(text)
        return translation[0]['translation_text']
    except Exception as e:
        return f"Error in translation: {str(e)}"

def process_translation(text, target_language):
    """
    Processes text for translation based on target language.
    Args:
        text (str): The text to translate.
        target_language (str): The target language, either 'english' or 'arabic'.
    Returns:
        str: The translated text.
    """
    if target_language == 'english':
        return translate_ar_to_en(text)
    elif target_language == 'arabic':
        return translate_en_to_ar(text)
    else:
        return "Unsupported target language."

def load_translation_models():
    try:
        # Test Arabic-to-English translation
        translator_ar_to_en = pipeline("translation", model="Helsinki-NLP/opus-mt-ar-en")
        print("Arabic-to-English model loaded successfully!")

        # Test English-to-Arabic translation
        translator_en_to_ar = pipeline("translation", model="Helsinki-NLP/opus-mt-en-ar")
        print("English-to-Arabic model loaded successfully!")
    except Exception as e:
        print(f"Error loading models: {e}")

if __name__ == '__main__':
    load_translation_models()
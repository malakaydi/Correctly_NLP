import re
from language_tool_python import LanguageTool #grammar
from rapidfuzz import fuzz 
import pandas as pd
from spellchecker import SpellChecker #spelling


tool_en = LanguageTool('en-US')
spell = SpellChecker()


dataset = pd.read_csv("Grammar Correction.csv")
dataset = dataset[["Ungrammatical Statement", "Standard English"]]

def preprocess_word(word):
    word = re.sub(r'[^a-zA-Z\']', '', word).lower()
    return word

def find_closest_match(input_text, dataset, threshold=70):
    best_match = None
    best_score = 0
    for _, row in dataset.iterrows():
        score = fuzz.ratio(input_text, row["Ungrammatical Statement"])
        if score > best_score and score >= threshold:
            best_score = score
            best_match = row["Standard English"]
    return best_match

def correct_spelling(text, dataset):
    
    words = re.findall(r'\b[\w\']+\b|[^\w\s]', text)
    corrected_words = []
    for word in words:
        if re.match(r'[^\w\s]', word):
            
            corrected_words.append(word)
        else:
            processed_word = preprocess_word(word)
            corrected_word = spell.correction(processed_word)
            if corrected_word == processed_word:
                corrected_word = find_closest_match(processed_word, dataset)
            corrected_words.append(corrected_word if corrected_word else word)
    return " ".join(corrected_words)

def correct_grammar(text):
    corrected = tool_en.correct(text)
    return corrected

def process_english_text(text):
    text_with_correct_spelling = correct_spelling(text, dataset)
    return correct_grammar(text_with_correct_spelling)





import os
import re
import pandas as pd
from collections import Counter
from nltk.tokenize import word_tokenize
from textdistance import DamerauLevenshtein
import nltk


# Download NLTK data
nltk.download('punkt')

def preprocess(text):
    """
    Preprocess the text by removing punctuation and converting to lowercase.
    """
    text = re.sub(r'[^\w\s]', '', text)  # Remove punctuation
    return text

DATASET_DIR = "Culture"

def read_and_preprocess_files(dir_path=DATASET_DIR):
    """
    Read all text files in a directory, preprocess the text, and return the cleaned text.
    """
    all_text = ''
    for filename in os.listdir(dir_path):
        if filename.endswith('.txt'):  # Only process text files
            file_path = os.path.join(dir_path, filename)
            with open(file_path, 'r', encoding='utf-8') as f:
                text = f.read()
                all_text += text
    cleaned_text = preprocess(all_text)
    return cleaned_text

def create_dictionary(dataframe):
    """
    Create a dictionary of word frequencies from the dataset.
    """
    words = []
    for index, row in dataframe.iterrows():
        words.extend(word_tokenize(row['text']))
    word_counts = Counter(words)
    return word_counts

def dl_distance(word1, word2):
    """
    Calculate Damerau-Levenshtein distance between two words.
    """
    dl = DamerauLevenshtein()
    return dl.distance(word1, word2)

def find_closest_word(misspelled_word, dictionary, max_distance=2):
    """
    Find the closest word to the given misspelled word based on Damerau-Levenshtein distance.
    """
    closest_word = None
    min_distance = float('inf')
    max_frequency = 0
    
    for word, count in dictionary.items():
        distance = dl_distance(misspelled_word, word)
        if distance <= max_distance:
            # Find the closest word with the highest frequency
            if distance < min_distance or (distance == min_distance and count > max_frequency):
                closest_word = word
                min_distance = distance
                max_frequency = count
    return closest_word

def correct_text(input_text, word_dict):
    """
    Automatically correct all potentially misspelled words in the input text.
    """
    corrected_text = []
    for word in word_tokenize(input_text):
        corrected_word = find_closest_word(word, word_dict)
        if corrected_word:
            corrected_text.append(corrected_word)  # Use the corrected word
        else:
            corrected_text.append(word)  # If no correction, keep the original word
    return ' '.join(corrected_text)

def process_arabic_text(text):
    """
    Process and correct Arabic text by using a word dictionary and Damerau-Levenshtein distance.
    """
    # Step 1: Read and preprocess the dataset
    dataset_text = read_and_preprocess_files(DATASET_DIR)
    
    # Step 2: Convert preprocessed text into a DataFrame
    dataset = pd.DataFrame({'text': [dataset_text]})
    
    # Step 3: Create a word frequency dictionary from the dataset
    word_dict = create_dictionary(dataset)
    
    # Step 4: Correct the Arabic text
    corrected_text = correct_text(text, word_dict)
    
    return corrected_text


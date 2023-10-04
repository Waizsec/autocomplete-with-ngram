import random
import pandas as pd
import nltk
from nltk.tokenize import word_tokenize
from collections import defaultdict
nltk.data.path.append("punkt/PY3/english.pickle")

file_path = "static/cleaned_text.txt"
text = ""
try:
    with open(file_path, "r") as file:
        text = file.read()
        print("File contents imported successfully.")
except FileNotFoundError:
    print("File not found. Please check the file path.")

tokens = word_tokenize(text)
tokens = [token for token in tokens if token not in ["'", '[', ']', '``']]

# Markov Model
def build_markov_model(tokens, order=1):
    model = {}
    for i in range(len(tokens) - order):
        history = tuple(tokens[i:i + order])
        next_word = tokens[i + order]
        
        if history in model:
            model[history].append(next_word)
        else:
            model[history] = [next_word]
    
    return model

# Membuat autocomplete suggestion
def autocomplete(input_text, model, max_suggestions=5):
    input_words = input_text.split()
    
    # Menentukan urutan yang benar berdasarkan number input kata
    order = 1 if len(input_words) == 1 else 2  # Gunakan 1 order (context) dan 2 jika lebih dari satu kata
    
    input_history = tuple(input_words[-order:])
    
    if input_history not in model:
        return []

    suggestions = model[input_history]
    
    # random suggestion 
    random.shuffle(suggestions)
    
    # Menghindari ada kata duplicate pada suggestion
    suggestions = list(dict.fromkeys(suggestions))
    
    # maximal 5
    suggestions = suggestions[:max_suggestions]
    
    return suggestions

model = build_markov_model(tokens, order=2) 

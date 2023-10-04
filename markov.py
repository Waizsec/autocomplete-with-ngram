import pandas as pd
import nltk
from nltk.tokenize import word_tokenize
from preprop import tokens
import random

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
    input_words = word_tokenize(input_text.lower())
    
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

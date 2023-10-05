import pandas as pd
import nltk
from nltk.tokenize import word_tokenize
from preprop import tokens
import random

# Markov Model
def build_markov_model_one_word(tokens, order):
    model = {}
    for i in range(len(tokens) - order):
        history = tuple(tokens[i:i + order])
        next_word = tokens[i + order]
        
        if history in model:
            model[history].append(next_word)
        else:
            model[history] = [next_word]
    
    return model

def build_markov_model_two_word(tokens, order):
    model = {}
    for i in range(len(tokens) - order):
        history = tuple(tokens[i:i + order])
        next_word = tokens[i + order]
        
        if history in model:
            model[history].append(next_word)
        else:
            model[history] = [next_word]
    
    return model

def autocomplete(input_text, model, max_suggestions):
    input_words = word_tokenize(input_text.lower())
    suggestions = set() 
    order = 1 if len(input_words) == 1 else 2  
    input_history = tuple(input_words[-order:])
    
    while len(suggestions) < max_suggestions:
        if input_history in model:
            next_word = random.choice(model[input_history])
            suggestions.add(next_word) 
        else:
            break
    
    return list(suggestions) 


one_word_model = build_markov_model_one_word(tokens, 1)
two_word_model = build_markov_model_two_word(tokens, 2)
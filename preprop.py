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

tokens = word_tokenize(text.lower())
tokens = [token for token in tokens if token not in ["'", '[', ']', '``']]
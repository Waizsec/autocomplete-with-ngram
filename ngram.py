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
vocab = set(tokens)
vocab_list = list(vocab)

bigram_text = []
trigram_text = []

for i in range(len(tokens)-2):
  bigram = []
  bigram.append(tokens[i])
  bigram.append(tokens[i+1])
  bigram_text.append(bigram)

for i in range(len(tokens)-3):
  trigram = []
  trigram.append(tokens[i])
  trigram.append(tokens[i+1])
  trigram.append(tokens[i+2])
  trigram_text.append(trigram)


unigram_counts = defaultdict(int)
for token in tokens:
    unigram_counts[token] += 1

def count_ngrams(tokens):
    bigram_counts = defaultdict(int)
    trigram_counts = defaultdict(int)

    for i in range(len(tokens) - 1):
        bigram = (tokens[i], tokens[i+1])
        bigram_counts[bigram] += 1

    for i in range(len(tokens) - 2):
        trigram = (tokens[i], tokens[i+1], tokens[i+2])
        trigram_counts[trigram] += 1

    return bigram_counts, trigram_counts

bigram_counts, trigram_counts = count_ngrams(tokens)

def suggest_next_word(input, bigram_counts, trigram_counts, unigram_counts, vocab):
    tokenized_input = word_tokenize(input.lower())
    last_bigram = tuple(tokenized_input[-2:])
    vocab_probabilities = {}

    if input is None or not input.strip():
        return []
    elif len(tokenized_input) == 1:
        if last_bigram:
            last_unigram = last_bigram[0]
            unigram_count = unigram_counts.get(last_unigram, 1)
            for vocab_word in vocab:
                test_bigram = (last_unigram, vocab_word)
                if unigram_count > 0:
                    probability = bigram_counts.get(test_bigram, 0) / unigram_count
                    vocab_probabilities[vocab_word] = probability
    else:
        for vocab_word in vocab:
            test_trigram = (last_bigram[0], last_bigram[1], vocab_word)
            test_bigram = last_bigram
            if bigram_counts[test_bigram] > 0 :
                probability = trigram_counts.get(test_trigram, 0) / bigram_counts[test_bigram]
                vocab_probabilities[vocab_word] = probability

    top_suggestions = sorted(vocab_probabilities.items(), key=lambda x: x[1], reverse=True)[:3]
    return top_suggestions
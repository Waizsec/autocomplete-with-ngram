import pandas as pd
import nltk
from nltk.tokenize import word_tokenize
from collections import defaultdict, Counter
from preprop import tokens
import string

# Preprocess tokens
vocab = set(tokens)
bigram_text = [(tokens[i], tokens[i+1]) for i in range(len(tokens) - 1)]
trigram_text = [(tokens[i], tokens[i+1], tokens[i+2]) for i in range(len(tokens) - 2)]

# Count unigrams, bigrams, and trigrams
unigram_counts = Counter(tokens)

def count_ngrams(tokens):
    bigram_counts = Counter([(tokens[i], tokens[i+1]) for i in range(len(tokens) - 1)])
    trigram_counts = Counter([(tokens[i], tokens[i+1], tokens[i+2]) for i in range(len(tokens) - 2)])
    return bigram_counts, trigram_counts

bigram_counts, trigram_counts = count_ngrams(tokens)

def suggest_next_word(input, bigram_counts, trigram_counts, unigram_counts, vocab):
    tokenized_input = word_tokenize(input.lower())
    last_bigram = tuple(tokenized_input[-2:])
    vocab_probabilities = {}

    if not input.strip():
        unigram_counter = Counter(unigram_counts)
        punctuation_chars = set(string.punctuation)
        top_3_most_frequent = [(word, frequency) for word, frequency in unigram_counter.most_common() if word not in punctuation_chars][:3]
        return top_3_most_frequent 

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

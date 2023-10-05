from flask import Flask, render_template, request, jsonify
from ngram import suggest_next_word, bigram_counts, trigram_counts, unigram_counts, vocab
from markov import autocomplete, two_word_model, one_word_model


app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/ngram")
def ngram():
    return render_template('ngram.html')

@app.route("/markov")
def markov():
    return render_template('markov.html')


@app.route('/get_suggestions', methods=['POST'])
def get_suggestions():
    input_text = request.form['input_text']
    suggestions = suggest_next_word(input_text, bigram_counts, trigram_counts, unigram_counts, vocab)
    return jsonify({'suggestions': [suggestion[0] for suggestion in suggestions]})

@app.route('/get_suggestions_markov', methods=['POST'])
def get_suggestions_markov():
    input_text = request.form['input_text']
    input_text = request.form['input_text']
    words = input_text.split()

    if len(words) == 1 :
        suggestions = autocomplete(input_text, one_word_model, max_suggestions=3)
    else:
         suggestions = autocomplete(input_text, two_word_model, max_suggestions=3)
         
    return jsonify({'suggestions': [suggestions]})

if __name__ == "__main__" :
    app.run(debug=True)
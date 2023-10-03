from flask import Flask, render_template, request, jsonify
from ngram import suggest_next_word, bigram_counts, trigram_counts, unigram_counts, vocab


app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')

@app.route('/get_suggestions', methods=['POST'])
def get_suggestions():
    input_text = request.form['input_text']
    
    suggestions = suggest_next_word(input_text, bigram_counts, trigram_counts, unigram_counts, vocab)

    return jsonify({'suggestions': [suggestion[0] for suggestion in suggestions]})


if __name__ == "__main__" :
    app.run(debug=True)
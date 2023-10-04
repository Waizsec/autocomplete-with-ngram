function updateSuggestions() {
    const inputText = document.getElementById('input_text').value;

    fetch('/get_suggestions_markov', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: `input_text=${encodeURIComponent(inputText)}`,
    })
        .then(response => response.json())
        .then(data => {
            const suggestionsSpan = document.getElementById('suggestions');
            suggestionsSpan.innerHTML = '';

            data.suggestions.forEach(suggestion => {
                for (let i = 0; i < suggestion.length; i++) {
                    const suggestionSpan = document.createElement('span');
                    suggestionSpan.className = 'text-custome suggestion ml-4 cursor-pointer';
                    suggestionSpan.textContent = suggestion[i];

                    suggestionSpan.addEventListener('click', () => {
                        const inputElement = document.getElementById('input_text');
                        const suggestionToAdd = suggestion[i];
                        const noSpaceWords = ["'s", "'t"];

                        if (suggestionToAdd.match(/^[.,!?';]/) || noSpaceWords.includes(suggestionToAdd)) {
                            inputElement.value += suggestionToAdd;
                        } else {
                            inputElement.value += ` ${suggestionToAdd}`;
                        }
                        updateSuggestions();
                    });

                    suggestionsSpan.appendChild(suggestionSpan);
                }
            });
        })
        .catch(error => {
            console.error('Error fetching suggestions:', error);
        });
}

const inputElement = document.getElementById('input_text');
inputElement.addEventListener('input', updateSuggestions);

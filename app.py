from flask import Flask, request, jsonify
from flask_cors import CORS
import subprocess
import boto3
import json 
import nltk
from nltk.corpus import stopwords

# nltk.download('stopwords')
# nltk.download('punkt')
# nltk.download('punkt_tab')

# Load the data from the events JSON file
with open(r'C:\Users\nickp\Documents\HTSL_2024\my-app\public\example_events.json', 'r') as file:
    events_data = json.load(file)


def search_events(query):
    results = []
    query = query.lower()  # Make the query case-insensitive
    
    for event in events_data:
        # Check if the query matches title or description
        if query in event['title'].lower() or query in event['description'].lower():
            results.append(event)
    
    return results

def search(search_term):
    comprehend = boto3.client('comprehend', region_name='us-west-2')
    response = comprehend.detect_key_phrases(Text=search_term, LanguageCode='en')

    key_phrases = [phrase['Text'] for phrase in response['KeyPhrases']]

    tokens = nltk.word_tokenize(search_term)
    stop_words = set(stopwords.words('english'))
    keywords = [word for word in tokens if word.lower() not in stop_words]
    keywords.extend(key_phrases)

    # Search for events that match the query
    matching_events = []
    for phrase in key_phrases:
        matching_events.extend(search_events(phrase))

    matching_events = list({event['title']: event for event in matching_events}.values())

    if matching_events:
        # Convert matching events to JSON-compatible format
        return json.dumps({
            "events": matching_events
        })
    else:
        # Return no events found
        return json.dumps({
            "events" : "No events found matching your query"
        })

app = Flask(__name__)
CORS(app)  # Enable CORS

@app.route('/search', methods=['POST'])
def search_route():
    data = request.json
    search_term = data.get('searchTerm')

    # Log the received search term
    app.logger.debug(f"Received search term: {search_term}")

    # Run your Python script with the search term
    result = search(search_term)
    output = result.stdout
    app.logger.debug(f"Script output: {output}")

    # Process the output and return the results
    # Assuming your script returns JSON formatted results
    return jsonify(output)

if __name__ == '__main__':
    app.run(port=5000,debug=True)

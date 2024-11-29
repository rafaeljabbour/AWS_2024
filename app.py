from flask import Flask, request, jsonify
from flask_cors import CORS
import subprocess

app = Flask(__name__)
CORS(app)  # Enable CORS

@app.route('/search', methods=['POST'])
def search():
    data = request.json
    search_term = data.get('searchTerm')

    # Run your Python script with the search term
    result = subprocess.run(['python', 'read_user_input.py', search_term], capture_output=True, text=True)
    output = result.stdout

    # Process the output and return the results
    # Assuming your script returns JSON formatted results
    return jsonify(output)

if __name__ == '__main__':
    app.run(debug=True)
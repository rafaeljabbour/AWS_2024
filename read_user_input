import boto3
import json
import nltk
from nltk.corpus import stopwords

# Load the data from the events JSON file
with open(r'C:\Users\mijan\Desktop\Folder of folders\AWS2024\HTSL_2024\example_events.json', 'r') as file:
    events_data = json.load(file)

# nltk.download('stopwords')
# nltk.download('punkt')
# nltk.download('punkt_tab')

# Function to search through events based on user input
def search_events(query):
    results = []
    query = query.lower()  # Make the query case-insensitive
    
    for event in events_data:
        # Check if the query matches title or description
        if query in event['title'].lower() or query in event['description'].lower():
            results.append(event)
    
    return results

#########

comprehend = boto3.client('comprehend', region_name='us-west-2')
text = input("Enter search term: ")
response = comprehend.detect_key_phrases(Text=text, LanguageCode='en')

key_phrases = [phrase['Text'] for phrase in response['KeyPhrases']]

tokens = nltk.word_tokenize(text)
stop_words = set(stopwords.words('english'))
keywords = [word for word in tokens if word.lower() not in stop_words]
keywords.extend(key_phrases)

print("Extracted keywords: ", keywords)
print("Key Phrases:", key_phrases)

#########

# Search for events that match the query
matching_events = []
for phrase in key_phrases:
    matching_events.extend(search_events(phrase))

matching_events = list({event['title']: event for event in matching_events}.values())

if matching_events:
    print(f"Found {len(matching_events)} event(s):")
    for event in matching_events:
        print(f"Title: {event['title']}")
        print(f"Description: {event['description']}")
        print(f"Date: {event['date']}")
        print(f"Location: {event['location']}\n")
else:
    print("No events found matching your query.")


###################################################################



###################################################################

# from opensearchpy import OpenSearch

# client = OpenSearch(
#     hosts=[{'host': 'https://frontend.dijbfopvikcw0.amplifyapp.com/', 'port': 443}],
#     http_auth=('username', 'password'),  # Use credentials if needed
#     use_ssl=True,
#     verify_certs=True,
#     ssl_assert_hostname=False,
#     ssl_show_warn=False
# )

# response = client.search(
#     index="events",
#     body={
#         "query": {
#             "match_all": {}
#         }
#     }
# )
# print("Search Results:", response)

# from opensearchpy import OpenSearch

# # Replace this with your OpenSearch endpoint
# host = "https://frontend.dijbfopvikcw0.amplifyapp.com/"

# # Initialize OpenSearch client
# client = OpenSearch(
#     hosts=[host],
#     http_auth=('your-username', 'your-password'),  # For basic auth; adjust if not needed
#     use_ssl=True,
#     verify_certs=True
# )

# # Test connection
# try:
#     response = client.info()
#     print("Connection successful!")
#     print("Cluster Info:", response)
# except Exception as e:
#     print("Connection failed!")
#     print("Error:", e)

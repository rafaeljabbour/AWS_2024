# lambda_function.py

import json
import boto3
import urllib.request
from bs4 import BeautifulSoup
from datetime import datetime
import uuid

# Initialize DynamoDB resource
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Events')  # Ensure 'Events' is your DynamoDB table name

def convert_date_to_ymd(date_str):
    try:
        date_formats = [
            "%b %d, %Y",           # Example: "Nov 29, 2024"
            "%b %d, %Y %I:%M %p",  # Example: "Nov 29, 2024 12:00 PM"
            "%A, %B %d, %Y",       # Example: "Friday, November 29, 2024"
            "%Y-%m-%d",            # Example: "2024-11-29"
        ]
        for date_format in date_formats:
            try:
                parsed_date = datetime.strptime(date_str, date_format)
                return parsed_date.strftime("%Y-%m-%d")  # Return in YYYY-MM-DD format
            except ValueError:
                pass  # Try the next format
        return date_str
    except Exception as e:
        print(f"Error in date conversion: {e}")
        return date_str

def lambda_handler(event, context):
    try:
        # Open the main page and parse it with BeautifulSoup
        page = urllib.request.urlopen('https://www.utoronto.ca/events').read()
        soup = BeautifulSoup(page, "html.parser")

        # Find all tables on the page
        tables = soup.find_all('table')

        # Iterate through each table to look for a <th> tag that starts with "Events"
        for table in tables:
            # Check for a <th> that contains "Events" at the start of its text
            th_elements = table.find_all('th')
            for th in th_elements:
                if th.get_text(strip=True).startswith("Events"):
                    # Found a table with an "Events" heading, now grab all rows in this table
                    print(f"\nFound an 'Events' section in this table.")

                    # Iterate through all rows in the table (skip the header row)
                    rows = table.find_all('tr')[1:]  # Skipping the first row which is usually the header

                    for row in rows:
                        # Find the columns (td elements) in this row
                        columns = row.find_all('td')

                        # Ensure the row has the correct number of columns (at least 2 for event and date)
                        if len(columns) >= 2:
                            # Extract the event name (link text) and associated link
                            event_column = columns[0]  # "Events" column
                            date_column = columns[1]   # "Date" column

                            # Extract event name and link from the "Events" column
                            event_link = event_column.find('a', href=True)
                            if event_link:
                                event_name = event_link.get_text(strip=True)  # Event name from the link
                                event_url = event_link['href']  # URL of the event

                                # Ensure the link is absolute
                                if not event_url.startswith('http'):
                                    event_url = 'https://www.utoronto.ca' + event_url

                                # Extract and convert the event date from the "Date" column
                                event_date_raw = date_column.get_text(strip=True)  # Date text
                                event_date = convert_date_to_ymd(event_date_raw)  # Convert date to YYYY-MM-DD

                                # Fetch the event page and extract its text content
                                try:
                                    event_page = urllib.request.urlopen(event_url).read()
                                    event_soup = BeautifulSoup(event_page, "html.parser")

                                    # Get all the text from the event page
                                    event_text = event_soup.get_text(separator=' ', strip=True)

                                    # Generate a unique EventID
                                    event_id = str(uuid.uuid4())

                                    # Extract keywords (customize this as needed)
                                    keywords_set = set(event_name.lower().split()) | set(event_text.lower().split())
                                    keywords_list = list(keywords_set)

                                    # Prepare the item for DynamoDB
                                    event_item = {
                                        'EventID': event_id,
                                        'EventName': event_name,
                                        'Date': event_date,
                                        'Description': event_text,
                                        'Keywords': keywords_list,
                                        'EventURL': event_url
                                    }

                                    # Insert the item into DynamoDB
                                    table.put_item(Item=event_item)

                                    # Print success message
                                    print(f"Stored event: {event_name} | Date: {event_date}")

                                except Exception as e:
                                    print(f"Error fetching the event page: {e}")
                            else:
                                print("No event link found.")
                        else:
                            print("Row does not have enough columns.")

        return {
            'statusCode': 200,
            'body': json.dumps('Events scraped and stored successfully.')
        }

    except Exception as e:
        print(f"Error in lambda_handler: {e}")
        return {
            'statusCode': 500,
            'body': json.dumps('An error occurred during scraping.')
        }

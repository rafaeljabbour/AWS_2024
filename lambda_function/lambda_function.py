import boto3
from datetime import datetime
from bs4 import BeautifulSoup
import urllib.request
import json


# DynamoDB Client
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('EventsTable')  # Replace with your DynamoDB table name


# Function to convert dates to YYYY-MM-DD format
def convert_date_to_ymd(date_str):
    try:
        # Check for a date range (i.e., "Month Day, Year to Month Day, Year")
        if "to" in date_str:
            # Split the range into start and end date
            start_date_str, end_date_str = date_str.split(" to ")
            start_date = parse_single_date(start_date_str.strip())
            end_date = parse_single_date(end_date_str.strip())
            return start_date, end_date
        
        # If it's a single date, parse it
        else:
            return parse_single_date(date_str.strip())


    except Exception as e:
        print(f"Error in date conversion: {e}")
        return date_str


# Helper function to parse a single date into YYYY-MM-DD
def parse_single_date(date_str):
    # List of potential date formats
    date_formats = [
        "%B %d, %Y",   # Example: "November 29, 2024"
        "%b %d, %Y",   # Example: "Nov 29, 2024"
        "%A, %B %d, %Y",  # Example: "Friday, November 29, 2024"
    ]
    
    # Try parsing the date using each format
    for date_format in date_formats:
        try:
            parsed_date = datetime.strptime(date_str, date_format)
            return parsed_date.strftime("%Y-%m-%d")  # Return date in YYYY-MM-DD format
        except ValueError:
            pass  # Try the next format if this one doesn't work


    # If no format matched, return the original string
    return date_str


# Lambda function handler
def lambda_handler(event, context):
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
                rows = table.find_all('tr')[1:]  # Skipping the first row which is usually the header


                for row in rows:
                    # Find the columns (td elements) in this row
                    columns = row.find_all('td')


                    # Ensure the row has the correct number of columns (at least 2 for event and date)
                    if len(columns) >= 2:
                        # Extract the event name (link text) and associated link
                        event_column = columns[0]  # This is usually the "Events" column
                        date_column = columns[1]   # This is usually the "Date" column
                        
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
                        
                        # Fetch the event page and extract its text content using urllib
                        try:
                            event_page = urllib.request.urlopen(event_url).read()
                            event_soup = BeautifulSoup(event_page, "html.parser")
                            
                            # Get all the text from the event page
                            event_text = event_soup.get_text(strip=True)
                            
                            # Store event details in DynamoDB
                            event_id = str(hash(event_url))  # Generate a unique event ID (hash of the URL)
                            table.put_item(
                                Item={
                                    'event_id': event_id,
                                    'event_url': event_url,
                                    'event_name': event_name,
                                    'event_date': event_date,
                                    'event_description': event_text[:500],  # Save a portion of the description (first 500 chars)
                                }
                            )
                            print(f"Stored event: {event_name} ({event_date})")
                            
                        except Exception as e:
                            print(f"Error fetching the event page: {e}")


    return {
        'statusCode': 200,
        'body': json.dumps('Events processing completed successfully')
    }






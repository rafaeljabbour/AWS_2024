# Why Wasn't I Invited

## Introduction

**Why Wasn't I Invited** is a web application designed to help University of Toronto students easily discover events happening across the campus. By simply typing in a keyword or description of the events they're interested in, students can quickly find matching events, complete with dates and links to more information. Our platform continuously scrapes data from UofT's events websites to provide up-to-date event listings.

## Frontend Implementation

The frontend of our application is built using **React**, offering a responsive and user-friendly interface. It allows users to input search queries and displays the search results dynamically. The frontend is hosted using **AWS Amplify**, ensuring seamless deployment and scalability.

## Backend & Data Processing

### Data Scraping (`data_mining.py`)

We developed a Python script, `data_mining.py`, that scrapes event data from the UofT events website. This script uses **Beautiful Soup** for parsing HTML content and extracting event details such as event names, dates, URLs, and descriptions. Dates are standardized to the `YYYY-MM-DD` format for consistency.

### AWS Lambda and DynamoDB

The `data_mining.py` script is deployed as an **AWS Lambda** function, scheduled to run once a day. This ensures our database is regularly updated with the latest events. The scraped data is stored in an **AWS DynamoDB** table named `EventsTable`. Each event is assigned a unique `event_id` generated from the hash of its URL.

### Backend API (`app.py`)

Our backend is a **Flask** application (`app.py`) that handles user search queries. It processes input by:

- Utilizing **AWS Comprehend** to detect key phrases in the user's query.
- Tokenizing the input and filtering out common stopwords using **NLTK**.
- Searching the **DynamoDB** for events that match the processed keywords.

The backend communicates with the frontend via a RESTful API, returning search results in JSON format.

## Challenges We Ran Into

- **Learning AWS Services**: Implementing AWS Lambda and DynamoDB was challenging due to our initial unfamiliarity with these services.
- **Time Constraints**: With limited time, integrating all components and ensuring they worked seamlessly was a significant challenge.
- **Search Functionality**: Initially using Amazon Comprehend provided adequate results, but refining the search to be more accurate required developing a knowledge-based model.

## Accomplishments We're Proud Of

- **AWS Integration**: Successfully learning and implementing AWS Lambda functions and DynamoDB for data storage and processing.
- **Data Scraping**: Developing a robust data scraper that keeps our event database current.
- **Full-Stack Implementation**: Connecting the frontend and backend effectively to provide a seamless user experience.

## What We Learned

- **AWS Lambda and DynamoDB**: Gained hands-on experience with AWS serverless functions and NoSQL databases.
- **React Development**: Enhanced our skills in building dynamic user interfaces with React.
- **Python Web Scraping**: Learned advanced techniques in data scraping using Beautiful Soup.
- **Natural Language Processing**: Applied NLP techniques using **NLTK** and **AWS Comprehend** to process and interpret user queries.

## What's Next for Why Wasn't I Invited

- **LLM Integration**: Finish implementing a Large Language Model to improve search querying on the frontend.
- **Enhanced Search Algorithms**: Develop more sophisticated algorithms to increase the accuracy and relevance of search results.
- **Expanded Data Sources**: Incorporate additional UofT event sources to provide a more comprehensive event listing.
- **User Accounts and Personalization**: Implement user accounts to allow personalization of event recommendations.

## References

- [AWS Lambda Documentation](https://aws.amazon.com/lambda/)
- [AWS DynamoDB Documentation](https://aws.amazon.com/dynamodb/)
- [AWS Amplify Documentation](https://aws.amazon.com/amplify/)
- [Beautiful Soup Documentation](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
- [NLTK Documentation](https://www.nltk.org/)
- [AWS Comprehend Documentation](https://aws.amazon.com/comprehend/)
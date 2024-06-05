## Need to work on this with API currently having issues
import requests
from urllib.parse import urlencode, quote_plus
import pandas as pd
from io import StringIO
from pandas import json_normalize

# ! Replace SURVEY_CODE_HERE with our survey code attached in the email
# CSV API
base_url = "https://app.surveystack.io/api/submissions/csv"
params = { 
    'survey': 'SURVEY_CODE_HERE', # replace this with code mentioned in email
    'match': '{"meta.dateSubmitted":{"$gt":{"$date":"01 jan 2024"}}}',
    'showIrrelevant': 'true',
    'showCsvDataMeta': 'true',
    'expandAllMatrices': 'true'
}

# URL encode the parameters
encoded_params = urlencode(params, quote_via=quote_plus)
full_url = f"{base_url}?{encoded_params}"

# Make the GET request
response = requests.get(full_url)

# Check if the request was successful
if response.status_code == 200:
    # Convert the CSV data to a DataFrame
    data = pd.read_csv(StringIO(response.text))
    print("Data loaded successfully!")
    print(data.head())  # Print the first few rows to verify the data
    # Save the DataFrame to CSV
    data.to_csv("survey_data_csv_api.csv", index=False)
    print("Data saved to 'survey_data_csv_api.csv'.")
else:
    print("Failed to retrieve data:", response.status_code, response.text)

# JSON API
full_url = 'https://app.surveystack.io/api/submissions?survey=SURVEY_CODE_HERE&match={"meta.dateSubmitted":{"$gt":{"$date":"01 jan 2024"}}}'
# Make the API request
try:
    response = requests.get(full_url)
    response.raise_for_status()  # Raises an HTTPError for bad responses

    # Check if the request was successful
    if response.status_code == 200:
        data_json = response.json()  # Load data as JSON
        # Normalize the JSON data into flat tables
        data_df = json_normalize(data_json, sep='_')
        print("Data loaded and normalized successfully!")
        print(data_df.head())  # Print the first few rows to verify the data
        # Save the DataFrame to CSV
        data_df.to_csv("survey_data_json.csv", index=False)
        print("Data saved to 'survey_data_json.csv'.")
    else:
        print("Failed to retrieve data:", response.status_code, response.text)

except requests.RequestException as e:
    print("HTTP Request failed:", e)

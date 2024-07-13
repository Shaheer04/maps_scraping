import serpapi
import os
import csv
from dotenv import load_dotenv
from flatten_json import flatten
import streamlit as st
import time

load_dotenv()

api_key = os.getenv('SERPAPI_KEY') or st.secrets["SERPAPI_KEY"]
client = serpapi.Client(api_key=api_key)

# get results
def get_results(query, quards, pages):
    json_data = client.search({
        'engine': "google_maps",
        'type': 'search',
        'q': query,
        'll': quards,
        'start': pages * 20,
    })
    return json_data

# flatten the json object to write it in Csv
def flatten_dict(d, parent_key='', sep='.'):
    items = []
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten_dict(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)

# Open CSV file in write mode
def create_csv(query, quards, pages):
    csv_file_name = f"./csv/{query}.csv"
    data = get_results(query, quards, pages)
    flattened_data = flatten_dict(data)

    with open(csv_file_name, 'w', newline='', encoding='utf-8') as csv_file:
        if not os.path.exists("./csv"):
            os.makedirs("./csv")

        # Create a CSV writer
        csv_writer = csv.writer(csv_file)

        csv_writer.writerow(["position", "title", "type", "address", "phone", "website", "rating", "reviews", "description"])

        # Check if 'local_results' key exists
        if 'local_results' in flattened_data:
            for dictionary in flattened_data['local_results']:
                csv_writer.writerow([
                    dictionary.get('position', ''),
                    dictionary.get('title', ''),
                    dictionary.get('type', ''),
                    dictionary.get('address', ''),
                    dictionary.get('phone', ''),
                    dictionary.get('website', ''),
                    dictionary.get('rating', ''),
                    dictionary.get('reviews', ''),
                    dictionary.get('description', '')
                ])
            st.success(f"{csv_file_name} is created successfully!")

#function for file download
def get_file():
    with open(f"./csv/{query}.csv", "r") as file:
        btn = st.download_button(
                label="Download CSV",
                data=file,
                file_name=csv_file_name,
                mime="text/csv"
            )
        
# Streamlit app
st.title("Maps Scraping")
st.info("You can get data for different places using this webapp, for your marketing purposes")

query = st.text_input("Enter your query")
pages = st.number_input("Enter number of pages (starts from 0 as first page and maximum is 5)", max_value=5)
st.info("ADD quards like this for the location '@ + latitude + , + longitude + , + zoom', For example: @40.7128,-74.0060,3z")
st.caption(" 'Zoom parameter' : (it ranges from 3z, map completely zoomed out - to 21z, map completely zoomed in)")
quards = st.text_area("Enter longitude and latitude for the search area")

csv_file_name = f"{query}.csv"

if st.button("Get Data"):
    with st.status("Downloading data..."):
        st.write("Searching for data...")
        time.sleep(2)
        st.write("Found URL.")
        time.sleep(1)
        st.write("Downloading data...")
        time.sleep(1)
        create_csv(query, quards, pages)
    get_file()
    
    


import serpapi
import os
import csv
from dotenv import load_dotenv
import pandas as pd
from flatten_json import flatten
load_dotenv()

api_key = os.getenv('SERPAPI_KEY')
client = serpapi.Client(api_key=api_key)

json_data = client.search({
        'engine':"google_maps",
        'type': 'search',
        'q': 'bookstores in newyork',
        
})

print(json_data)

def flatten_dict(d, parent_key='', sep='.'):
    items = []
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten_dict(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)

flattened_data = flatten_dict(json_data)

# Specify CSV file name
csv_file_name = 'query.csv'

# Open CSV file in write mode
with open(csv_file_name, 'w', newline='', encoding='utf-8') as csv_file:

    # Create a CSV writer
    csv_writer = csv.writer(csv_file)

    csv_writer.writerow (flattened_data['local_results'][0].keys())

    for dictionary in flattened_data['local_results']:
        csv_writer.writerow (dictionary.values())
       



print(f'CSV file "{csv_file_name}" created successfully.')
from elasticsearch import Elasticsearch
import csv

# Connect to Elasticsearch
es = Elasticsearch()

# Specify the index and query to retrieve the data
index_name = 'articles'
query = {
    "query": {
        "match_all": {}  # Retrieve all documents, you can modify the query as needed
    }
}

# Execute the search query
search_results = es.search(index=index_name, body=query, size=10000)  # Set size as per your requirements

# Extract the relevant data from the search results
data = []
for hit in search_results['hits']['hits']:
    data.append(hit['_source'])

# Define the CSV file name
csv_filename = 'elasticsearch_data.csv'

# Extract the field names from the data
field_names = list(data[0].keys()) if data else []

# Writing the data to the CSV file
with open(csv_filename, 'w', newline='') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=field_names)
    writer.writeheader()
    writer.writerows(data)

print(f"Dataset saved to '{csv_filename}'.")
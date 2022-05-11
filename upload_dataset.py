from elasticsearch import Elasticsearch
es = Elasticsearch('https://localhost:9200')

ELASTIC_PASSWORD = "8KwOiqLxoUXsKPhZ5vZZ"

# Create the client instance
client = Elasticsearch(
    "https://localhost:9200",
    ca_certs="ca.crt",
    basic_auth=("elastic", ELASTIC_PASSWORD)
)
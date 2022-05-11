from elasticsearch import Elasticsearch


es = Elasticsearch('https://localhost:9200')

ELASTIC_PASSWORD = "8KwOiqLxoUXsKPhZ5vZZ"

# Create the client instance
client = Elasticsearch(
    "https://localhost:9200",
    ca_certs="ca.crt",
    basic_auth=("elastic", ELASTIC_PASSWORD)
)


# Post search response with value
def put_settings_elastic(value: str):
    response = client.put_script
    response = client.search(query={"fuzzy": {"sentence": {"value": value}}})
    return response

json_data = {
    'settings': {
        'analysis': {
            'analyzer': {
                'english_analyzer': {
                    'tokenizer': 'standard',
                    'filter': [
                        'lowercase',
                        'english_stop_filter',
                    ],
                },
            },
            'filter': {
                'english_stop_filter': {
                    'type': 'stop',
                    'stopwords': '_english_',
                },
            },
        },
    },
    'mappings': {
        '_doc': {
            'properties': {
                'title': {
                    'type': 'text',
                    'analyzer': 'english_analyzer',
                },
                'description': {
                    'type': 'text',
                    'analyzer': 'english_analyzer',
                },
                'publicationPlace': {
                    'type': 'text',
                    'analyzer': 'keyword',
                },
            },
        },
    },
}

response = requests.put('http://localhost:9200/library-book-text-phrase', headers=headers, json=json_data)
import logging
from datetime import datetime

from elasticsearch import Elasticsearch

es = Elasticsearch([{'host': 'localhost', 'port': 9200}])

#Sample Data
records = [
    {
        'name': "Harry Potter",
        'genre': 'Fantasy',
        'created': datetime.now(),
    },
    {
        'name': "Three",
        'genre': 'Thriller',
        'created': datetime.now(),
    },
    {
        'name': "The Notebook",
        'genre': 'Romance',
        'created': datetime.now(),
    },
]


def create_index(es_object, index_name):
    created = False
    # index settings
    settings = {
        "settings": {
            "number_of_shards": 1,
            "number_of_replicas": 0
        },
        "mappings": {
            "books": {
                "dynamic": "strict",
                "properties": {
                    "name": {
                        "type": "text"
                    },
                    "genre": {
                        "type": "text"
                    },
                    "created": {
                        "type": "date"
                    },
                }
            }
        }
    }
    try:
        if not es_object.indices.exists(index_name):
            es_object.indices.create(index=index_name,
                                     ignore=400,
                                     body=settings)
            print('Created Index')
        created = True
    except Exception as ex:
        print(str(ex))
    finally:
        return created


def store_data(es_object, index_name, data):
    try:
        outcome = es_object.index(index=index_name,
                                  doc_type='books',
                                  body=data)
    except Exception as ex:
        print('Error in indexing data')
        return {'error': str(ex)}
    return outcome


def create_and_ingest_data(es, data):
    indices = []
    for i in range(1, 4):
        index_name = f'project_{i}'
        new_index = create_index(es, index_name)
        if new_index:
            for data in records:
                print(store_data(es, index_name, data))
                indices.append(index_name)
        else:
            return {'status': False}

    return {'status': True, 'indices': indices}


if __name__ == "__main__":
    res = create_and_ingest_data(es, records)
    print(res['status'])
from flask import Flask
from flask import request
from elasticsearch import Elasticsearch
from ingestion import store_data

es = Elasticsearch()

app = Flask(__name__)


@app.route('/ingest', methods=['POST'])
def ingest():
    data = request.get_json()
    index = data['index']
    payload = data['payload']
    data = store_data(es, index, payload)
    return data


if __name__ == "__main__":
    app.run(debug=True)
import requests
import json

from elasticsearch import Elasticsearch

#es = Elasticsearch([{'host': 'localhost', 'port': 9200}])

query = {
    "script": {
        "lang": "painless",
        "source": "ctx._source.new_field = 'last_updated'"
    },
}


def re_index_wildcard(wildcard, url='http://localhost:9200/'):

    url = url + '_reindex?wait_for_completion=false'
    headers = {"Content-Type": "application/json"}
    data = {
        "source": {
            "index": wildcard
        },
        "dest": {
            "index": wildcard[:-2]
        },
        "script": {
            "lang": "painless",
            "inline": "ctx._index = ctx._index + '_1'"
        },
    }
    data = json.dumps(data)
    res = requests.post(url=url, data=data, headers=headers)
    return res.json()


def update_indices_by_query(target, data, url='http://localhost:9200/'):

    url = url + f'{target}/_update_by_query?wait_for_completion=false'
    data = json.dumps(data)
    headers = {"Content-Type": "application/json"}
    res = requests.post(url=url, data=data, headers=headers)
    return res.json()


if __name__ == "__main__":
    res_1 = re_index_wildcard('project_*')
    print(res_1)
    res_2 = update_indices_by_query('project_*', data=query)
    print(res_2)

    # Can check the status of the API's usingthe task id generated
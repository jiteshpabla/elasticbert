from elasticsearch import Elasticsearch
from bert_serving.client import BertClient
from elasticsearch.exceptions import ConnectionError, NotFoundError

# total number of responses
SEARCH_SIZE = 1
MODEL_NAME = "BERT"
INDEX_NAME = "index1" # name of the index

# establishing connections
bc = BertClient(ip='localhost', output_fmt='list', check_length=False)
client = Elasticsearch('localhost:9200')

# this query is used as the search term, feel free to change
query = 'machine learning'
query_vector = bc.encode([query])[0]

script_query = {
    "script_score": {
        "query": {"match_all": {}},
        "script": {
            "source": "cosineSimilarity(params.query_vector, doc['abstract_vector']) + 1.0",
            "params": {"query_vector": query_vector}
        }
    }
}

try:
    response = client.search(
         index= INDEX_NAME,
         body={
             "size": SEARCH_SIZE,
             "query": script_query,
             "_source": {"includes": ["title", "abstract"]}
         }
     )
    print(response)

    # to save the results in a csv
    csv_file = MODEL_NAME+"_"+query+".csv"
    csv_columns = ["_index", "_type", "_id", "_score", "_source"]
    try:
        with open(csv_file, 'w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
            writer.writeheader()
            for data in response["hits"]["hits"]:
                writer.writerow(data)
    except IOError:
        print("I/O error")
except ConnectionError:
    print("[WARNING] docker isn't up and running!")
except NotFoundError:
    print("[WARNING] no such index!")

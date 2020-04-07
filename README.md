# elasticbert

## Instructions

This code is tested on:
 - Ubuntu 18.04
 - Python 3.7.6
 - Docker 18.09.9


1. Clone the repository and change directory
```
git clone https://github.com/jiteshpabla/elasticbert.git
cd elasticbert
```

2. Download pre - trained BERT model.
```
cd bert/model
wget https://storage.googleapis.com/bert_models/2018_10_18/cased_L-12_H-768_A-12.zip
unzip cased_L-12_H-768_A-12.zip
```

3. Naviagate to `bert/` folder and setup BERT docker
```
cd ..
docker build -t bert-server .
```

4. Setup elasticsearch docker.
```
docker pull docker.elastic.co/elasticsearch/elasticsearch:7.5.2
```

5. Start docker containers.
```
docker run -d --net="host" bert-server
docker run -d -p 9200:9200 -p 9300:9300 -e "discovery.type=single-node" docker.elastic.co/elasticsearch/elasticsearch:7.5.2
```

6. (optional) Make sure the dockers are up and running by
```
docker ps
```

7. Install dependencies
```
pip3 install argparse 
pip3 install elasticsearch 
pip3 install bert-serving-client
```

8. Create elasticsearch index
```
python3 elastic/create_index.py --index index1 --config elastic/index_config.json
```
create_index.py script creates an index in elasticsearch.
`--index` and `--config` arguments specify the name of the elasticsearch index and schema of the target index, respectively.
You can verify the index by checking `http://127.0.0.1:9200/index1`

9. Create documents
```
python3 elastic/create_document.py --index index1 --csv elastic/example.csv --output example.json1
```
This script creates an example.json1 file in the elasticsearch prescribed format which in-turn to be indexed later.

10. Create indexes
```
python3 elastic/index_documents.py --data example.json1
```
This scripts generates the actual indexes and saves it into elasticsearch
verify it by checking `http://127.0.0.1:9200/index1/_search`

11. Test the engine.
```
python3 elastic/elastic.py
```

These instructions have been adapted from https://github.com/kelvin-jose/elasticbert.

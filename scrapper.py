import copy
import json

import requests

url = "https://search-aiindex-76cl5n3qdcbspk7eztijpvdq6i.us-east-2.es.amazonaws.com/arxiv2/documents/_msearch?"
data_template = [{"preference": "SearchResult"},
                {"query": {"bool": {"must": [{"bool": {"must": [{"bool": {"should": [{"multi_match": {
                    "query": "Ukraine", "fields": ["content"], "type": "best_fields", "operator": "or",
                    "fuzziness": 0}}, {"multi_match": {"query": "Ukraine", "fields": ["content"],
                                                       "type": "phrase_prefix", "operator": "or"}}],
                                                                          "minimum_should_match": "1"}}]}}]}},
                 "size": 8, "_source": {"includes": ["*"], "excludes": []}, "from": 0}]
headers = {"Content-type": "application/x-ndjson"}
mx = 1
mx_id = 0
all_hits = []
while mx_id < mx:
    data_to_post = copy.deepcopy(data_template)
    data_to_post[1]["from"] = mx_id
    data_to_post = '\n'.join(json.dumps(d) for d in data_to_post) + "\n"
    r = requests.post(url, headers=headers, data=data_to_post)
    info = json.loads(r.text)
    mx = info['responses'][0]['hits']["total"]['value']
    hits = info['responses'][0]['hits']['hits']
    all_hits += hits
    mx_id += len(hits)
    print(mx_id)

print(len(all_hits))
with open("hits.json", "w") as f:
   json.dump(all_hits, f)

#print()
#all_data
#print(data)
#print(len(data))
# print(len(info['took']))
# print(info.keys())
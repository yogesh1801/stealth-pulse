import pandas as pd
import os
import json
from elasticsearch7 import Elasticsearch
from elasticsearch7.helpers import bulk

def process(input_file, output_dir):
    df = pd.read_csv(input_file, usecols=range(10))
    df['id'] = range(1, len(df) + 1)
    
    columns_to_fill = ['title', 'tag', 'sourceURL', 'category']
    df[columns_to_fill] = df[columns_to_fill].fillna('')

    es = Elasticsearch(['http://localhost:9200'])
    documents = []

    INDEX_NAME = "assignment_index"
    if not es.indices.exists(index=INDEX_NAME):
        es.indices.create(index=INDEX_NAME)
        print(f"Created index: {INDEX_NAME}")

    for _, row in df.iterrows():

        document = {
            "_index": INDEX_NAME,
            "_id": int(row['id']),
            "title": row['title'],
            "tags": row['tag'],
            "url": row['sourceURL'],
            "category": row['category']
        }
        documents.append(document)
        
    success, _ = bulk(es, documents)
    print(f"Indexed {success} documents")

    queries_file = "../queries.txt"
    with open(queries_file, 'r') as f:
        queries = f.readlines()

    results = {}

    for i, query in enumerate(queries, 1):
        query = query.strip().split('. ', 1)[-1].strip()
        res = es.search(index=INDEX_NAME,
            query = {
                "multi_match": {
                    "query": query,
                    "fields": ["title", "tags", "category", "url"],
                    "type": "best_fields",
                    "tie_breaker": 0.3
                }
            },
            size= 100)

        results[f"query{i}"] = res['hits']['hits']

    print("queries done")
    
    os.makedirs(output_dir, exist_ok=True)
    for query_num, docs in results.items():
        with open(f"{output_dir}/{query_num}Results.txt", 'w', encoding='utf-8') as f:
            for doc in docs:
                doc_id = doc['_id']
                title = doc['_source']['title']
                score = doc['_score']
                f.write(f"{doc_id} {title} {score}\n")
    print("Results written")
    
if __name__ == "__main__":
    input_file = "../assessment_data.csv"  
    output_dir = "../Results"  
    process(input_file, output_dir)
    print("Processing completed successfully.")

# nlp4j-llm-embeddings-e5

nlp4j-llm-embeddings-e5

## Installation

Clone the repository:

```sh
git clone https://github.com/oyahiroki/nlp4j-llm-embeddings-e5.git
cd example-python-project
pip install -r requirements.txt
```


```
http://127.0.0.1:8888/?text=これはテストです。
```

```
http://127.0.0.1:8888/?text=%E3%81%93%E3%82%8C%E3%81%AF%E3%83%86%E3%82%B9%E3%83%88%E3%81%A7%E3%81%99%E3%80%82
```

```
curl -X POST -H "Content-Type: application/json" -d "{\"text\":\"これはテストです。\"}" http://127.0.0.1:8888/
```

```
Expected response: {"message": "ok", "time": "2024-05-26T23:21:38", "text": "これはテストです。", "embeddings": [0.04231283441185951, -0.0035561583936214447, -0.014567600563168526, ... 0.022928446531295776]}
```


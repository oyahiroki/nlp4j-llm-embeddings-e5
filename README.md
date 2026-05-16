https://github.com/oyahiroki/nlp4j-llm-embeddings-e5

# Multilingual E5 Embedding Server

[Japanese 日本語](README_ja.md)

## nlp4j-llm-embeddings-e5

A lightweight, REST API-powered server for generating multilingual embeddings using the E5 model. This server is built with sentence-transformers and provides an easy-to-use interface for text processing tasks.

## Key Features

### 1. Embeddings API (`/embeddings`)
Convert text into vector embeddings for document search. Automatically applies E5's "passage:" prefix for optimal performance.

### 2. Semantic Search API (`/semantic_search`)
Perform semantic search between queries and corpus. Automatically applies "query:" prefix for queries and "passage:" prefix for corpus documents.

### 3. Cosine Similarity API (`/cos_sim`)
Calculate cosine similarity between two texts without prefixes.

## Prerequisites 

Python

```
$ python3 --version
Python 3.10.12
```


## Installation

To get started, follow these steps:

Clone the repository:

```
git clone https://github.com/oyahiroki/nlp4j-llm-embeddings-e5.git
```

Navigate to the project directory:

```
cd nlp4j-llm-embeddings-e5
```

Install the required dependencies:

```
pip install -r requirements.txt
```

## How to Run

Start the server with the following command:

```bash
python3 nlp4j-embedding-server-e5.py
```

### Command Line Options

- `--host`: Bind host (default: 127.0.0.1)
- `-p, --port`: Port number (default: 8888)

Example:
```bash
python3 nlp4j-embedding-server-e5.py --host 0.0.0.0 --port 9000
```

## API Usage

The server provides a REST API for sending text and receiving its embeddings. Below are usage examples for GET and POST requests.

### Embeddings API

#### GET Request (Plain Text)

Send a plain text query without encoding:

```bash
curl http://127.0.0.1:8888/embeddings?text=これはテストです。
```

#### GET Request (URL Encoded)

Send a text query with URL encoding:

```bash
curl http://127.0.0.1:8888/embeddings?text=%E3%81%93%E3%82%8C%E3%81%AF%E3%83%86%E3%82%B9%E3%83%88%E3%81%A7%E3%81%99%E3%80%82
```

#### POST Request (JSON Body)

Send text in a JSON request body:

```bash
curl -X POST -H "Content-Type: application/json" \
  -d '{"text":"これはテストです。"}' \
  http://127.0.0.1:8888/embeddings
```

#### Request with Token Count Check

```bash
curl http://127.0.0.1:8888/embeddings?text=これはテストです。&checktokencount=true
```

#### Expected Response

The server returns a JSON response with the following structure:

```json
{
  "message": "ok",
  "time": "2024-05-26T23:21:38",
  "text": "これはテストです。",
  "embeddings": [0.04231283441185951, -0.0035561583936214447, -0.014567600563168526, ...]
}
```

With token count check:
```json
{
  "message": "ok",
  "time": "2024-05-26T23:21:38",
  "text": "これはテストです。",
  "token_count": 15,
  "max_tokens": 512,
  "truncated": false,
  "embeddings": [...]
}
```

### Semantic Search API

#### GET Request

```bash
curl "http://127.0.0.1:8888/semantic_search?text1=これはテストです。&text2=これは試験です。"
```

#### POST Request (Multiple Documents)

```bash
curl -X POST -H "Content-Type: application/json" \
  -d '{"text":"これはテストです。","texts":["これは試験です。","これは検査です。"]}' \
  http://127.0.0.1:8888/semantic_search
```

#### Expected Response

```json
{
  "message": "ok",
  "time": "2024-05-26T23:21:38",
  "text": "これはテストです。",
  "r": [
    {"corpus_id": 0, "score": 0.8234},
    {"corpus_id": 1, "score": 0.7891}
  ]
}
```

### Cosine Similarity API

#### GET Request

```bash
curl "http://127.0.0.1:8888/cos_sim?text1=これはテストです。&text2=これは試験です。"
```

#### POST Request

```bash
curl -X POST -H "Content-Type: application/json" \
  -d '{"text1":"これはテストです。","text2":"これは試験です。"}' \
  http://127.0.0.1:8888/cos_sim
```

#### Request with Token Count Check

```bash
curl "http://127.0.0.1:8888/cos_sim?text1=これはテストです。&text2=これは試験です。&checktokencount=true"
```

#### Expected Response

```json
{
  "text1": "これはテストです。",
  "text2": "これは試験です。",
  "cosine_similarity": 0.8234567
}
```

With token count check:
```json
{
  "text1": "これはテストです。",
  "text2": "これは試験です。",
  "max_tokens": 512,
  "token_count1": 15,
  "token_count2": 14,
  "truncated1": false,
  "truncated2": false,
  "cosine_similarity": 0.8234567
}
```

## REST API Overview

This API enables easy integration into various applications through HTTP requests. The server supports both GET and POST methods.

GET: Simple and fast for passing text as query parameters.

POST: Ideal for structured data, allowing JSON payloads for complex requests.

## Advantages of REST API Integration

Language Independence: The API can be used with any programming language capable of sending HTTP requests (e.g., Python, Java, JavaScript, Ruby).

Ease of Integration: No need to modify server-side code; the API is ready for immediate use.

Scalability: Handles multiple concurrent requests, making it suitable for production workloads.

## Docker Support

### Build Docker Image

```bash
docker build -t nlp4j-llm-embeddings-e5 ./docker
```

Or with a specific version tag:

```bash
docker build --no-cache -t oyahiroki/nlp4j-llm-embeddings-e5:1.0.0.0 ./docker
```

### Run Container

```bash
docker run -d --name nlp4j-llm-embeddings-e5 -p 8888:8888 nlp4j-llm-embeddings-e5
```

### Test

```bash
curl http://127.0.0.1:8888/embeddings?text=%E3%81%93%E3%82%8C%E3%81%AF%E3%83%86%E3%82%B9%E3%83%88%E3%81%A7%E3%81%99%E3%80%82
```

For more details, see [docker/README.md](docker/README.md).

---


# Overview of Multilingual E5 Embedding

The Multilingual E5 Embedding, available on Hugging Face, is a large-scale language model designed for feature extraction in 94 languages.

## Foundation and Training Data

It uses a base of XLM-RoBERTa, trained on a diverse set of multilingual datasets, enhancing text encoding capabilities for various tasks like text retrieval and semantic similarity.

## Performance and Applications

The model achieves high performance across a variety of benchmarks, particularly in multilingual environments.

## Implementation and Integration

It is implemented with PyTorch and compatible with Sentence Transformers for easy integration into applications.

For more details, you can view the full description on [the Hugging Face page](https://huggingface.co/intfloat/multilingual-e5-large) .




## Example of Resources

```
$ ps aux | grep python
oyahiro+   832  0.0  4.1 128670360 4127176 pts/3 Sl Jul17   0:32 python3 nlp4j-embedding-server-e5.py
oyahiro+   962  0.0  0.0   3536  1040 pts/3    R+   00:57   0:00 grep --color=auto python
```

```
$ nvidia-smi
Thu Jul 18 01:03:18 2024
+-----------------------------------------------------------------------------------------+
| NVIDIA-SMI 550.54.10              Driver Version: 551.61         CUDA Version: 12.4     |
|-----------------------------------------+------------------------+----------------------+
| GPU  Name                 Persistence-M | Bus-Id          Disp.A | Volatile Uncorr. ECC |
| Fan  Temp   Perf          Pwr:Usage/Cap |           Memory-Usage | GPU-Util  Compute M. |
|                                         |                        |               MIG M. |
|=========================================+========================+======================|
|   0  NVIDIA GeForce RTX 3060 Ti     On  |   00000000:01:00.0 Off |                  N/A |
| 30%   32C    P8             10W /  200W |    3737MiB /   8192MiB |     12%      Default |
|                                         |                        |                  N/A |
+-----------------------------------------+------------------------+----------------------+

+-----------------------------------------------------------------------------------------+
| Processes:                                                                              |
|  GPU   GI   CI        PID   Type   Process name                              GPU Memory |
|        ID   ID                                                               Usage      |
|=========================================================================================|
|    0   N/A  N/A       832      C   /python3.10                                 N/A      |
+-----------------------------------------------------------------------------------------+
$
```

The time taken for embedding was 0.05 - 0.1 seconds when using the NVIDIA GeForce RTX 3060 Ti.

```bash
$ curl -w"time_total: %{time_total}\n" -X POST -H "Content-Type: application/json" \
  -d '{"text":"これはテストです。"}' http://127.0.0.1:8888/embeddings

{"message": "ok", "time": "2024-07-19T16:25:52", "text": "これはテストです。",
 "embeddings": [0.04231283441185951, -0.0035561583936214447, ...]}
time_total: 0.058588
```

## Test Scripts

The project includes sample scripts to test the API:

### Test Embeddings

```bash
python3 bin/nlp4j-embedding-server-e5-test-embedding.py
```

### Test Cosine Similarity

```bash
python3 bin/nlp4j-embedding-server-e5-test-cos_sim.py
```

## Utility Tools

### Local Embedding Processing

Tool for batch processing JSONL files:

```bash
python3 bin/nlp4j-embedding-local-e5.py input.jsonl output.jsonl \
  --text-attr text --vector-attr vector
```

## Project Structure

```
nlp4j-llm-embeddings-e5/
├── nlp4j-embedding-server-e5.py          # Main server
├── requirements.txt                       # Dependencies
├── README.md                              # English README
├── README_ja.md                           # Japanese README
├── LICENSE.txt                            # Apache License 2.0
├── bin/                                   # Utilities and test scripts
│   ├── nlp4j_embedding_server_requesthandler.py  # Request handler
│   ├── nlp4j-embedding-server-e5-test-embedding.py
│   ├── nlp4j-embedding-server-e5-test-cos_sim.py
│   ├── nlp4j-embedding-local-e5.py
│   └── nlp4j-embedding-local-openai.py
├── docker/                                # Docker configuration
│   ├── Dockerfile
│   └── README.md
├── html/                                  # Web interface
│   └── index.html
└── bak/                                   # Backup files
```

## Technical Specifications

- **Model**: intfloat/multilingual-e5-large
- **Base Model**: XLM-RoBERTa
- **Supported Languages**: 94 languages
- **Max Tokens**: 512
- **Embedding Dimension**: 1024
- **Normalization**: L2 normalized

## E5 Prefixes

The E5 model uses specific prefixes for optimal performance:

- **passage:**: For document/corpus embeddings (search targets)
- **query:**: For query embeddings (search sources)

This server automatically applies these prefixes at the appropriate endpoints.

## Troubleshooting

### Model Download Takes Time

On first startup, the model will be automatically downloaded (~2GB). This only happens once.

### Out of Memory Errors

- GPU usage: Minimum 8GB VRAM recommended
- CPU usage: Minimum 8GB RAM recommended

### Port Already in Use

Specify a different port:
```bash
python3 nlp4j-embedding-server-e5.py --port 9000
```

## License

Apache License 2.0

Copyright 2024 Hiroki Oya (NLP4J)

See [LICENSE.txt](LICENSE.txt) for details.

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## Support

If you have any issues or questions, please create a GitHub issue:
https://github.com/oyahiroki/nlp4j-llm-embeddings-e5/issues

## Conclusion

This project offers a highly efficient solution for generating multilingual text embeddings. The REST API provides flexibility, making it a valuable tool for natural language processing tasks such as search, recommendation, and semantic analysis.


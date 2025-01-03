https://github.com/oyahiroki/nlp4j-llm-embeddings-e5

# Multilingual E5 Embedding Server


## nlp4j-llm-embeddings-e5

A lightweight, REST API-powered server for generating multilingual embeddings using the E5 model. This server is built with sentence-transformers and provides an easy-to-use interface for text processing tasks.

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

```
python3 nlp4j-embedding-server-e5.py
```

## API Usage

The server provides a REST API for sending text and receiving its embeddings. Below are usage examples for GET and POST requests.

### GET Request (Plain Text)

Send a plain text query without encoding:

```
curl http://127.0.0.1:8888/?text=これはテストです。
```

### GET Request (URL Encoded)

Send a text query with URL encoding:

```
curl http://127.0.0.1:8888/?text=%E3%81%93%E3%82%8C%E3%81%AF%E3%83%86%E3%82%B9%E3%83%88%E3%81%A7%E3%81%99%E3%80%82
```

### POST Request (JSON Body)

Send text in a JSON request body:

```
curl -X POST -H "Content-Type: application/json" -d "{\"text\":\"これはテストです。\"}" http://127.0.0.1:8888/
```

### POST Request (URL Encoded Body)

Send a URL-encoded string in the JSON body:

```
curl -X POST -H "Content-Type: application/json" -d "{\"text\":\"%E3%81%93%E3%82%8C%E3%81%AF%E3%83%86%E3%82%B9%E3%83%88%E3%81%A7%E3%81%99%E3%80%82\"}" http://127.0.0.1:8888/
```

### Expected Response

The server returns a JSON response with the following structure:

```
{
  "message": "ok",
  "time": "2024-05-26T23:21:38",
  "text": "これはテストです。",
  "embeddings": [0.04231283441185951, -0.0035561583936214447, -0.014567600563168526, ... 0.022928446531295776]
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

# Conclusion

This project offers a highly efficient solution for generating multilingual text embeddings. The REST API provides flexibility, making it a valuable tool for natural language processing tasks such as search, recommendation, and semantic analysis.

This version improves readability and provides a more detailed explanation for users unfamiliar with the project or its functionality. Let me know if additional enhancements are needed!

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

```
$ curl -w"time_total: %{time_total}\n" -X POST -H "Content-Type: application/json" -d "{\"text\":\"これはテストです。\"}" http://127.0.0.1:8888/
{"message": "ok", "time": "2024-07-19T16:25:52", "text": "\u3053\u308c\u306f\u30c6\u30b9\u30c8\u3067\u3059\u3002", "embeddings": [0.04231283441185951, -0.0035561583936214447, -0.014567600563168526, -0.057356465607881546, 0.033991988748311996, -0.023742299526929855, 0.006811152212321758, 0.08303837478160858, 0.04199839010834694, ... -0.02498556673526764, -0.03213634714484215, 0.022928446531295776]}time_total: 0.058588


```


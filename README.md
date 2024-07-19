# nlp4j-llm-embeddings-e5

nlp4j-llm-embeddings-e5

## Installation

Clone the repository:

```sh
git clone https://github.com/oyahiroki/nlp4j-llm-embeddings-e5.git
cd nlp4j-llm-embeddings-e5
pip install -r requirements.txt
```

## How to run

```
$ python3 nlp4j-embedding-server-e5.py
```

## How to call

### GET (unencoded)

```
http://127.0.0.1:8888/?text=これはテストです。
```

### GET (URL encoded)

```
http://127.0.0.1:8888/?text=%E3%81%93%E3%82%8C%E3%81%AF%E3%83%86%E3%82%B9%E3%83%88%E3%81%A7%E3%81%99%E3%80%82
```

### POST (Request body is JSON)

```
curl -X POST -H "Content-Type: application/json" -d "{\"text\":\"これはテストです。\"}" http://127.0.0.1:8888/
```

### Expected response

```
{"message": "ok", "time": "2024-05-26T23:21:38", "text": "これはテストです。", "embeddings": [0.04231283441185951, -0.0035561583936214447, -0.014567600563168526, ... 0.022928446531295776]}
```


## REST API

The REST API interface allows this server to be easily accessed from applications written in different programming languages. This interoperability makes it highly versatile for various development environments.

- **GET Request**:
  ```bash
  curl "http://127.0.0.1:8888/?text=これはテストです。"
  ```
  This request sends a text query to the server, which responds with the processed embeddings.

- **POST Request**:
  ```bash
  curl -X POST -H "Content-Type: application/json" -d '{"text":"これはテストです。"}' http://127.0.0.1:8888/
  ```
  This sends a JSON payload with the text to be processed, and the server responds with a JSON containing the embeddings.

### Sample Response
The response JSON includes the status message, current timestamp, the input text, and its corresponding sentence embeddings:
```json
{
  "message": "ok",
  "time": "2024-05-26T23:21:38",
  "text": "これはテストです。",
  "embeddings": [0.04231283441185951, -0.0035561583936214447, -0.014567600563168526, ... 0.022928446531295776]
}
```

### Benefits of REST API Integration

- **Language Agnostic**: The REST API allows the server to be accessed from any programming language that can make HTTP requests, including JavaScript, Java, C#, Ruby, and more.
- **Ease of Use**: Developers can integrate text processing capabilities into their applications without needing to understand the underlying Python code.
- **Scalability**: The multithreaded nature of the server ensures it can handle multiple requests concurrently, making it suitable for production environments.

### Conclusion

This script demonstrates a straightforward yet powerful approach to creating a text processing server using Python. By leveraging the `sentence-transformers` library for generating embeddings and implementing a multithreaded HTTP server with a REST API interface, it efficiently handles text input and produces valuable output. The REST API integration ensures that this server can be seamlessly used from various programming languages and platforms, making it a versatile tool for a wide range of natural language processing tasks.



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

The time taken for embedding was 2.5 seconds when using the NVIDIA GeForce RTX 3060 Ti.

```
$ curl -w"time_total: %{time_total}\n" -X POST -H "Content-Type: application/json" -d "{\"text\":\"これはテストです。\"}" http://127.0.0.1:8888/
{"message": "ok", "time": "2024-07-19T16:25:52", "text": "\u3053\u308c\u306f\u30c6\u30b9\u30c8\u3067\u3059\u3002", "embeddings": [0.04231283441185951, -0.0035561583936214447, -0.014567600563168526, -0.057356465607881546, 0.033991988748311996, -0.023742299526929855, 0.006811152212321758, 0.08303837478160858, 0.04199839010834694, ... -0.02498556673526764, -0.03213634714484215, 0.022928446531295776]}time_total: 2.594760


```


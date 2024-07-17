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

## Resources

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


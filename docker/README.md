https://github.com/oyahiroki/nlp4j-llm-embeddings-e5/tree/main/docker

# HOW-TO-USE

# 0. Installation

```
git clone https://github.com/oyahiroki/nlp4j-llm-embeddings-e5.git
```


# 1. BUILD


```
$ docker build --no-cache -t oyahiroki/nlp4j-llm-embeddings-e5:1.0.0.0.20250303 ./nlp4j-llm-embeddings-e5/docker
```


# 2. RUN

```
docker run -d --name nlp4j-llm-embeddings-e5 -p 8888:8888 img_nlp4j-llm-embeddings-e5
```

# 3. TEST

```
curl http://127.0.0.1:8888/?text=%E3%81%93%E3%82%8C%E3%81%AF%E3%83%86%E3%82%B9%E3%83%88%E3%81%A7%E3%81%99%E3%80%82
```

---

## Docker build for publish

```
docker build -t oyahiroki/nlp4j-llm-embeddings-e5:1.0.0.0 -t oyahiroki/nlp4j-llm-embeddings-e5:latest .
```

```
[+] Building 499.3s (11/11) FINISHED                                                               docker:desktop-linux
 => [internal] load build definition from Dockerfile                                                               0.1s
 => => transferring dockerfile: 1.29kB                                                                             0.0s
 => [internal] load metadata for docker.io/library/python:3.10-slim                                                2.7s
 => [auth] library/python:pull token for registry-1.docker.io                                                      0.0s
 => [internal] load .dockerignore                                                                                  0.1s
 => => transferring context: 2B                                                                                    0.0s
 => [1/6] FROM docker.io/library/python:3.10-slim@sha256:bdc6c5b8f725df8b009b32da65cbf46bfd24d1c86dce2e6169452c19  7.8s
 => => resolve docker.io/library/python:3.10-slim@sha256:bdc6c5b8f725df8b009b32da65cbf46bfd24d1c86dce2e6169452c19  0.0s
 => => sha256:75c8834d673790bec55c0462db7093813c31b9f20a4518c4002f4e787c1e6b18 1.75kB / 1.75kB                     0.0s
 => => sha256:fed91319d6a7007de26639d3a7316659ebb1b3527df1fd5d29242dc0921e3d30 5.29kB / 5.29kB                     0.0s
 => => sha256:fd674058ff8f8cfa7fb8a20c006fc0128541cbbad7f7f7f28df570d08f9e4d92 28.23MB / 28.23MB                   5.2s
 => => sha256:a1235d039a7d629d661cd58c84386a20caab12ed3ba2ca999d194fb1055a3113 3.32MB / 3.32MB                     2.3s
 => => sha256:e17464c8c9fbfac9efc479940986e26dc06b5d14b5753c16971f6930184b2f42 15.65MB / 15.65MB                   7.1s
 => => sha256:bdc6c5b8f725df8b009b32da65cbf46bfd24d1c86dce2e6169452c193ad660b4 9.13kB / 9.13kB                     0.0s
 => => sha256:f344618db07e51c52e9a0ca634b057784db11516d257efd7fc211dfe4199bc45 249B / 249B                         2.6s
 => => extracting sha256:fd674058ff8f8cfa7fb8a20c006fc0128541cbbad7f7f7f28df570d08f9e4d92                          0.8s
 => => extracting sha256:a1235d039a7d629d661cd58c84386a20caab12ed3ba2ca999d194fb1055a3113                          0.1s
 => => extracting sha256:e17464c8c9fbfac9efc479940986e26dc06b5d14b5753c16971f6930184b2f42                          0.4s
 => => extracting sha256:f344618db07e51c52e9a0ca634b057784db11516d257efd7fc211dfe4199bc45                          0.0s
 => [2/6] RUN apt-get update && apt-get install -y git                                                            11.4s
 => [3/6] WORKDIR /app                                                                                             0.1s
 => [4/6] RUN git clone https://github.com/oyahiroki/nlp4j-llm-embeddings-e5.git                                   1.2s
 => [5/6] WORKDIR /app/nlp4j-llm-embeddings-e5                                                                     0.1s
 => [6/6] RUN pip install --no-cache-dir -r requirements.txt                                                     467.7s
 => exporting to image                                                                                             8.0s
 => => exporting layers                                                                                            8.0s
 => => writing image sha256:72c0dbb4904502c6373e76364b3c45d3357811f960fab383f9c6af50be5484c0                       0.0s
 => => naming to docker.io/oyahiroki/nlp4j-llm-embeddings-e5:1.0.0.0                                               0.0s
 => => naming to docker.io/oyahiroki/nlp4j-llm-embeddings-e5:latest                                                0.0s

View build details: docker-desktop://dashboard/build/desktop-linux/desktop-linux/ijhwwhufmhxbudrbjycnmwc4h

What's next:
    View a summary of image vulnerabilities and recommendations → docker scout quickview

>
```

```
docker run --name nlp4j-llm-embeddings-e5 -p 8888:8888 oyahiroki/nlp4j-llm-embeddings-e5
```



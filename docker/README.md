https://github.com/oyahiroki/nlp4j-llm-embeddings-e5/docker/README.md

# HOW-TO-USE

# 1. BUILD

```
docker build -t img_nlp4j-llm-embeddings-e5 .
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


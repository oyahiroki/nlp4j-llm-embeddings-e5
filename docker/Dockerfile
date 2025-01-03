# https://github.com/oyahiroki/nlp4j-llm-embeddings-e5/docker/Dockerfile

# Docker file for multilingual-E5-large embedding server
# Python + nlp4j-llm-embeddings-e5  

# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Install git
RUN apt-get update && apt-get install -y git

# Set the initial working directory
WORKDIR /app

# Clone the repository
RUN git clone https://github.com/oyahiroki/nlp4j-llm-embeddings-e5.git

# Change the working directory to the newly cloned repository
WORKDIR /app/nlp4j-llm-embeddings-e5

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 8888 available to the world outside this container
EXPOSE 8888

# Define environment variable
ENV NAME=nlp4j-llm-embeddings-e5

# Run nlp4j-embedding-server-e5.py when the container launches
CMD ["python3", "nlp4j-embedding-server-e5.py"]


# HOW-TO-USE
# 1. BUILD
# > docker build -t img_nlp4j-llm-embeddings-e5 .
# 2. RUN
# > docker run -d --name nlp4j-llm-embeddings-e5 -p 8888:8888 img_nlp4j-llm-embeddings-e5
# 3. TEST
# curl http://127.0.0.1:8888/?text=%E3%81%93%E3%82%8C%E3%81%AF%E3%83%86%E3%82%B9%E3%83%88%E3%81%A7%E3%81%99%E3%80%82


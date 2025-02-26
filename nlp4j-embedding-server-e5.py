# coding: utf-8

# /embedding Embedding Server
# /semantic_search Semantic Search Server
# /cos_sim Cosine Similarity
# / (default) Embedding Server

from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs, unquote
import json
import traceback
from socketserver import ThreadingMixIn
import sys
import time
import datetime
import signal
from sentence_transformers import SentenceTransformer, util
import argparse

from bin.nlp4j_embedding_server_requesthandler import EmbeddingRequestHandler

signal.signal(signal.SIGINT, signal.SIG_DFL)

def sig_handler(signum, frame) -> None:
	sys.exit(1)

class HelloHttpServer(ThreadingMixIn, HTTPServer):
	pass

def main():
	signal.signal(signal.SIGTERM, sig_handler)
#	 ip = '127.0.0.1'
	ip = '0.0.0.0'
	
	parser = argparse.ArgumentParser(description="nlp4j-embedding")
	parser.add_argument("-p", "--port", type=int, default=8888, help="Port Number")
	args = parser.parse_args()	
	
	port = args.port
	print("[Examples]")
	# Embeddings
	print("http://localhost:" + str(port) + "/embeddings?text=これはテストです。")
	print("curl -X POST -H \"Content-Type: application/json\" -d \"{\\\"text\\\":\\\"これはテストです。\\\"}\" http://" + ip + ":" + str(port) + "/embeddings")
	# semantic_search
	print()
	print("http://localhost:" + str(port) + "/semantic_search?text1=これはテストです。&text2=これは試験です。")
	print("curl -X POST -H \"Content-Type: application/json\" -d \"{\\\"text1\\\":\\\"これはテストです。\\\",\\\"text2\\\":\\\"これは試験です。\\\"}\" http://" + ip + ":" + str(port) + "/embeddings")
	# cos_sim
	print()
	print("http://localhost:" + str(port) + "/cos_sim?text1=これはテストです。&text2=これは試験です。")
	print("curl -X POST -H \"Content-Type: application/json\" -d \"{\\\"text1\\\":\\\"これはテストです。\\\",\\\"text2\\\":\\\"これは試験です。\\\"}\" http://" + ip + ":" + str(port) + "/cos_sim")
	
	# これはテストです
	# これは試験です
	# http://localhost:8888/semanticsearch?text1=%E3%81%93%E3%82%8C%E3%81%AF%E3%83%86%E3%82%B9%E3%83%88%E3%81%A7%E3%81%99&text2=%E3%81%93%E3%82%8C%E3%81%AF%E8%A9%A6%E9%A8%93%E3%81%A7%E3%81%99
	
	server = HelloHttpServer((ip, port), EmbeddingRequestHandler)
	try:
		server.serve_forever()
	except KeyboardInterrupt:
		pass
	finally:
		server.server_close()

if __name__ == '__main__':
	main()

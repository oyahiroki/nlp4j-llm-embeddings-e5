# coding: utf-8

# /embeddings      Embedding Server
# /semantic_search Semantic Search Server
# /cos_sim         Cosine Similarity
# / (default)      Embedding Server

from http.server import HTTPServer
from socketserver import ThreadingMixIn
import argparse
import signal

from bin.nlp4j_embedding_server_requesthandler import EmbeddingRequestHandler


class HelloHttpServer(ThreadingMixIn, HTTPServer):
	# ThreadingMixIn を使う場合の定番設定（運用で事故りにくい）
	daemon_threads = True
	allow_reuse_address = True


def main():
	parser = argparse.ArgumentParser(description="nlp4j-embedding")
	parser.add_argument("--host", type=str, default="127.0.0.1", help="Bind host (default: 127.0.0.1)")
	parser.add_argument("-p", "--port", type=int, default=8888, help="Port Number")
	args = parser.parse_args()

	host = args.host
	port = args.port

	server = HelloHttpServer((host, port), EmbeddingRequestHandler)

	def _sigterm_handler(signum, frame):
		# 穏当に止める（docker stop 等）
		try:
			server.shutdown()
		except Exception:
			pass

	# Ctrl+C はデフォルト動作に戻す（開発用途）
	signal.signal(signal.SIGINT, signal.SIG_DFL)
	# SIGTERM は graceful shutdown
	signal.signal(signal.SIGTERM, _sigterm_handler)

	print("[Examples]")
	# Embeddings
	print(f"http://localhost:{port}/embeddings?text=これはテストです。")
	print(f"http://localhost:{port}/embeddings?text=これはテストです。&checktokencount=true")
	print(f"curl -X POST -H \"Content-Type: application/json\" -d \"{{\\\"text\\\":\\\"これはテストです。\\\"}}\" http://{host}:{port}/embeddings")

	# semantic_search
	print()
	print(f"http://localhost:{port}/semantic_search?text1=これはテストです。&text2=これは試験です。")
	print(f"http://localhost:{port}/semantic_search?text1=これはテストです。&text2=これは試験です。&checktokencount=true")
	print(f"curl -X POST -H \"Content-Type: application/json\" -d \"{{\\\"text\\\":\\\"これはテストです。\\\",\\\"texts\\\":[\\\"これは試験です。\\\"]}}\" http://{host}:{port}/semantic_search")

	# cos_sim
	print()
	print(f"http://localhost:{port}/cos_sim?text1=これはテストです。&text2=これは試験です。")
	print(f"http://localhost:{port}/cos_sim?text1=これはテストです。&text2=これは試験です。&checktokencount=true")
	print(f"curl -X POST -H \"Content-Type: application/json\" -d \"{{\\\"text1\\\":\\\"これはテストです。\\\",\\\"text2\\\":\\\"これは試験です。\\\",\\\"checktokencount\\\":true}}\" http://{host}:{port}/cos_sim")

	try:
		server.serve_forever()
	except KeyboardInterrupt:
		pass
	finally:
		server.server_close()


if __name__ == '__main__':
	main()
